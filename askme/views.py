from django.http import HttpResponse
from django.shortcuts import render
from . import models


# Create your views here.

def index(request):
    return render(request, "index.html", {"questions": models.QUESTIONS})


def question(request, question_id):
    context = {"question": models.QUESTIONS[min(len(models.QUESTIONS) - 1, question_id)]}
    return render(request, "question.html", context)


def hot(request):
    return render(request, "hot.html", {"questions": models.QUESTIONS})


def tag(request, tag_name):
    return render(request, "questions_tag.html", {"questions": models.QUESTIONS, "tag_name": tag_name})


def login(request):
    return render(request, "authorization.html")


def signup(request):
    return render(request, "reg.html")


def ask(request):
    return render(request, "add_question.html")


def settings(request):
    return render(request, "settings.html")
