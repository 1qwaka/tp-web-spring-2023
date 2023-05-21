from django.http import HttpResponse, Http404
from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, InvalidPage


# Create your views here.

def index(request):
    p = Paginator(models.QUESTIONS, 3)

    page = request.GET.get("page")

    if page is None:
        page = 1

    try:
        page_obj = p.page(page)
    except InvalidPage:
        page_obj = p.page(1)

    return render(request, "index.html", {"page_obj": page_obj})


def hot(request):
    p = Paginator(models.QUESTIONS, 3)

    page = request.GET.get("page")

    if page is None:
        page = 1

    try:
        page_obj = p.page(page)
    except InvalidPage:
        page_obj = p.page(1)

    return render(request, "hot.html", {"page_obj": page_obj})


def tag(request, tag_name):
    p = Paginator(models.QUESTIONS, 3)

    page = request.GET.get("page")

    if page is None:
        page = 1

    try:
        page_obj = p.page(page)
    except InvalidPage:
        page_obj = p.page(1)


    return render(request, "questions_tag.html", {"page_obj": page_obj, "tag_name": tag_name})


def question(request, question_id):
    context = {"question": models.QUESTIONS[min(len(models.QUESTIONS) - 1, question_id)]}
    return render(request, "question.html", context)



def login(request):
    return render(request, "authorization.html")


def signup(request):
    return render(request, "reg.html")


def ask(request):
    return render(request, "add_question.html")


def settings(request):
    return render(request, "settings.html")


def paginate(objects_list, request, per_page=10):
    # do smth with Paginator, etc…
    return page