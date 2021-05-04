from django.urls import path
from . import views

urlpatterns = [
    path('',views.league_admin_roster_select, name='league-admin-roster-select'),
    ]