from django.urls import path
from . import views
from .views import (
    ArticlesView, ArticleCreateView, ArticleEditView, ArticleDeleteView)

urlpatterns = [
    path('', views.home, name='news-home'),
    path('news/<slug:slug>', views.news_detail, name='news-detail'),
    path('news/', ArticlesView.as_view(), name='news-page'),
    path('news/create/article', ArticleCreateView.as_view(), name='news-create'),
    path('news/<slug:slug>/edit', ArticleEditView.as_view(), name='news-edit'),
    path('news/<slug:slug>/delete', ArticleDeleteView.as_view(), name='news-delete'),
]
