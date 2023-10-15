from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article_name>", views.article, name="article"),
    path("search", views.search, name="search")
]
