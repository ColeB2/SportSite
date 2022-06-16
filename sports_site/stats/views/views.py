from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from league.models import League, SeasonStage
from ..decorators import user_owns_game
from ..filters import HittingSimpleFilter, PitchingSimpleFilter, StandingsSimpleFilter
from ..get_stats import (get_stats, get_extra_innings)
from ..models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameLineScore, TeamGameStats)
from ..tables import (ASPlayerHittingGameStatsTable,
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
        stage = (season_stage if season_stage
             else SeasonStage.objects.get(season__league=league, featured=True))
        qs = PlayerHittingGameStats.objects.filter(
            player__player__league=league,
            season=stage)
        hitting_stats = get_stats(qs, "all_season_hitting")
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
        stage = (season_stage if season_stage
             else SeasonStage.objects.get(season__league=league, featured=True))
        qs = PlayerPitchingGameStats.objects.filter(
            player__player__league=league,
            season=stage)
        pitching_stats = get_stats(qs, "all_season_pitching")
        return pitching_stats


class TeamHittingStatsView(SingleTableMixin, FilterView):
    model = PlayerHittingGameStats
    table_class = TeamHittingStatsTable
    template_name = "stats/team_stats_page.html"

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
        stage = (season_stage if season_stage
             else SeasonStage.objects.get(season__league=league, featured=True))
        qs = PlayerHittingGameStats.objects.filter(
            player__player__league=league,
            season=stage)
        hitting_stats = get_stats(qs, "team_season_hitting")
        return hitting_stats


class TeamPitchingStatsView(SingleTableMixin, FilterView):
    model = PlayerPitchingGameStats
    table_class = TeamPitchingStatsTable
    template_name = "stats/team_pitching_stats_page.html"

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
        stage = (season_stage if season_stage
             else SeasonStage.objects.get(season__league=league, featured=True))
        qs = PlayerPitchingGameStats.objects.filter(
            player__player__league=league,
            season=stage)
        pitching_stats = get_stats(qs, "team_season_pitching")
        return pitching_stats


"""Standings Display View"""
class StandingsView(SingleTableMixin, FilterView):
    model = TeamGameStats
    table_class = StandingsTable
    template_name = "stats/standings_page.html"

    filterset_class = StandingsSimpleFilter
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
        stage = (season_stage if season_stage
             else SeasonStage.objects.get(season__league=league, featured=True))
        qs = TeamGameStats.objects.filter(
            team__team__league=league,
            season=stage)
        standings_stats = get_stats(qs, "league_standings")
        return standings_stats
