from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey

from league.models import PlayerSeason, TeamSeason, SeasonStage, Game



import datetime
from .stat_calc import _calc_average, _calc_obp, _calc_slugging, _calc_ops, _calc_win_pct


class PlayerHittingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


class PlayerPitchingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


"""Game Related Models"""
class TeamGameStats(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True)
    game = ChainedForeignKey(
        Game,
        chained_field = "season",
        chained_model_field="season",
        show_all = False,
        auto_choose=False,
        sort=True,
        null=True)



    def __str__(self):
        return f"{self.game} - {self.owner} Game Stats"


    def save(self, *args, **kwargs):
        self.season = self.team.season
        super(TeamGameStats,self).save(*args, **kwargs)


class PlayerHittingGameStats(models.Model):
    team_stats = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    # player = ChainedForeignKey(
    #     PlayerSeason,
    #     chained_field = "season",
    #     chained_model_field = "season",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=True,
    #     null=True,
    #     )
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)
    at_bats = models.IntegerField(null=True, blank=True, default=0, verbose_name="AB")
    plate_appearances = models.IntegerField(null=True, blank=True, default=0, verbose_name="PA")
    hits = models.IntegerField(null=True, blank=True, default=0, verbose_name="H")
    runs = models.IntegerField(null=True, blank=True, default=0, verbose_name="R")
    strikeouts = models.IntegerField(null=True, blank=True, default=0, verbose_name="SO")
    walks = models.IntegerField(null=True, blank=True, default=0, verbose_name="BB")
    singles = models.IntegerField(null=True, blank=True, default=0, verbose_name="1B")
    doubles = models.IntegerField(null=True, blank=True, default=0, verbose_name="2B")
    triples = models.IntegerField(null=True, blank=True, default=0, verbose_name="3B")
    homeruns = models.IntegerField(null=True, blank=True, default=0, verbose_name="HR")
    stolen_bases = models.IntegerField(null=True, blank=True, default=0, verbose_name="SB")
    caught_stealing = models.IntegerField(null=True, blank=True, default=0, verbose_name="CS")
    runs_batted_in = models.IntegerField(null=True, blank=True, default=0, verbose_name="RBI")
    hit_by_pitch = models.IntegerField(null=True, blank=True, default=0, verbose_name="HBP")
    sacrifice_flies = models.IntegerField(null=True, blank=True, default=0, verbose_name="SF")
    sacrifice_bunts = models.IntegerField(null=True, blank=True, default=0, verbose_name="SAC")
    average = models.CharField(max_length=10, null=False, default='---', verbose_name='AVG')
    on_base_percentage = models.CharField(max_length=10, null=False, default='---', verbose_name='OBP')
    slugging_percentage = models.CharField(max_length=10, null=False, default='---', verbose_name='SLG')
    on_base_plus_slugging = models.CharField(max_length=10, null=False, default='---', verbose_name='OPS', help_text=f"On-Base Plus Slugging\nCombined rate of OBP and SLG."
        f"\nOBP+SLG")
    reached_on_error = models.IntegerField(null=True, blank=True, default=0)
    fielders_choice = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = "Hitter's Game Stats"
        verbose_name_plural = "Hitter's Game Stats"


    # def __str__(self):
    #     return f"{self.player}"


    def save(self, *args, **kwargs):
        self.game = self.team_stats.game
        self.season = self.team_stats.season
        self.hits = (self.singles + self.doubles + self.triples + self.homeruns)
        self.average = _calc_average(self.hits, self.at_bats)
        self.on_base_percentage = _calc_obp(self.hits, self.walks, self.hit_by_pitch, self.at_bats, self.sacrifice_flies)
        self.slugging_percentage = _calc_slugging(self.singles, self.doubles, self.triples, self.homeruns, self.at_bats)
        self.on_base_plus_slugging = _calc_ops(self.on_base_percentage, self.slugging_percentage)
        super(PlayerHittingGameStats, self).save(*args , **kwargs)







