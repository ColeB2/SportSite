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

basic_stat_sums = ["at_bats", "plate_appearances",
            "runs", "hits", "doubles", "triples", "homeruns", "runs_batted_in",
            "walks", "strikeouts", "stolen_bases", "caught_stealing",
            "hit_by_pitch", "sacrifice_flies"]

basic = {
    "Sum" : Sum
    }

ratio_stats = {
    'average' : {
        "function": Cast,
        "args":
            [{"function": F, "args": "hits" }, FloatField]
            }
    }