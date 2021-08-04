from django.urls import path
from . import views

urlpatterns = [
    path('player/<int:player_pk>', views.player_page_view, name='player-page'),
    path('team/<int:team_pk>', views.team_page_view, name='team-page'),
    path('schedule/', views.schedule_page_view, name="schedule-page"),
    ]