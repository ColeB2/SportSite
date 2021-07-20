from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db import router
from django.shortcuts import render, redirect
from ..forms import (TeamCreateForm)
from ..decorators import user_owns_team
from league.models import (Team, TeamSeason)



@permission_required('league.league_admin')
def league_admin_team_create_view(request):
    league = request.user.userprofile.league
    league_users = User.objects.all().filter(userprofile__league=league)

    if request.method == 'POST':
        form = TeamCreateForm(data=request.POST)
        form.fields['owner'].queryset=league_users
        if form.is_valid():
            new_team = form.process(league=league)
            messages.success(request, f"{new_team} created.")

        # next=request.POST.get('next', '/')
        # return HttpResponseRedirect(next)
        return redirect('league-admin-dashboard')

    else:
        form = TeamCreateForm()
        form.fields['owner'].queryset=league_users
    context = {
        "form": form,
        "lu":league_users
    }
    return render(request, "league_admin/team_create.html", context)


@permission_required('league.league_admin')
def league_admin_team_select_view(request):
    league = request.user.userprofile.league
    teams = Team.objects.all().filter(league=league)

    context = {
        "teams":teams
    }
    return render(request, "league_admin/team_select.html",context)


@permission_required('league.league_admin')
@user_owns_team
def league_admin_team_info_view(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    team_seasons = TeamSeason.objects.all().filter(team=team)

    context = {
        "team":team,
        "team_seasons": team_seasons,
    }
    return render(request, "league_admin/team_page.html",context)


@permission_required('league.league_admin')
@user_owns_team
def league_admin_team_delete_info_view(request, team_pk):
    team = Team.objects.get(pk=team_pk)

    using = router.db_for_write(team._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([team])

    if request.method == 'POST':
        team.delete()
        messages.success(request, f"{team} and all releated object were deleted")
        return redirect('league-admin-team-select')
    else:
        pass

    context = {
        'team':team,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/team_delete.html", context)