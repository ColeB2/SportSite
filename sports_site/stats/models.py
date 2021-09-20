from django.db import models
from league.models import PlayerSeason, TeamSeason, SeasonStage, Game
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

    first = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="1")
    second = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="2")
    third = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="3")
    fourth = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="4")
    fifth = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="5")
    sixth = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="6")
    seventh = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="7")
    eighth = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="8")
    ninth = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="9")

    extras = models.CharField(max_length=50, null=True, default="None", blank=True, help_text="Extra innings score, formatted with dashes, - to separate each score. Ex for 3 extra innings, 0-1-1.", verbose_name="extras")


    def __str__(self):
        return f"{self.game.team.team} Linescore for {self.game}"



class PlayerHittingGameStats(models.Model):
    team_stats = models.ForeignKey(TeamGameStats, on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, null=True, blank=True)

    batting_order_position = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Order Position")
    starter = models.BooleanField(null=True, default=True, verbose_name="Starter")
    substitute = models.BooleanField(null=True, default=False, verbose_name="Sub")

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

    intentional_walks = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="IBB")
    left_on_base = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="LOB")
    picked_off = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="PO")
    ground_into_double_play = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name= "GIDP")
    two_out_runs_batted_in = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="2-out-RBI")


    class Meta:
        verbose_name = "Hitter's Game Stats"
        verbose_name_plural = "Hitter's Game Stats"


    def __str__(self):
        return f"Player: {self.player.player} Game: {self.team_stats}"


    def save(self, *args, **kwargs):
        self.game = self.team_stats.game
        self.season = self.team_stats.season
        self.hits = (self.singles + self.doubles + self.triples + self.homeruns)
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
        super(PlayerPitchingGameStats, self).save(*args, **kwargs)







