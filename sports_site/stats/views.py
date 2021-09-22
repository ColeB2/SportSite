from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import router
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from league.models import Game, League, Roster, TeamSeason, SeasonStage
from .get_stats import (get_all_season_hitting_stats,
    get_all_season_standings_stats, get_extra_innings)
from .models import (TeamGameLineScore, TeamGameStats,)
from .forms import (LinescoreEditForm, HittingGameStatsFormset,
    PitchingGameStatsFormset, PlayerPitchingStatsCreateForm,
    PlayerStatsCreateForm, PHGSFHelper, PPGSFHelper)
from .decorators import user_owns_game
from .tables import (ASPlayerHittingGameStatsTable,
    ASPlayerPitchingGameStatsTable, PlayerHittingStatsTable, StandingsTable,
    TeamGameLineScoreTable)




@permission_required('league.league_admin')
@user_owns_game
def team_game_stats_info_view(request, game_pk, team_season_pk):
    game_stats = TeamGameStats.objects.get(team__pk=team_season_pk,
                                           game__pk=game_pk)
    player_stats = game_stats.playerhittinggamestats_set.all()
    pitching_stats = game_stats.playerpitchinggamestats_set.all()
    table = ASPlayerHittingGameStatsTable(player_stats)
    table2 = ASPlayerPitchingGameStatsTable(pitching_stats)

    try:
        linescore = TeamGameLineScore.objects.get(game=game_stats,
                                                  game__team=team_season_pk)
        table_data = [get_extra_innings(linescore)]
        table3 = TeamGameLineScoreTable(table_data)
    except ObjectDoesNotExist:
        linescore = None
        table3 = None
        table_data = None

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats":game_stats,
        "player_stats":player_stats,
        "pitching_stats":pitching_stats,
        "table": table,
        "table2":table2,
        "table3": table3,
        "linescore": linescore,
        }
    return render(request, "stats/game_stats_info.html", context)


"""Team Game Stats -- Hitting"""
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
                    messages.info(request,
                        f"{hitting_stats.player.player} already has "
                        f"stats for {game}.")



        if 'create' in request.POST:
            return redirect('stats-team-game-stats', game_pk, team_season_pk)
        elif 'create-and-continue' in request.POST:
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
            f"{hitting_stats} and all releated "
            f"object were deleted")

        return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats": game_stats,
        "hitting_stats": hitting_stats,
        }
    return render(request, "stats/game_stats_delete.html", context)


"""Team Game Stats -- Pitching """
@permission_required('league.league_admin')
@user_owns_game
def team_game_pitching_stats_create_view(request, game_pk, team_season_pk,
                                team_game_stats_pk):

    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk,
                                                season=team_season.season,
                                                team=team_season,
                                                game=game)

    StatsFormset = formset_factory(form=PlayerPitchingStatsCreateForm,
                                   extra=len(players))

    formset = StatsFormset(data=request.POST or None,
                           files=request.FILES or None,
                           form_kwargs={'team_season':team_season,
                                        'team_game_stats':team_game_stats})

    if request.method == "POST":
        for form in formset:
            if form.is_valid():
                pitching_stats, created = form.process()

                if created:
                    messages.success(request,
                        f"{pitching_stats.player.player} pitching stats "
                        f"created for {game}")
                else:
                    messages.info(request,
                        f"{pitching_stats.player.player} already has "
                        f"stats for {game}.")



        if 'create' in request.POST:
            return redirect('stats-team-game-stats', game_pk, team_season_pk)
        elif 'create-and-continue' in request.POST:
            return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game":game,
        "team_season":team_season,
        "roster": roster,
        "players": players,
        "formset": formset,
        }
    return render(request, "stats/game_pitching_stats_create.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_pitching_stats_edit_view(request, game_pk, team_season_pk,
                                       team_game_stats_pk):

    game = Game.objects.get(pk=game_pk)
    team_season = TeamSeason.objects.get(pk=team_season_pk)
    roster = Roster.objects.get(team=team_season)
    players = roster.playerseason_set.all()

    team_game_stats= TeamGameStats.objects.get(pk=team_game_stats_pk,
                                               season=team_season.season,
                                               team=team_season,
                                               game=game)

    helper = PPGSFHelper()

    if request.method == "POST":
        formset = PitchingGameStatsFormset(
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
        formset = PitchingGameStatsFormset(
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
    return render(request, "stats/game_pitching_stats_edit.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_pitching_stats_delete_info_view(request, game_pk, team_season_pk,
                                              team_game_stats_pk):

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)
    pitching_stats = game_stats.playerpitchinggamestats_set.all()

    if request.method == 'POST':
        for stat_obj in pitching_stats:
            stat_obj.delete()
        messages.success(request,
            f"{pitching_stats} and all releated object were deleted")

        return redirect('stats-team-game-stats', game_pk, team_season_pk)
    else:
        pass

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats": game_stats,
        "pitching_stats": pitching_stats,
        }
    return render(request, "stats/game_pitching_stats_delete.html", context)



"""Linescore Views"""
@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_create_view(request, game_pk, team_season_pk,
                                    team_game_stats_pk):
    """View which creates a linescore model and if one doesn't exist and
    immediately redirects to  team game stats info view"""

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)

    linescore, created = TeamGameLineScore.objects.get_or_create(game=game_stats)
    if created:
        linescore.save()
        messages.success(request, f"{linescore} created.")
    else:
        messages.info(request, f"{linescore} already exists.")

    return redirect("stats-team-game-stats", game_pk, team_season_pk)


@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_edit_view(request, game_pk, team_season_pk,
                                  team_game_stats_pk, linescore_pk):

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)

    try:
        linescore = TeamGameLineScore.objects.get(game=game_stats,
                                                  game__team=team_season_pk)
    except ObjectDoesNotExist:
        linescore = None

    if request.method == "POST":
        form = LinescoreEditForm(data=request.POST,
                                 files=request.FILES,
                                 instance=linescore)
        if form.is_valid:
            linescore_save = form.process()
            messages.success(request, f"{linescore_save} saved.")
        return redirect("stats-team-game-stats", game_pk, team_season_pk)
    else:
        form = LinescoreEditForm(instance=linescore)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats":game_stats,
        "linescore": linescore,
        "form":form,
        }
    return render(request, "stats/game_linescore_create.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_delete_info_view(request, game_pk, team_season_pk,
                                         team_game_stats_pk, linescore_pk):
    linescore = TeamGameLineScore.objects.get(pk=linescore_pk)


    using = router.db_for_write(linescore._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([linescore])

    if request.method == 'POST':
        linescore.delete()
        messages.success(request,
            f"{linescore} and all releated object were deleted")

        return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "linescore": linescore,
        "nested_object": nested_object,
        }
    return render(request, "stats/game_linescore_delete.html", context)


"""Stats Display Views"""
def stats_display_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
    hitting_stats = get_all_season_hitting_stats(league, featured_stage)
    table = PlayerHittingStatsTable(hitting_stats)
    RequestConfig(request).configure(table)

    context = {
        "league": league,
        "table": table,
        "featured_stage": featured_stage,
        }
    return render(request, "stats/stats_page.html", context)


"""Standings Display View"""
def standings_display_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
    standings_stats = get_all_season_standings_stats(league, featured_stage)
    table = StandingsTable(standings_stats)
    RequestConfig(request).configure(table)

    context = {
        "league": league,
        "table": table,
        "featured_stage": featured_stage,
    }
    return render(request, "stats/standings_page.html", context)
