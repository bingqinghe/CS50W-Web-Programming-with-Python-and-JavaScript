from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("writepost", views.writepost, name="writepost"),
    path("submitpost", views.submitpost, name="submitpost"),
    path("profile/<str:urname>", views.profile, name="profile"),
    path("follow/<str:name>", views.follow, name="followuser"),
    path("unfollow/<str:name>", views.unfollow, name="unfollowuser"),
    path("followposts", views.followposts, name="followposts"),
    path("postapi/<int:postid>", views.postapi, name="postapi"),
    path("likeapi/<int:postid>", views.likeapi, name="likeapi"),
    path("followapi/<str:name>", views.followapi, name="followapi")
]
