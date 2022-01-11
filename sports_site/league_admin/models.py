from django.db import models
from league.models import League

# Create your models here.
"""Testing -- Model Bools for optional stats"""
class PlayerHittingStatsChoice(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    batting_order_position = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Order Position")
    starter = models.BooleanField(null=True, default=True, verbose_name="Starter")
    substitute = models.BooleanField(null=True, default=False, verbose_name="Sub")

    at_bats = models.BooleanField(default=True, verbose_name="AB")
    plate_appearances = models.BooleanField(default=True, verbose_name="PA")
    hits = models.BooleanField(default=True, verbose_name="H")
    runs = models.BooleanField(default=True,  verbose_name="R")
    strikeouts = models.BooleanField(default=True, verbose_name="SO")
    walks = models.BooleanField(default=True, verbose_name="BB")
    singles = models.BooleanField(default=True, verbose_name="1B")
    doubles = models.BooleanField(default=True, verbose_name="2B")
    triples = models.BooleanField(default=True, verbose_name="3B")
    homeruns = models.BooleanField(default=True, verbose_name="HR")
    stolen_bases = models.BooleanField(default=True, verbose_name="SB")
    caught_stealing = models.BooleanField(default=True, verbose_name="CS")
    runs_batted_in = models.BooleanField(default=True, verbose_name="RBI")
    hit_by_pitch = models.BooleanField(default=True, verbose_name="HBP")
    sacrifice_flies = models.BooleanField(default=True, verbose_name="SF")
    sacrifice_bunts = models.BooleanField(default=True, verbose_name="SAC")
    average = models.BooleanField(default=True, verbose_name="AVG")
    on_base_percentage = models.BooleanField(default=True, verbose_name="OBP")
    slugging_percentage = models.BooleanField(default=True, verbose_name="SLG")
    on_base_plus_slugging = models.BooleanField(default=True, verbose_name="OPS",  help_text="On-Base Plus Slugging\nCombined rate of OBP and SLG.\nOBP+SLG")
    reached_on_error = models.BooleanField(default=True, verbose_name="ROE")
    fielders_choice = models.BooleanField(default=True, verbose_name="FC")

    intentional_walks = models.BooleanField(default=True, verbose_name="IBB")
    left_on_base = models.BooleanField(default=True, verbose_name="LOB")
    picked_off = models.BooleanField(default=True, verbose_name="PO")
    ground_into_double_play = models.BooleanField(default=True, verbose_name= "GIDP")
    two_out_runs_batted_in = models.BooleanField(default=True, verbose_name="2-out-RBI")