from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path("games", views.game_all),
    path("games/create", views.create_game),
    path("games/<int:game_id>", views.show_one),
    path("games/<int:game_id>/update", views.update),
    path("games/<int:game_id>/delete", views.delete),
    path("favorite/<int:game_id>", views.favorite),
    path("unfavorite/<int:game_id>", views.unfavorite),
    path("logout", views.logout)


]