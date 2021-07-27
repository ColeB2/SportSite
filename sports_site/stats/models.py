from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from league.models import PlayerSeason, TeamSeason, SeasonStage, Game
import datetime
from .stat_calc import (_calc_average, _calc_obp, _calc_slugging, _calc_ops,
    _calc_win_pct, _calc_whip, _calc_era, _calc_pitchers_avg)
from .validators import validate_innings_pitched

class PlayerHittingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


class PlayerPitchingStats(models.Model):
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True)


"""Game Related Models"""
class TeamGameStats(models.Model):
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

    runs_for = models.PositiveIntegerField(null=True, blank=True, default=0)
    runs_against = models.PositiveIntegerField(null=True, blank=True, default=0)
    win = models.BooleanField(null=True, default=None)
    loss = models.BooleanField(null=True, default=None)
    tie = models.BooleanField(null=True, default=None)

    linescore = models.CharField(max_length=50, null=True, default="0-0-0-0-0-0-0-0-0", blank=True, help_text="Line score formatted with dashes, - to separate innings.")


    def __str__(self):
        return f"{self.game} Game Stats"


    def save(self, *args, **kwargs):
        self.season = self.team.season
        super(TeamGameStats,self).save(*args, **kwargs)



class TeamGameLineScore(models.Model):
    game = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True)

    first = models.PositiveIntegerField(null=True, blank=True, default=0)
    second = models.PositiveIntegerField(null=True, blank=True, default=0)
    third = models.PositiveIntegerField(null=True, blank=True, default=0)
    fourth = models.PositiveIntegerField(null=True, blank=True, default=0)
    fifth = models.PositiveIntegerField(null=True, blank=True, default=0)
    sixth = models.PositiveIntegerField(null=True, blank=True, default=0)
    seventh = models.PositiveIntegerField(null=True, blank=True, default=0)
    eighth = models.PositiveIntegerField(null=True, blank=True, default=0)
    ninth = models.PositiveIntegerField(null=True, blank=True, default=0)

    extras = models.CharField(max_length=50, null=True, default="None", blank=True, help_text="Extra innings score, formatted with dashes, - to separate each score. Ex for 3 extra innings, 0-1-1.")



class PlayerHittingGameStats(models.Model):
    team_stats = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True, blank=True)

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
    on_base_plus_slugging = models.FloatField(null=True, blank=True, verbose_name="OPS",  help_text="On-Base Plus Slugging\nCombined rate of OBP and SLG.\nOBP+SLG")
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

    win = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="W")
    loss = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="L")
    game = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="G")
    game_started = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="GS")
    complete_game = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="CG")
    shutout = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SHO")
    save_converted = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SV")
    save_op = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SVO")
    innings_pitched = models.FloatField(validators=[validate_innings_pitched],  null=True, blank=True, default=0, verbose_name="IP", help_text="Innings Pitched\nThe number of putouts recorded while the pitcher was on the mound divided by 3.\n.1 - 1 out\n.2 - 2 outs.")
    hits_allowed = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="H")
    runs_allowed = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="R")
    earned_runs = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="ER")
    homeruns_allowed =  models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="HR")
    hit_batters = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="HB")
    walks_allowed = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="BB")
    strikeouts = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="K")
    stolen_bases_allowed = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="SB")
    runners_caught_stealing = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="CS")
    pick_offs = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="PK")
    average = models.FloatField(null=True, blank=True, verbose_name='AVG')
    whip = models.FloatField(null=True, blank=True, verbose_name='WHIP')
    era = models.FloatField(null=True, blank=True, verbose_name='ERA')


    class Meta:
        verbose_name = "Pitching's Game Stats"
        verbose_name_plural = "Pitcher's Game Stats"


    def __str__(self):
        return f"{self.player}"


    def save(self, *args, **kwargs):
        self.whip = _calc_whip(self.walks_allowed, self.hits_allowed, self.innings_pitched)
        self.era = _calc_era(self.earned_runs, self.innings_pitched)
        #self.average = _calc_pitchers_avg(self.hits_allowed, self.innings_pitched, self.pick_offs, self.runners_caught_stealing)
        super(PlayerPitchingGameStats, self).save(*args, **kwargs)







