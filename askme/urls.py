from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("question/<int:question_id>", views.question, name="question"),
    path("hot/", views.hot, name="hot"),
    path("tag/<str:tag_name>", views.tag, name="tag"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("ask/", views.ask, name="ask"),
    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout, name="logout"),
    path("like_question/", views.like_question, name="like_question"),
    path("check_answer/", views.check_answer, name="check_answer"),

]