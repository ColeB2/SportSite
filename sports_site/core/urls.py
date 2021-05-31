from django.urls import path
from . import views

urlpatterns = [
    # path('', views.roster_select, name='')
    path('', views.landing, name='landing')
    ]