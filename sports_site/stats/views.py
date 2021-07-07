from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.forms.models import modelformset_factory
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from league.models import Game, TeamSeason, Roster
from .models import (PlayerHittingGameStats, TeamGameStats,
    PlayerPitchingGameStats)
from .forms import (PlayerHittingGameStatsForm, PlayerStatsCreateForm, PHGSFHelper,
    HittingGameStatsFormset)
from .decorators import user_owns_game

from .tables import ASPlayerHittingGameStatsTable
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView

# Create your views here.
@permission_required('league.league_admin')
@user_owns_game
def team_game_stats_create_view(request, game_pk, team_season_pk):
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
                hitting_stats, h_created, pitching_stats, p_created, pitched = form.process()
                if h_created:
                    messages.success(request, f"{hitting_stats.player.player} hitting stats created for {game}")
                else:
                    if hitting_stats:
                        messages.info(request, f"{hitting_stats.player.player} already has stats for {game}.")
                if p_created:
                    messages.success(request, f"{pitching_stats.player.player} pitching stats created for {game}")
                else:
                    if pitching_stats and pitched:
                        messages.info(request, f"{pitching_stats.player} already has pitching stats for {game}.")


        if 'create' in request.POST:
            return redirect('league-admin-schedule', team_season.season.season.year, team_season.season.pk)
        elif 'create-and-continue' in request.POST:
            return redirect('stats-add-game-stats', game_pk, team_season_pk)

    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/game_stats_create.html", context)


def team_game_stats_edit_view(request, game_pk, team_season_pk):
    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats, created = TeamGameStats.objects.get_or_create(
            season=team_season.season, team=team_season, game=game)
    helper = PHGSFHelper()

    if request.method == "POST":
        formset = HittingGameStatsFormset(
        instance=team_game_stats,
        data=request.POST,
        files=request.FILES,
        form_kwargs={'team_season':team_season,
                     'team_game_stats':team_game_stats})
        if formset.is_valid():
            for form in formset:
                saved_stats = form.process()
                messages.success(request, f"{saved_stats} saved.")
            return redirect('league-admin-schedule', team_season.season.season.year, team_season.season.pk)
    else:
        formset = HittingGameStatsFormset(
        instance=team_game_stats,
        form_kwargs={'team_season':team_season,
                     'team_game_stats':team_game_stats})
    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        "helper": helper,
        }
    return render(request, "stats/game_stats_edit.html", context)


def team_game_stats_info_view(request, game_pk, team_season_pk):
    game_stats = TeamGameStats.objects.get(team__pk=team_season_pk, game__pk=game_pk)
    player_stats = game_stats.playerhittinggamestats_set.all()
    pitching_stats = game_stats.playerpitchinggamestats_set.all()
    table = ASPlayerHittingGameStatsTable(player_stats)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats":game_stats,
        "player_stats":player_stats,
        "pitching_stats":pitching_stats,
        "table": table,
        }

    return render(request, "stats/game_stats_info.html", context)

class team_game_stats_info_view2(SingleTableView):
    pass


def select_games_view(request, season_stage_pk):
    pass