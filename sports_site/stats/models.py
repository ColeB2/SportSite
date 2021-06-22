from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from league.models import PlayerSeason, TeamSeason, SeasonStage, Game
import datetime
from .stat_calc import (_calc_average, _calc_obp, _calc_slugging, _calc_ops,
    _calc_win_pct, _calc_whip, _calc_era)


class PlayerHittingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


class PlayerPitchingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


"""Game Related Models"""
class TeamGameStats(models.Model):
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.game} Game Stats"


    def save(self, *args, **kwargs):
        self.season = self.team.season
        super(TeamGameStats,self).save(*args, **kwargs)


class PlayerHittingGameStats(models.Model):
    team_stats = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)

    at_bats = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="AB")
    plate_appearances = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="PA")
    hits = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="H")
    runs = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="R")
    strikeouts = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SO")
    walks = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="BB")
    singles = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="1B")
    doubles = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="2B")
    triples = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="3B")
    homeruns = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="HR")
    stolen_bases = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SB")
    caught_stealing = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="CS")
    runs_batted_in = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="RBI")
    hit_by_pitch = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="HBP")
    sacrifice_flies = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SF")
    sacrifice_bunts = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SAC")
    average = models.FloatField(null=True, blank=True, verbose_name="AVG")
    on_base_percentage = models.FloatField(null=True, blank=True, verbose_name="OBP")
    slugging_percentage = models.FloatField(null=True, blank=True, verbose_name="SLG")
    on_base_plus_slugging = models.FloatField(null=True, blank=True, verbose_name="OPS",  help_text=f"On-Base Plus Slugging\nCombined rate of OBP and SLG.\nOBP+SLG")
    reached_on_error = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="ROE")
    fielders_choice = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="FC")


    class Meta:
        verbose_name = "Hitter's Game Stats"
        verbose_name_plural = "Hitter's Game Stats"


    def __str__(self):
        return f"{self.player}"


    def save(self, *args, **kwargs):
        self.game = self.team_stats.game
        self.season = self.team_stats.season
        self.hits = (self.singles + self.doubles + self.triples + self.homeruns)
        self.average = _calc_average(self.hits, self.at_bats)
        self.on_base_percentage = _calc_obp(self.hits, self.walks, self.hit_by_pitch, self.at_bats, self.sacrifice_flies)
        self.slugging_percentage = _calc_slugging(self.singles, self.doubles, self.triples, self.homeruns, self.at_bats)
        self.on_base_plus_slugging = _calc_ops(self.on_base_percentage, self.slugging_percentage)
        super(PlayerHittingGameStats, self).save(*args , **kwargs)


class PlayerPitchingGameStats(models.Model):
    team_stats = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)

    wins = models.IntegerField(null=True, blank=True, default=0, verbose_name="W")
    losses = models.IntegerField(null=True, blank=True, default=0, verbose_name="L")
    games = models.IntegerField(null=True, blank=True, default=0, verbose_name="G")
    games_started = models.IntegerField(null=True, blank=True, default=0, verbose_name="GS")
    complete_games = models.IntegerField(null=True, blank=True, default=0, verbose_name="CG")
    shutouts = models.IntegerField(null=True, blank=True, default=0, verbose_name="SHO")
    saves = models.IntegerField(null=True, blank=True, default=0, verbose_name="SV")
    save_ops = models.IntegerField(null=True, blank=True, default=0, verbose_name="SVO")
    innings_pitched = models.IntegerField(null=True, blank=True, default=0, verbose_name="IP")
    hits_allowed = models.IntegerField(null=True, blank=True, default=0, verbose_name="H")
    runs_allowed = models.IntegerField(null=True, blank=True, default=0, verbose_name="R")
    earned_runs = models.IntegerField(null=True, blank=True, default=0, verbose_name="ER")
    homeruns_allowed =  models.IntegerField(null=True, blank=True, default=0, verbose_name="HR")
    hit_batters = models.IntegerField(null=True, blank=True, default=0, verbose_name="HB")
    walks_allowed = models.IntegerField(null=True, blank=True, default=0, verbose_name="BB")
    strikeouts = models.IntegerField(null=True, blank=True, default=0, verbose_name="K")
    # average = models.FloatField(null=True, blank=True, verbose_name='AVG')
    whip = models.FloatField(null=True, blank=True, verbose_name='WHIP')
    era = models.FloatField(null=True, blank=True, verbose_name='ERA')


    class Meta:
        verbose_name = "Pitchers's Game Stats"
        verbose_name_plural = "Pitcher's Game Stats"


    def __str__(self):
        return f"{self.player}"


    def save(self, *args, **kwargs):
        self.whip = _calc_whip(self.walks_allowed, self.hits_allowed, self.innings_pitched)
        self.era = _calc_era(self.earned_runs, self.innings_pitched)
        # self.average = _calc_average(self.hits_allowed, self.at_bats)
        super(PlayerPitchingGameStats, self).save(*args, **kwargs)







