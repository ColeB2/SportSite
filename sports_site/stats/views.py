from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.forms.models import modelformset_factory
from django.forms import formset_factory
from django.shortcuts import render, redirect
from league.models import Game, TeamSeason, Roster
from .models import PlayerHittingGameStats, TeamGameStats
from .forms import (PlayerHittingGameStatsForm, PlayerStatsCreateForm)
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.
def create_team_game_stats_view(request, game_pk, team_season_pk):
    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats, created = TeamGameStats.objects.get_or_create(
            season=team_season.season, team=team_season, game=game)

    StatsFormset = formset_factory(form=PlayerStatsCreateForm, extra=len(players))

    formset = StatsFormset(data=request.POST or None,
                           files=request.FILES or None,
                           form_kwargs={'team_season':team_season,
                                        'team_game_stats':team_game_stats})

    if request.method == "POST":
        for form in formset:
            if form.is_valid():
                new_stats = form.process()
                if new_stats:
                    messages.success(request, f"{new_stats} created for {game}")

        return redirect('league-admin-schedule', team_season.season.season.year, team_season.season.pk)


    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/game_stats_create.html", context)

def add_game_stats_view(request, game_pk, team_season_pk):
    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats, created = TeamGameStats.objects.get_or_create(
            season=team_season.season, team=team_season, game=game)

    player_stats = team_game_stats.playerhittinggamestats_set.all()


    StatsFormset = modelformset_factory(PlayerHittingGameStats,
        form=PlayerHittingGameStatsForm, extra=len(players)-len(player_stats))
    formset = StatsFormset(queryset=player_stats, data=request.POST or None,
        files=request.FILES or None,
        form_kwargs={'team_season':team_season,
                     'team_game_stats':team_game_stats})

    if request.method == "POST":
        for form in formset:
            if form.is_valid():
                new_hitting_stats = form.process()
                if new_hitting_stats:
                    messages.success(request, f"{new_hitting_stats} created for {game}")

        return redirect('league-admin-schedule', team_season.season.season.year, team_season.season.pk)

    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/game_stats_add.html", context)

def game_stats_info_view(request, game_pk, team_season_pk, team_game_pk):
    game_stats = TeamGameStats.objects.get(pk=team_game_pk)
    player_stats = game_stats.playerhittinggamestats_set.all()

    context = {
        "game_stats":game_stats,
        "player_stats":player_stats,
        }

    return render(request, "stats/game_stats_info.html", context)


class PlayerHittingStatsCreateView(CreateView):
    template_name = 'stats/add_game_stats.html'
    model = PlayerHittingGameStats
    form_class = PlayerHittingGameStatsForm


def select_games_view(request, season_stage_pk):
    pass