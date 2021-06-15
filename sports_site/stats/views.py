from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from league.models import Game, TeamSeason, Roster
from .models import PlayerHittingGameStats
from .forms import (PlayerHittingGameStatsForm)

# Create your views here.
def add_game_stats_view(request, game_pk, team_season_pk):
    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    StatsFormset = modelformset_factory(PlayerHittingGameStats,
        form=PlayerHittingGameStatsForm, extra=len(players)-7)
    formset = StatsFormset(data=request.POST or None,
        form_kwargs={'team_season_pk':team_season_pk})

    if request.method == "POST":
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    pass

    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/add_game_stats.html", context)


def select_games_view(request, season_stage_pk):
    pass