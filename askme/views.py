from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.forms import model_to_dict
# from . import models
from .models import *
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required
from .forms import *
import django.contrib.auth as auth
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse, resolve


# Create your views here.

def get_page_obj(request, query_set, per_page=3):
    p = Paginator(query_set, per_page)

    page = request.GET.get("page")

    if page is None or page == "":
        page = 1

    try:
        page_obj = p.page(page)
    except InvalidPage:
        # page_obj = p.page(1)
        raise Http404("page not found")

    return page_obj


def index(request):
    page_obj = get_page_obj(request, Question.objects.top_likes())
    context = {
        "page_obj": page_obj,
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10]
    }

    return render(request, "index.html", context)


def hot(request):
    page_obj = get_page_obj(request, Question.objects.latest())
    context = {
        "page_obj": page_obj,
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10]
    }

    return render(request, "hot.html", context)


def tag(request, tag_name):
    page_obj = get_page_obj(request, Question.objects.by_tag_name(tag_name))
    context = {
        "page_obj": page_obj,
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "tag_name": tag_name
    }

    return render(request, "questions_tag.html", context)


def question(request, question_id):
    form = None
    print(f">>>>>>>>>>> QUESTION {request}")
    if request.method == "GET" and request.user.is_authenticated:
        form = AnswerForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        form = AnswerForm(request.POST)
        print(f">>>>>>>>>>> QUESTION FORM VALID {form.is_valid()}")
        if form.is_valid():
            answer = form.save(request, question_id)

            paginator = Paginator(Question.objects.get(id=question_id).answer_set.all(), 3)
            for i in paginator.page_range:
                page_obj = paginator.get_page(i)
                for item in page_obj.object_list:
                    if item.id == answer.id:
                        return redirect(f"{reverse('question', args=[question_id])}?page={i}")

    page_obj = get_page_obj(request, Question.objects.get(id=question_id).answer_set.all())

    context = {
        "question": Question.objects.get(id=question_id),
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "page_obj": page_obj,
        "form": form
    }
    print(f">>>>>>>>>>> QUESTION CONTEXT {context}")

    return render(request, "question.html", context)


def login(request):
    if request.user.is_authenticated:
        redir = request.GET.get("continue")
        if redir == "":
            redir = "index"
        return redirect(reverse(redir))

    form = LoginForm(request.POST)
    print(f"LOGIN REQUEST {request}")
    if request.method == "POST":
        print(f"FORM VALID {form.is_valid()}")
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                print(f"USER {user} AUTHENTICATED")
                redir = request.GET.get("continue")
                if redir is None or redir == "":
                    redir = "index"
                return redirect(reverse(redir))
            else:
                print(f"USER NOT AUTHENTICATED")
                form.add_error(None, "Invalid login data")
                form.add_error("username", "")
                form.add_error("password", "")

    context = {
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "form": form
    }
    return render(request, "login.html", context)


def signup(request):
    # if request.user.is_authenticated:
    #     redir = request.GET.get("continue")
    #     if redir == "":
    #         redir = "index"
    #     return redirect(reverse(redir))
    if request.method == "GET":
        form = SignupForm(request.POST)

    if request.method == "POST":
        form = SignupForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            redir = request.GET.get("continue")
            if redir is None or redir == "":
                redir = "index"
            return redirect(reverse(redir))

    context = {
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "form": form
    }
    return render(request, "reg.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def ask(request):
    print(f"ASK {request}")
    if request.method == "GET":
        form = QuestionForm()
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        print(f"ASK FORM VALID {form.is_valid()}")
        if form.is_valid():
            question = form.save(request)
            return redirect(reverse("question", args=[question.id]))


    context = {
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "form": form
    }
    return render(request, "add_question.html", context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(["GET", "POST"])
def settings(request):
    if request.method == "GET":
        form = SettingsForm(initial=model_to_dict(request.user))
    else:
        form = SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    context = {
        "popular_tags": Tag.objects.top_popular()[:10],
        "best_members": Profile.objects.top_answers()[:10],
        "form": form
    }
    return render(request, "settings.html", context)


# @login_required(login_url="login", redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    # return redirect(request.META.get("HTTP_REFERER"))
    redir = request.GET.get("continue")
    if redir is None or redir == "":
        redir = "index"
    return redirect(reverse(redir))


@require_POST
@login_required
def like_question(request):
    status = "ok"
    rating = 0
    if "question_id" in request.POST:
        question_id = request.POST.get("question_id")
        print(f"QUESTION LIKE id={question_id}")

        question = Question.objects.filter(id=question_id)
        if question.count() > 0:
            question = question[0]
            author_likes = question.questionlike_set.filter(author=request.user.profile)
            if author_likes.count() > 0:
                author_likes.delete()
                question.save()
                rating = question.rating()
                # like.delete()
                # status = "fail"
            else:
                like = QuestionLike.objects.create(question=question, author=request.user.profile, value=1)
                like.save()
                question.save()
                rating = question.rating()
        else:
            status = "fail"

    else:
        status = "fail"

    return JsonResponse({
        "status": status,
        "likes_count": rating
    })


@require_POST
@login_required
def check_answer(request):
    status = "ok"
    checked = False
    if "answer_id" in request.POST:
        answer_id = request.POST.get("answer_id")
        print(f"CHECK ANSWER id={answer_id}")

        answer = Answer.objects.filter(id=answer_id)
        if answer.count() > 0:
            answer = answer[0]

            if answer.question.author == request.user.profile:
                answer.is_true = not answer.is_true
                answer.save()
                checked = answer.is_true
            else:
                status = "fail"
        else:
            status = "fail"
    else:
        status = "fail"

    return JsonResponse({
        "status": status,
        "checked": checked
    })
