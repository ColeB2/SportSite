from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import (SeasonCreateForm, SeasonStageCreateForm, TeamSelectForm)
from league.models import (League, Season, SeasonStage, Team, TeamSeason)



@login_required
@permission_required('league.league_admin')
def league_admin_users_view(request):
    league = League.objects.get(admin=request.user)
    teams = Team.objects.all().filter(league=league)

    context = {
        'league':league,
        'teams':teams,
        }
    return render(request, "league_admin/users_page.html", context)
