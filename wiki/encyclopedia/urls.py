from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/q", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random_article, name="random_article"),
    path("edit/edit", views.edit, name="edit"),
    path("edit/?article_title", views.edit, name="edit"),
    path("wiki/<str:article>", views.view_article, name="article"),
]
