from django.db.models import  F, FloatField, Sum, Count, Case, When
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

on_base_percentage = (
    (
    Cast(F('hits'), FloatField())
    + Cast(F('walks'), FloatField())
    + Cast(F('hit_by_pitch'), FloatField())
    ) /
    (
    Cast(F('at_bats'), FloatField())
    + Cast(F('walks'), FloatField())
    + Cast(F('hit_by_pitch'), FloatField())
    + Cast(F('sacrifice_flies'), FloatField())
    ))


era = (
            Cast(F('earned_runs'),FloatField()) * 9 /
            Cast(F('innings_pitched'), FloatField())
            )
whip = (
    (
    Cast(F('walks_allowed'), FloatField())
    + Cast(F('hits_allowed'), FloatField())
    ) /
    (
    Cast(F('innings_pitched'), FloatField())
    ))


#Team Options
differential = (
    Cast(F("runs_for"), FloatField())
    - Cast(F("runs_against"),FloatField())
    )

pct =  (
    (
    Cast(F("win"), FloatField())
    + (Cast(F("tie"), FloatField()) * 0.5)
    ) /
    (
    Cast(F('win'), FloatField())
    + Cast(F('loss'), FloatField())
    + Cast(F('tie'), FloatField())
    )
    )

win = Count(Case(When(win=True, then=1)))
loss = Count(Case(When(loss=True, then=1)))
tie = Count(Case(When(tie=True, then=1)))

#Note --> Ratio stats must include the stats that create the ratio.
#Hitting Defaults
default_league_leader_sums = [
    "homeruns", "runs_batted_in", "stolen_bases", "runs", "at_bats", "hits"]
default_league_leader_ratios = {"average": average}
ratio_stats = {"average": average, "on_base_percentage" : on_base_percentage}
basic_stat_sums = [
    "at_bats", "plate_appearances", "runs", "hits", "doubles", "triples",
    "homeruns", "runs_batted_in", "walks", "strikeouts", "stolen_bases",
    "caught_stealing","hit_by_pitch", "sacrifice_flies"]
last_x_defaults = [
    ]



#Pitching Defaults
basic_pitching_sums_team = [
    "win", "loss", ("game", "game_started"), "game_started", "complete_game", "shutout",
    "save_converted", "save_op", "hits_allowed", "runs_allowed", "earned_runs",
    "homeruns_allowed", "hit_batters", "walks_allowed", "strikeouts",
    ("innings_pitched", "_innings")]
basic_pitching_sums_league = [
    "win", "loss", "game", "game_started", "complete_game", "shutout",
    "save_converted", "save_op", "hits_allowed", "runs_allowed", "earned_runs",
    "homeruns_allowed", "hit_batters", "walks_allowed", "strikeouts",
    ("innings_pitched", "_innings")]
#Need to fix to add earned runs, innings pitched, walk, hits for league leader pages
basic_pitching_ratios = {"era": era, "whip": whip}


#Team Record/Stast default
basic_team_sums = ["runs_for", "runs_against"]
basic_team_ratios = {"win": win, "loss": loss, "tie": tie, "pct": pct, "differential": differential}


##Default dict
"""Main Stats Page Defaults"""
stats_page_hitting_defaults = {
    "initial": {
        'first': F("player__player__first_name"),
        'last': F("player__player__last_name")},
    "default_stats": [basic_stat_sums, ratio_stats],
    "annotation_value": "player"
    }

stats_page_pitching_defaults = {
    "initial": {
        'first': F("player__player__first_name"),
        'last': F("player__player__last_name")},
    "default_stats": [basic_pitching_sums_league, basic_pitching_ratios],
    "annotation_value": "player"
    }

team_stats_page_hitting_defaults = {
    "initial": {
        "team" : F("team_stats__team__team__name")},
    "default_stats": [basic_stat_sums, ratio_stats],
    "annotation_value": "team_stats__team"
    }

team_stats_page_pitching_defaults = {
    "initial": {
        "team" : F("team_stats__team__team__name")},
    "default_stats": [basic_pitching_sums_team, basic_pitching_ratios],
    "annotation_value": "team_stats__team"
    }

"""Home Page Leaders Defaults"""
hitting_league_leaders_defaults = {
    "initial": {
        "player_id": F("player__player__pk"),
        "first": F("player__player__first_name"),
        "last": F("player__player__last_name"),
        "team": F("player__team__team__team__name")
        },
    "default_stats": [default_league_leader_sums, default_league_leader_ratios],
    "annotation_value": "player"
    }

"""Player Stats Page Defaults"""
last_x_hitting_stats_defaults = {
    "initial": {
        "date": F("team_stats__game__date")
        },
    "default_stats": [basic_stat_sums, ratio_stats],
    "annotation_value": "team_stats__game__date"
    }

player_career_hitting_stats = {
    "initial": {
        "year": F("season__season__year")
        },
    "default_stats": [basic_stat_sums, ratio_stats],
    "annotation_value": "season__season__year"
    }

##Player Page --> uses aggregate instead
last_x_hitting_stats_totals_defaults = {
    "initial": {},
    "default_stats": [basic_stat_sums, {}],
    "additional_keys": {},
    }

player_career_hitting_stats_totals = {
    "initial": {},
    "default_stats": [basic_stat_sums, {}],
    "additional_keys": {"year": "Career"},
    }

stats_dict_choices = {
    "all_season_hitting": stats_page_hitting_defaults,
    "all_season_pitching": stats_page_pitching_defaults,
    "team_season_hitting": team_stats_page_hitting_defaults,
    "team_season_pitching": team_stats_page_pitching_defaults,
    "hitting_league_leaders": hitting_league_leaders_defaults,
    "last_x_hitting_date": last_x_hitting_stats_defaults,
    "last_x_hitting_stats_totals": last_x_hitting_stats_totals_defaults,
    "player_career_hitting_stats": player_career_hitting_stats,
    "player_career_hitting_stats_totals": player_career_hitting_stats_totals,
    }


