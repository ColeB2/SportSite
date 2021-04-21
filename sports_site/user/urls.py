from django.urls import path
from . import views

from .views import RosterView #test

urlpatterns = [
    path('',views.roster_select, name='roster-select'),
    path('<team>/<int:season>/<int:pk>/', views.roster_view, name='roster-view'),
    path('<team>/<int:season>/<int:pk>/edit', views.roster_edit, name='roster-edit'),
    path('roster/<int:pk>', RosterView.as_view(), name='team-roster-page'),
]