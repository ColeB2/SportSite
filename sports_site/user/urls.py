from django.urls import path
from . import views

urlpatterns = [
    path('',views.roster_select, name='roster-select'),
    path('<team>/<int:season>/<int:pk>/', views.roster_view, name='roster-view'),
    path('<team>/<int:season>/<int:pk>/edit/add/existing', views.roster_edit_add, name='roster-edit-add'),
    path('<team>/<int:season>/<int:pk>/edit/add/new', views.roster_edit_create, name='roster-edit-create'),
    path('<team>/<int:season>/<int:pk>/edit/remove', views.roster_edit_remove, name='roster-edit-remove'),
]