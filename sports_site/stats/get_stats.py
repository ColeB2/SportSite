from django.db.models import  F, FloatField, Sum
from django.db.models.functions import Cast
from django.forms.models import model_to_dict
from .models import PlayerHittingGameStats



def get_league_leaders(league, featured_stage):
    """Returns league leaders in Avg, HomeRuns, RBI, SB and Runs"""
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


def get_extra_innings(linescore_obj):
    """Takes linescore object turns it into a dictionary, removes the game and
    id values from it, then turns the extras values into own key/value pairs in
    the dictionary and returns the dict for use in django-tables."""
    table_data = [model_to_dict(linescore_obj, fields=[field.name for field in linescore_obj._meta.fields])]
    extra_innings = table_data[0].pop("extras")
    table_data[0].pop("game")
    table_data[0].pop("id")
    if 'None' != extra_innings != None:
        extras = extra_innings.split("-")
        table_data_len = len(table_data[0])
        extras_len = len(extras)
        for i in range(table_data_len, table_data_len + extras_len, 1):
            list_i = i - table_data_len
            table_data[0][str(i+1)] = int(extras[list_i])

    return table_data