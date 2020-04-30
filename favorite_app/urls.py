from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('create_book', views.create_book),
    path('books/<id>', views.edit_book),
    path('update_book/<id>', views.update_book),
    path('fav_book/<id>', views.fav_book),
    path('unfav_book/<id>', views.unfav_book),
    path('logout', views.logout)
    
]