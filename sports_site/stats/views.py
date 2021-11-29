from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import router
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin
from league.models import Game, League, Roster, SeasonStage, TeamSeason
from .decorators import user_owns_game
from .filters import HittingSimpleFilter, PitchingSimpleFilter
from .forms import (LinescoreEditForm, HittingGameStatsFormset,
    PitchingGameStatsFormset, PlayerPitchingStatsCreateForm,
    PlayerStatsCreateForm, PHGSFHelper, PPGSFHelper)
from .get_stats import (get_all_season_hitting_stats,
    get_all_season_pitching_stats, get_all_season_standings_stats,
    get_extra_innings, get_team_hitting_stats, get_team_pitching_stats)
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameLineScore, TeamGameStats)
from .tables import (ASPlayerHittingGameStatsTable,
    ASPlayerPitchingGameStatsTable, PlayerHittingStatsTable,
    PlayerPitchingStatsTable, StandingsTable, TeamGameLineScoreTable,
    TeamHittingStatsTable, TeamPitchingStatsTable)



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
"""Team Game Stats -- Pitching """
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
class StatsView(SingleTableMixin, FilterView):
    model = PlayerHittingGameStats
    table_class = PlayerHittingStatsTable
    template_name = "stats/stats_page.html"

    filterset_class = HittingSimpleFilter
    paginate_by = 25


    def dispatch(self, request, *args, **kwargs):
        self.league_slug = self.request.GET.get('league', None)

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['league'] = League.objects.get(url=self.league_slug)
        data['stage'] = SeasonStage.objects.get(season__league__url=self.league_slug,
            featured=True)
        return data


    def get_queryset(self):
        super().get_queryset()
        league = League.objects.get(url=self.league_slug)
        season_stage = self.request.GET.get("season", None)
        hitting_stats = get_all_season_hitting_stats(
            league,
            season_stage=season_stage)
        return hitting_stats


class PitchingStatsView(SingleTableMixin, FilterView):
    model = PlayerPitchingGameStats
    table_class = PlayerPitchingStatsTable
    template_name = "stats/pitching_stats_page.html"

    filterset_class = PitchingSimpleFilter
    paginate_by = 25


    def dispatch(self, request, *args, **kwargs):
        self.league_slug = self.request.GET.get('league', None)

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['league'] = League.objects.get(url=self.league_slug)
        data['stage'] = SeasonStage.objects.get(season__league__url=self.league_slug,
            featured=True)
        return data


    def get_queryset(self):
        super().get_queryset()
        league = League.objects.get(url=self.league_slug)
        season_stage = self.request.GET.get("season", None)
        pitching_stats = get_all_season_pitching_stats(
            league,
            season_stage=season_stage)
        return pitching_stats


def team_stats_display_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
    hitting_stats = get_team_hitting_stats(league, featured_stage)
    table = TeamHittingStatsTable(hitting_stats)
    RequestConfig(request).configure(table)

    context = {
        "league": league,
        "table": table,
        "featured_stage": featured_stage,
        }
    return render(request, "stats/team_stats_page.html", context)


def team_pitching_stats_display_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
    pitching_stats = get_team_pitching_stats(league, featured_stage)
    table = TeamPitchingStatsTable(pitching_stats)
    RequestConfig(request).configure(table)

    context = {
        "league": league,
        "table": table,
        "featured_stage": featured_stage,
        }
    return render(request, "stats/team_pitching_stats_page.html", context)


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
