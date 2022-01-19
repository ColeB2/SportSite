from django.db.models import  F, FloatField, CharField, Sum, Count, Case, When, Value
from django.db.models.functions import Cast


basic_stat_defaults = {
    'at_bats': {"function": Sum, "args": "at_bats"},
    'plate_appearances': {"function": Sum, "args": "plate_appearances"},
    'runs': {"function": Sum, "args": "runs"},
    'hits': {"function": Sum, "args": "hits"},
    'doubles': {"function": Sum, "args": "doubles"},
    'triples': {"function": Sum, "args": "triples"},
    'homeruns': {"function": Sum, "args": "homeruns"},
    'runs_batted_in': {"function": Sum, "args": "runs_batted_in"},
    'walks': {"function": Sum, "args": "walks"},
    'strikeouts': {"function": Sum, "args": "strikeouts"},
    'stolen_baes': {"function": Sum, "args": "stolen_baes"},
    'caught_stealing': {"function": Sum, "args": "caught_stealing"},
    'hit_by_pitch': {"function": Sum, "args": "hit_by_pitch"},
    'sacrifice_flies': {"function": Sum, "args": "sacrifice_flies"},
    }

average = (
        Cast(F('hits'),FloatField()) /
        Cast(F('at_bats'), FloatField())
        )

on_base_percentage = ((
        Cast(F('hits'), FloatField()) +
        Cast(F('walks'), FloatField()) +
        Cast(F('hit_by_pitch'), FloatField())
        ) /
        (
        Cast(F('at_bats'), FloatField()) +
        Cast(F('walks'), FloatField()) +
        Cast(F('hit_by_pitch'), FloatField()) +
        Cast(F('sacrifice_flies'), FloatField())
        ))


#Note --> Ratio stats must include the stats that create the ratio.
default_league_leader_sums = [
    "homeruns", "runs_batted_in", "stolen_bases", "runs", "at_bats", "hits"]
default_league_leader_ratios = {"average": average}
ratio_stats = {"average": average, "on_base_percentage" : on_base_percentage}
basic_stat_sums = [
    "at_bats", "plate_appearances", "runs", "hits", "doubles", "triples",
    "homeruns", "runs_batted_in", "walks", "strikeouts", "stolen_bases",
    "caught_stealing","hit_by_pitch", "sacrifice_flies"]