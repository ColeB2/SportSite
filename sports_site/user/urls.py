from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard_view, name='user-dashboard'),
    path('roster-select',views.roster_select, name='roster-select'),
    path('<team_name>/<int:season>/<int:roster_pk>/', views.roster_view, name='user-roster-view'),
    path('<team_name>/<int:season>/<int:roster_pk>/edit/copy', views.roster_edit_copy, name='roster-edit-copy'),
    path('<team_name>/<int:season>/<int:roster_pk>/edit/add/existing', views.roster_edit_add, name='roster-edit-add'),
    path('<team_name>/<int:season>/<int:roster_pk>/edit/add/new', views.roster_edit_create, name='roster-edit-create'),
    path('<team_name>/<int:season>/<int:roster_pk>/edit/remove', views.roster_edit_remove, name='roster-edit-remove'),
    path('<team_name>/<int:season>/<int:roster_pk>/edit/remove/<int:playerseason_pk>/info', views.roster_playerseason_delete_info, name='roster-edit-delete-playerseason'),
    path('<team_name>/create/', views.roster_create, name='roster-create'),
    path('<team_name>/<int:season_year>/<int:roster_pk>/delete', views.roster_delete_info_view, name='roster-delete'),
]