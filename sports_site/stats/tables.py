import django_tables2 as tables
from .models import PlayerHittingGameStats, TeamGameStats
from league.models import Player, TeamSeason, Game

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