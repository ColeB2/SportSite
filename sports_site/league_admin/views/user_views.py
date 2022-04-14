from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Permission
from django.shortcuts import render, redirect
from ..forms import (EditUserRosterPermissionsForm)
from league.models import (League, Team, Roster)


"""Currently DEPRECATED"""

@permission_required('league.league_admin')
def league_admin_users_view(request):
    league = League.objects.get(admin=request.user)
    teams = Team.objects.all().filter(league=league)

    context = {
        'league':league,
        'teams':teams,
        }
    return render(request, "league_admin/user_templates/users_page.html",
                  context)


@permission_required('league.league_admin')
def league_admin_user_info_view(request, user_name, user_pk):
    user_viewed = User.objects.get(pk=user_pk)
    team = Team.objects.get(owner=user_viewed, league__admin=request.user)

    context = {
        'user_viewed': user_viewed,
        'team': team,
        }
    return render(request, "league_admin/user_templates/user_info.html",
                  context)


@permission_required('league.league_admin')
def league_admin_user_edit_perms_view(request, user_name, user_pk):
    user_viewed = User.objects.get(pk=user_pk)
    team = Team.objects.get(owner=user_viewed, league__admin=request.user)

    roster_permissions = Permission.objects.filter(
        content_type__app_label=Roster._meta.app_label,
        content_type__model=Roster._meta.model_name,
        codename__contains='user')
    user_permissions = Permission.objects.filter(user__pk=user_pk)

    if request.method =="POST":
        form = EditUserRosterPermissionsForm(data=request.POST,
                                             selected_user=user_viewed)
        if form.is_valid():
            if form.has_changed():
                form.process()
                messages.success(request,
                                 f"{user_viewed}'s permissions updated.")
        return redirect('league-admin-user-info', user_name, user_pk)
    else:
        form = EditUserRosterPermissionsForm(selected_user=user_viewed)

    context = {
        'user_viewed': user_viewed,
        'team': team,
        'form':form,
        'roster_permissions': roster_permissions,
        'user_perms': user_permissions,
        }
    return render(request, "league_admin/user_templates/user_edit_perms.html",
                  context)

