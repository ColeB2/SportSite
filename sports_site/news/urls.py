from django.urls import path
from . import views
from .views import (
    ArticlesView)

urlpatterns = [
    path('', views.home, name='news-home'),
    path('news/<int:pk>', views.news_detail, name='news-detail'),
    # path('news/', views.news_page, name='news-page'),
    path('news/', ArticlesView.as_view(), name='news-page'),
]
