
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow_view, name="follow"),
    path("unfollow/<str:username>", views.unfollow_view, name="unfollow"),
    path("following", views.following_posts_view, name="following_posts"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like_view, name="like"),
]
