from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..filters import RosterFilter, PlayerFilter
from ..forms import (SeasonCreateForm, SeasonStageCreateForm, TeamSelectForm,
    PlayerCreateForm, CreateGameForm, EditGameForm, EditPlayerForm)
from league.models import (League, Roster, Season, SeasonStage, Team, Game,
    TeamSeason, Player)



@login_required
def league_admin_dashboard_view(request):
    context = {}
    return render(request, "league_admin/dashboard.html",context)

@login_required
def league_admin_roster_select(request):
    league = League.objects.get(admin=request.user)
    f = RosterFilter(request.GET, queryset=Roster.objects.all().filter(team__team__league=league) )
    context = {
        'filter': f,
        }
    return render(request, "league_admin/roster_select.html", context)



