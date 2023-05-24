from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TagManager(models.Manager):
    def top_popular(self):
        return self.all().annotate(rating=models.Count("question")).order_by("-rating")


class ProfileManager(models.Manager):
    def top_answers(self):
        return self.all().annotate(rating=models.Count("answer")).order_by("-rating")


class QuestionManager(models.Manager):
    def top_likes(self):
        return self.all().annotate(rating=
                                   models.Count("questionlike",
                                                filter=models.Q(questionlike__value=QuestionLike.Choices.LIKE))
                                   - models.Count("questionlike",
                                                  filter=models.Q(questionlike__value=QuestionLike.Choices.DISLIKE))
                                   ).order_by("-rating")

    def latest(self):
        return self.all().order_by("-creation_date")

    def by_tag_name(self, tag_name):
        return Tag.objects.get(name=tag_name).question_set.all()


class AnswerManager(models.Manager):
    def top_likes(self, question):
        return self.all().filter(question=question).annotate(
            rating=
            models.Count("answerlike", filter=models.Q(answerlike__value=AnswerLike.Choices.LIKE))
            - models.Count("answerlike", filter=models.Q(answerlike__value=AnswerLike.Choices.DISLIKE))
        ).order_by("-rating")


class Question(models.Model):
    header = models.CharField(max_length=80)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    # rating

    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")

    objects = QuestionManager()

    def __str__(self):
        return f"{self.header} | {self.author.user.username}"

    def rating(self):
        return self.questionlike_set.filter(value=QuestionLike.Choices.LIKE).count() \
               - self.questionlike_set.filter(value=QuestionLike.Choices.DISLIKE).count()


class Answer(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_true = models.BooleanField(default=False)
    # rating

    objects = AnswerManager()

    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.user.username}"

    # def rating(self):
    #     return self.answerlike_set.filter(value=AnswerLike.Choices.LIKE).count() \
    #            - self.answerlike_set.filter(value=AnswerLike.Choices.DISLIKE).count()


class QuestionLike(models.Model):
    class Choices(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    value = models.IntegerField(choices=Choices.choices)

    def __str__(self):
        return f"{'LIKE' if self.value == 1 else 'DISLIKE'} |" \
               f" {self.author.user.username} | to {self.question.id}"


class AnswerLike(models.Model):
    class Choices(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    value = models.IntegerField(choices=Choices.choices)

    def __str__(self):
        return f"{'LIKE' if self.value == 1 else 'DISLIKE'} |" \
               f" {self.author.user.username} | to {self.answer.id}"


class Tag(models.Model):
    name = models.CharField(max_length=32)

    objects = TagManager()

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    # nickname = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255)
    avatar = models.ImageField(upload_to='media/', default='media/default-avatar.jpg')

    # registration_date = models.DateTimeField()

    objects = ProfileManager()

    # rating

    def __str__(self):
        return f"{self.user.username}"
