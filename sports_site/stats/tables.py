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
    class Meta:
        model = PlayerHittingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("first", "last", "at_bats", "plate_appearances",
            "runs", "hits", "doubles", "triples", "homeruns", "runs_batted_in",
            "walks", "strikeouts", "stolen_bases",  "caught_stealing",
            "hit_by_pitch", "sacrifice_flies", "average", "on_base_percentage")


    def render_average(self, record):
        return _convert_to_str(record['average'])

    def render_on_base_percentage(self, record):
        return _convert_to_str(record['on_base_percentage'])
