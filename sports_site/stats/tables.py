from django.db.models import F, Sum
import django_tables2 as tables
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats)
from .stat_calc import _calc_average, _convert_to_str

class ASPlayerHittingGameStatsTable(tables.Table):
    """Table used to display stats for given game on admin pages for editing
    stats. Omits Team"""
    class Meta:
        model = PlayerHittingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("player__player", "at_bats", "plate_appearances",
            "runs", "hits", "doubles", "triples", "homeruns", "runs_batted_in",
            "walks", "strikeouts", "stolen_bases", "caught_stealing", "average",
            "on_base_percentage", "slugging_percentage",
            "on_base_plus_slugging")


class ASPlayerPitchingGameStatsTable(tables.Table):
    """Table used to display stats for given game on admin pages for editing
    stats. Omits Team"""
    class Meta:
        model = PlayerPitchingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("player__player", "win", "loss", "era", "game", "game_started",
            "complete_game", "shutout", "save_converted", "save_op",
            "innings_pitched", "hits_allowed", "runs_allowed", "earned_runs",
            "homeruns_allowed", "hit_batters", "walks_allowed", "strikeouts",
            "whip")


class PlayerHittingStatsTable(tables.Table):
    """Table used to display stats for given game on admin pages for editing
    stats. Omits Team"""
    # average = tables.Column(empty_values=())
    class Meta:
        model = PlayerHittingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("first", "last", "at_bats", "plate_appearances",
            "runs", "hits", "doubles", "triples", "homeruns", "runs_batted_in",
            "walks", "strikeouts", "stolen_bases", "caught_stealing", 'average')


    def render_average(self, record):
        return _convert_to_str(record['average'])

    # def order_average(self, queryset, is_descending):
    #     queryset = queryset.annotate(
    #         average = F('hits') + F('at_bats')
    #         ).order_by(("-" if is_descending else "") + "average")

    #     return (queryset, True)
