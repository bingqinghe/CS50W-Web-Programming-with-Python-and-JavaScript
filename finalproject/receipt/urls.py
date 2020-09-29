from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("welcome", views.welcome, name="welcome"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register_view, name="register"),
	path("user", views.profile_view, name="user"),
	path("user/<int:user_id>", views.profile_view, name="user"),
	path("search", views.search, name="search"),
	path("following/<int:user_id>", views.following_view, name="following"),
	path("followers/<int:user_id>", views.followers_view, name="followers"),
	path("post/<post_id>", views.post, name="post"),
	path("follow", views.addfollow, name="follow"),
	path("like", views.addlike, name='like'),
	path("comment", views.addcomment, name='comment'),
	path("profile", views.profile_photo, name='profile'),
	path("upload", views.upload, name='upload')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)