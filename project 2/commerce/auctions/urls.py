from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categorylist", views.categorylist, name="categorylist"),
    path("category/<str:category>", views.categoryitem, name="categoryitem"),
    path("create", views.create, name="create"),
    path("submitlist", views.submitlist, name="submitlist"),
    path("listing/<int:id>", views.listingpage, name="listingpage"),
    path("removewatchlist/<int:listid>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:listid>", views.addwatchlist, name="addwatchlist"),
    path("submitbid/<int:listid>", views.submitbid, name="submitbid"),
    path("closebid/<int:listid>", views.closebid, name="closebid"),
    path("submitcomment/<int:listid>", views.submitcomment, name="submitcomment"),
    path("watchlist/<str:username>", views.watchlistpage, name="watchlistpage"),
    path("mywinning", views.mywinning, name="mywinning")
]
