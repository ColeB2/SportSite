from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from league.models import Game, Roster, TeamSeason
from ..decorators import user_owns_game
from ..forms import HittingGameStatsFormset, PlayerStatsCreateForm, PHGSFHelper
from ..models import TeamGameStats



@permission_required('league.league_admin')
@user_owns_game
def team_game_stats_create_view(request, game_pk, team_season_pk,
                                team_game_stats_pk):

    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk,
                                                season=team_season.season,
                                                team=team_season,
                                                game=game)

    StatsFormset = formset_factory(form=PlayerStatsCreateForm,
                                   extra=len(players))

    formset = StatsFormset(data=request.POST or None,
                           files=request.FILES or None,
                           form_kwargs={'team_season':team_season,
                                        'team_game_stats':team_game_stats})

    if request.method == "POST":
        for form in formset:
            if form.is_valid():
                hitting_stats, created = form.process()

                if created:
                    messages.success(request,
                        f"{hitting_stats.player.player} hitting stats "
                        f"created for {game}")
                else:
                    if hitting_stats:
                        messages.info(request,
                            f"{hitting_stats.player.player} already has "
                            f"stats for {game}.")



        if 'create' in request.POST:
            return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/game_stats_create.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_stats_edit_view(request, game_pk, team_season_pk,
                              team_game_stats_pk):

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
                         'game_stats':team_game_stats})
        if formset.is_valid():
            for form in formset:
                saved_stats = form.process()
                messages.success(request, f"{saved_stats} saved.")

            return redirect('stats-team-game-stats', game_pk, team_season_pk)

    else:
        formset = HittingGameStatsFormset(
            instance=team_game_stats,
            form_kwargs={'team_season':team_season,
                         'game_stats':team_game_stats})
    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        "helper": helper,
        }
    return render(request, "stats/game_stats_edit.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_stats_delete_info_view(request, game_pk, team_season_pk,
                                     team_game_stats_pk):

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)
    hitting_stats = game_stats.playerhittinggamestats_set.all()

    if request.method == 'POST':
        for stat_obj in hitting_stats:
            stat_obj.delete()

            messages.success(request,
                f"{stat_obj} and all releated "
                f"object were deleted")

        return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats": game_stats,
        "hitting_stats": hitting_stats,
        }
    return render(request, "stats/game_stats_delete.html", context)