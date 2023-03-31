from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/q", views.search, name="search"),
    path("new", views.new, name="new"),
    path("<str:article>", views.view_article, name="article"),
]
