from django.urls import path
from . import views

urlpatterns = [
    path('player/<int:player_pk>', views.player_page_view, name='player-page'),
    path('schedule/', views.schedule_view, name="schedule-page"),
    ]