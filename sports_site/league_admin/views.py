from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.forms import (PlayerSelectForm, PlayerCreateForm, PlayerSeasonForm, PlayerDeleteForm,
    RosterCreateForm)

from django.forms import formset_factory, modelformset_factory
from league.models import Roster, PlayerSeason, Player, Team, TeamSeason, SeasonStage

# Create your views here.

@login_required
def league_admin_roster_select(request):
    roster = Roster.objects.all()
    context = {
        'rosters': roster,
        }
    return render(request, "league_admin/roster_select.html", context)
