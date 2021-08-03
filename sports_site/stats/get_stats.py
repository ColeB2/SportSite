from django.db.models import  F, FloatField, Sum, Count, Case, When
from django.db.models.functions import Cast
from django.forms.models import model_to_dict
from .models import PlayerHittingGameStats, TeamGameStats



def get_league_leaders(league, featured_stage):
    """Returns league leaders in Avg, HomeRuns, RBI, SB and Runs in use for the
    main home page widget."""
    hitting_stats = PlayerHittingGameStats.objects.all().filter(player__player__league=league, season=featured_stage)
    hitting_stats1 = hitting_stats.values("player").annotate(
        player_id = F("player__player__pk"),
        first = F("player__player__first_name"),
        last = F("player__player__last_name"),
        team = F("player__team__team__team__name"),
        at_bats = Sum('at_bats'),
        runs = Sum('runs'),
        hits = Sum('hits'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        stolen_bases = Sum('stolen_bases'),
        average = Cast(F('hits'),FloatField())/ Cast(F('at_bats'), FloatField())
        )
    return hitting_stats1


def get_all_season_hitting_stats(league, featured_stage):
    """Gets all hitting stats, and returns them in a usable fashion for the
    django-tables2 main stats page."""
    hitting_stats = PlayerHittingGameStats.objects.all().filter(player__player__league=league, season=featured_stage)
    hitting_stats1 = hitting_stats.values("player").annotate(
        first = F("player__player__first_name"),
        last = F("player__player__last_name"),
        at_bats = Sum('at_bats'),
        plate_appearances = Sum('plate_appearances'),
        runs = Sum('runs'),
        hits = Sum('hits'),
        doubles = Sum('doubles'),
        triples = Sum('triples'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        walks = Sum('walks'),
        strikeouts = Sum('strikeouts'),
        stolen_bases = Sum('stolen_bases'),
        caught_stealing = Sum('caught_stealing'),
        hit_by_pitch = Sum('hit_by_pitch'),
        sacrifice_flies = Sum('sacrifice_flies'),
        average = Cast(F('hits'),FloatField())/ Cast(F('at_bats'), FloatField()),
        on_base_percentage = (
            Cast(F('hits'), FloatField()) +
            Cast(F('walks'), FloatField()) +
            Cast(F('hit_by_pitch'), FloatField())
            ) /
            (
            Cast(F('at_bats'), FloatField()) +
            Cast(F('walks'), FloatField()) +
            Cast(F('hit_by_pitch'), FloatField()) +
            Cast(F('sacrifice_flies'), FloatField())
            )
        )
    return hitting_stats1

def get_all_season_standings_stats(league, featured_stage):
    """Gets all the standings data, and returns them in usable fashion for
    django-tables2 standings page"""
    game_stats = TeamGameStats.objects.all().filter(season=featured_stage)
    standings_stats = game_stats.values("team").annotate(
        team_name = F("team__team__name"),
        # wins = Sum("win"),
        win = Count(Case(When(win=True, then=1))),
        loss = Count(Case(When(loss=True, then=1))),
        tie = Count(Case(When(tie=True, then=1))),
        # loss = Sum("loss"),
        # tie = Sum("tie"),
        pct =  (
            Cast(F("win"), FloatField()) +
            (Cast(F("tie"), FloatField()) * 0.5)
            ) /
            (
            Cast(F('win'), FloatField()) +
            Cast(F('loss'), FloatField()) +
            Cast(F('tie'), FloatField())
            ),
        runs_for = Sum("runs_for"),
        runs_against = Sum("runs_against"),
        differential = (
            Cast(F("runs_for"), FloatField()) -
            Cast(F("runs_against"),FloatField())
            ),
        )
    print(f"standings_stats {standings_stats}")
    return standings_stats


def get_extra_innings(linescore_obj):
    """Takes linescore object turns it into a dictionary, removes the game and
    id values from it, then turns the extras values into own key/value pairs in
    the dictionary and returns the dict for use in django-tables."""
    table_data = model_to_dict(linescore_obj, fields=[field.name for field in linescore_obj._meta.fields])
    extra_innings = table_data.pop("extras")
    table_data.pop("game")
    table_data.pop("id")
    if 'None' != extra_innings != None:
        extras = extra_innings.split("-")
        table_data_len = len(table_data)
        extras_len = len(extras)
        for i in range(table_data_len, table_data_len + extras_len, 1):
            list_i = i - table_data_len
            table_data[str(i+1)] = int(extras[list_i])

    return table_data