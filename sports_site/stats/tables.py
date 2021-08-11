import django_tables2 as tables
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameLineScore, TeamGameStats)
from .stat_calc import _convert_to_str

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
    """Table used to display stats for given game"""
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


class TeamGameLineScoreTable(tables.Table):
    """Table used to display linescore of a game."""
    def __init__(self, *args, **kwargs):
        """Checks if arg dict has more than min inning value (HARDCODED 9) and
        if it does, adds those values to base_columns using key as name (happens
        to equal to str number from min inning on...)
        ToDo: Find better solution. Works, as long as you don't open up an extra
        inning lienscore first.

        Currently args[0][0] len should be 10:
            9 innings
            1 R - total runs
            1 F - Final -- Team(s) involved
        """
        print(f"Boxscore Args: {args}")
        extras_len = len(args[0][0])
        non_inn_vals = 2
        if extras_len > 9+non_inn_vals:
            for i in range(9, extras_len-non_inn_vals):
                self.base_columns[str(i+1)] = tables.Column()
        else:
            for i in range(extras_len-non_inn_vals, len(self.base_columns)):
                self.base_columns.popitem()

        if args[0][0]["R"]:
            self.base_columns["R"] = tables.Column()
            self.base_columns.move_to_end("R")
        super(TeamGameLineScoreTable, self).__init__(*args, **kwargs)

    class Meta:
        model = TeamGameLineScore
        template_name = "django_tables2/bootstrap-responsive.html"

        fields = [
            "first", "second", "third", "fourth", "fifth", "sixth",
            "seventh","eighth", "ninth",
        ]


class StandingsTable(tables.Table):
    class Meta:
        model = TeamGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ["team_name", "win", "loss", "tie", "pct", "runs_for",
            "runs_against", "differential",]


    def render_win(self, record):
        return str(record['win'])


    def render_loss(self, record):
        return str(record['loss'])


    def render_tie(self, record):
        return str(record['tie'])


    def render_pct(self, record):
        return _convert_to_str(record['pct'])


class PlayerHittingGameStatsTable(tables.Table):
    """Table used to display stats for given game"""
    class Meta:
        model = PlayerHittingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("player__player", "at_bats", "plate_appearances",
            "runs", "hits", "doubles", "triples", "homeruns", "runs_batted_in",
            "walks", "strikeouts", "stolen_bases",  "caught_stealing",
            "hit_by_pitch", "sacrifice_flies")


class BattingOrderTable(tables.Table):
    """Table used to display stats for given game"""
    class Meta:
        model = PlayerHittingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("player__player", "at_bats", "runs", "hits", "runs_batted_in",
            "walks", "strikeouts",)




class PlayerPitchingGameStatsTable(tables.Table):
    """Table used to display pitching stats for given game"""
    class Meta:
        model = PlayerPitchingGameStats
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("player__player", "game_started","save_converted", "save_op",
            "innings_pitched", "hits_allowed", "runs_allowed", "earned_runs",
            "homeruns_allowed", "hit_batters", "walks_allowed", "strikeouts",
            )




