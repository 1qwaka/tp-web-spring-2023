from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "mb-3"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "mb-3"}))
    avatar = forms.ImageField(required=False)


    class Meta:
        model = User
        fields = ["username", "email", "first_name"]

        labels = {
            "first_name": "Nickname"
        }

        widgets = {
            "username": forms.TextInput(attrs={"class": "mb-3"}),
            "first_name": forms.TextInput(attrs={"class": "mb-3"}),
            "email": forms.EmailInput(attrs={"class": "mb-3"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get("password", "")
        passwd_rep = cleaned_data.get("password_repeat", b"\0\0")

        if passwd != passwd_rep:
            self.add_error("password_repeat", "Passwords don't match")

        if "email" in cleaned_data.keys():
            if len(cleaned_data["email"]) == 0:
                self.add_error("email", "Empty email not allowed")
            else:
                has_same_email = User.objects.filter(email=cleaned_data["email"])
                if has_same_email.count() > 0:
                    self.add_error("email", "User with email already exists")
        else:
            self.add_error("email", "Invalid email")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        user.save()
        profile = Profile.objects.create(user=user, avatar=self.cleaned_data["avatar"])
        # profile = Profile(user=user)

        if commit:
            profile.save()

        return profile


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "last_name", "first_name"]

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.avatar = self.cleaned_data["avatar"]
        profile.save()
        return user


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "mb-3"}), label="Tags")

    class Meta:
        model = Question
        fields = "__all__"
        fields = ["header", "text"]

        labels = {
            "header": "Title"
        }

        # widgets = {
        #     "username": forms.TextInput(attrs={"class": "mb-3"}),
        #     "first_name": forms.TextInput(attrs={"class": "mb-3"}),
        #     "email": forms.EmailInput(attrs={"class": "mb-3"}),
        # }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text", "")
        header = cleaned_data.get("header", "")

        if text == "":
            self.add_error("text", "Question cannot be empty")

        if header == "":
            self.add_error("header", "Question cannot be empty")

        return cleaned_data

    def save(self, request, commit=True):
        question = super().save(commit=False)
        question.author = request.user.profile
        tags = self.cleaned_data["tags"].split()

        if commit:
            question.save()
            for tag in tags:
                tags_by_name = Tag.objects.filter(name=tag)
                if tags_by_name.count() > 0:
                    question.tags.add(tags_by_name[0])
                else:
                    new_tag = Tag.objects.create(name=tag)
                    new_tag.save()
                    question.tags.add(new_tag)

        return question


class AnswerForm(forms.ModelForm):
    # tags = forms.CharField(widget=forms.TextInput(attrs={"class": "mb-3"}), label="Tags")

    class Meta:
        model = Answer
        fields = [ "text" ]

        labels = {
            "text": "Your answer"
        }

        widgets = {
            "text": forms.Textarea(attrs={"class": "mb-3"}),
        }


    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text", "")

        if text == "":
            self.add_error("text", "Answer cannot be empty")

        return cleaned_data

    def save(self, request, question_id, commit=True):
        author = Profile.objects.get(user=request.user)
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(text=self.cleaned_data["text"], question=question, author=author)
        # answer = super().save(commit=commit)

        if commit:
            answer.save()

        return answer
