from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article_name>", views.article, name="article"),
    path("search", views.search, name="search"),
    path("results", views.results, name="results"),
    path("newpage", views.new_page, name="newpage"),
    path('wiki/<str:article_name>/edit/', views.edit_article, name='edit_article'),
]
