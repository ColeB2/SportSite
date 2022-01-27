from django.db.models import  F, FloatField, Sum, Count, Case, When
from django.db.models.functions import Cast
from django.forms.models import model_to_dict
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameStats)
from league.models import SeasonStage

from .stats_defaults import (basic_stat_sums, ratio_stats,
    default_league_leader_ratios, default_league_leader_sums,
    basic_pitching_ratios, basic_pitching_sums_team, basic_pitching_sums_league,
    basic_team_sums, basic_team_ratios, stats_dict_choices)




def stats_dict(initial_dict, sum_stat_list=basic_stat_sums,
                                                   ratio_stat_dict=ratio_stats):

    """
    Uses a list/dict combo to populate an initial dictionary of stats,
    to be passed to annotate_stats to annotate on.

    Params:
        sum_stat_list: A list of stats in which Sum function is to be
            used in the annotation, ex, hits, at_bats, etc.
            Default: basic_stat_sums from stats_default.py

        ratio_stat_dict: A dictionary of ratio stats (batting average, OBP,
            etc.) to be used in the annotation.
            Default: ratio_stats from stats_default.py
    """

    for val in sum_stat_list:
        if type(val) == tuple:
            initial_dict[val[0]] = Sum(val[1])
        else:
            initial_dict[val] = Sum(val)
    for k, v in ratio_stat_dict.items():
        initial_dict[k] = v

    return initial_dict


def annotate_stats(stats_queryset, annotate_dict, annotate_value="player"):
    """
    Annotates a stats based on given dict, from stats_dict

    Params:
        stats_queryset - queryset to call .values and .annotate on.
        annotate_dict - Dictionary of (from stats_dict) of all operations
            to be annotated on, ie Sum, Count etc.
        annotate_value - Value that is being annotated on.
            Default: "player"
    """
    return_stats = stats_queryset.values(annotate_value).annotate(**annotate_dict)
    return return_stats


def aggregate_stats(stats_queryset, aggregate_dict):
    return_stats = stats_queryset.aggregate(**aggregate_dict)
    return return_stats


def average(aggregated_dict):
    try:
        aggregated_dict["average"] = aggregated_dict["hits"] / aggregated_dict["at_bats"]
    except:
        aggregated_dict["average"] = .000
    return aggregated_dict


def obp(aggregated_dict):
    try:
        aggregated_dict["on_base_percentage"] = (
            (
            aggregated_dict["hits"] +
            aggregated_dict["walks"] +
            aggregated_dict["hit_by_pitch"]
            ) /
            (
            aggregated_dict["at_bats"] +
            aggregated_dict["walks"] +
            aggregated_dict["hit_by_pitch"] +
            aggregated_dict["sacrifice_flies"]
            ))
    except:
        aggregated_dict["on_base_percentage"] = .000


def aggregate_ratios(aggregated_dict):
    """
    Adds the common ratio stats needed
    """

    average(aggregated_dict)
    obp(aggregated_dict)

    return aggregated_dict


def get_stats(queryset, stats_to_retrieve, **filters):
    """
    Gets stats, and returns them in a usable fashion for any
    stats page needing stats.

    Params:
        league - League model object
        stats_to_retrieve = str value to call proper defaults on a dict
            Dict kept in stats_defaults.py
        season_stage = SeasonStage model_obj, defaults to None, which
            then defaults to featured stage.

    View - stats/views.py - StatsView
    Template - stats/stats_page.html
    """
    stats = stats_dict_choices[str(stats_to_retrieve)]

    return_stats = _get_stats(
        queryset=queryset,
        filters=filters,
        initial=stats["initial"],
        default_stats=stats["default_stats"],
        annotation_value=stats["annotation_value"])

    return return_stats


def _get_stats(queryset, filters, initial, default_stats, annotation_value, order_value=None):
    """
    Params:
        queryset - Queryset of stats object we are going to process.
        filters - Filters to pass to the queryset
        default_stats - Default stats, which are either default, or
            to be chosen by the user ot pass on.
        annotation_valute - the value to be annotated on
        order_value - The value to by ordered on
    """
    stats = queryset.filter(**filters)

    annotate_dict = stats_dict(initial, default_stats[0], default_stats[1])
    return_stats = annotate_stats(stats, annotate_dict, annotation_value)

    return return_stats


def get_stats_agg(queryset, stats_to_retrieve, **filters):
    stats = stats_dict_choices[str(stats_to_retrieve)]


    default_stats = stats["default_stats"]
    aggregate_dict = stats_dict(stats["initial"], default_stats[0], default_stats[1])
    return_stats = aggregate_stats(queryset, aggregate_dict)

    add_additional_keys(return_stats, stats["additional_keys"])
    aggregate_ratios(return_stats)
    return return_stats


"""Player Page Stats Functions"""
def get_player_last_x_hitting_stats_totals(player, league, num_games):
    """
    Gets last x games played totals for a hitter to use in display
    last X games totals table. Does so for the featured stage.

    Params:
        Params:
        player - Player Model Object
        league - League model object
        num_games - Int, number of games wanting to be displayed. Starting from
            most recent, up until the nth number of game described by this int.

    View - league/views.py player_page_view"""
    hitting_stats = PlayerHittingGameStats.objects.filter(
                                    player__player=player,
                                    player__player__league=league,
                                    season__featured=True).order_by(
                                        "-team_stats__game__date")[:num_games]

    aggregate_dict = stats_dict({}, basic_stat_sums, ratio_stat_dict={})
    return_stats = aggregate_stats(hitting_stats, aggregate_dict)

    return_stats["duration"] = f"Last {num_games} Games"
    aggregate_ratios(return_stats)


    return return_stats


def get_player_career_hitting_stats(player,
                                    league,
                                    stage_type=SeasonStage.REGULAR):
    """
    Retrieves the career hittings stats for given player during given
    stage_type. Defaults to regular season.

    Params:
        player - Player model object from league.models Player.
        league - League model object from league.models League.
            Retrieved from request.GET.get('league') url.
        stage_type - stage field from SeasonStage model object.
            Defaults to SeasonStage.REGULAR

    Returns dictionary of totals for various player hitting stats.

    Views: league/views.py - player_page_view.

    """
    hitting_stats = PlayerHittingGameStats.objects.filter(
                                                player__player=player,
                                                player__player__league=league,
                                                season__stage=stage_type)

    aggregate_dict = stats_dict({}, basic_stat_sums, ratio_stat_dict={})
    return_stats = aggregate_stats(hitting_stats, aggregate_dict)

    return_stats["year"] = "Career"
    aggregate_ratios(return_stats)

    return return_stats


def get_extra_innings(linescore_obj):
    """
    Takes linescore object turns it into a dictionary, removes the
    game and id values from it, then turns the extras values into
    own key/value pairs in the dictionary and returns the dict for
    use in django-tables.

    Data retured as a list of multiple obj of itself used as so:
    TeamGameLineScoreTable([-returned table_data-,])

    Params:
        linescore_obj - TeamGameLineScore model object - stats/models.py

    Views - league/views.py - game_boxscore_page_view
    Templates Featured - league/game_boxscore_page.html
    """
    table_data = model_to_dict(
                    linescore_obj,
                    fields=[field.name for field in linescore_obj._meta.fields])
    extra_innings = table_data.pop("extras")
    game_pk = table_data.pop("game")
    table_data.pop("id")

    if 'None' != extra_innings != None:
        extras = extra_innings.split("-")
        table_data_len = len(table_data)
        extras_len = len(extras)
        for i in range(table_data_len, table_data_len + extras_len, 1):
            list_i = i - table_data_len
            table_data[str(i+1)] = int(extras[list_i])

    table_data["R"] = sum(table_data.values())
    tgs = TeamGameStats.objects.get(pk=game_pk)
    if tgs.team.team.abbreviation:
        table_data["game"] = tgs.team.team.abbreviation
    else:
        table_data["game"] = tgs.team.team.name


    return table_data


def _get_extra_stat_totals(player):
    """
    Internal method used in get_stats_info. Retrieves the totals for
    the extra stats from a playerhittinggamestats model object.

    Params:
        player - PlayerHittingGameStats object

    TODO: Remove hard coded date.
    """
    game = player.team_stats.game
    hitting_stats = PlayerHittingGameStats.objects.filter(
                        player__player=player.player.player,
                        season=game.season,
                        team_stats__game__date__range=["2021-05-14",game.date])

    return_stats = hitting_stats.values("player").aggregate(
        doubles = Sum('doubles'),
        triples = Sum('triples'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        two_out_runs_batted_in = Sum('two_out_runs_batted_in'),
        stolen_bases = Sum('stolen_bases'),
        caught_stealing = Sum('caught_stealing'),
        )
    return return_stats


def get_stats_info(stats_queryset):
    """
    get_stats_info - Get the extra info stats that shows under the
    boxscore of a game summary.

    Used in conjunction with format_stats to gather and display
    properly. ie format_stats(get_stats_info(-given_stats-))

    Params:
        stats_queryset: Queryset of multiple PlayerHittingGameStats.
            Often gathered in reverse from a TeamGameStats object.
            ie teamgamestatsobject.playerhittinggamestats_set.all()

    Views - league/views.py game_boxscore_page_view
    Templates - league/game_boxscore_page.html
    """
    doubles = ["2B:",]
    triples = ["3B:",]
    homeruns = ["HR:",]
    total_bases = ["TB:",]
    rbi = ["RBI:",]
    rbi_2out = ["2-out RBI:",]
    gidp = ["GIDP:",]
    sf = ["SF:",]
    sb = ["SB:",]
    cs = ["CS:",]
    po = ["PO:",]

    for player in stats_queryset:
        player_totals = _get_extra_stat_totals(player)
        if player.hits:
            tb = player.singles
            if player.doubles:
                tb += player.doubles*2
                doubles.append(
                    (player, player.doubles, player_totals["doubles"]))
            if player.triples:
                tb += player.triples*3
                triples.append(
                    (player, player.triples, player_totals["triples"]))
            if player.homeruns:
                tb += player.homeruns*4
                homeruns.append(
                    (player, player.homeruns, player_totals["homeruns"]))
        if player.two_out_runs_batted_in:
            rbi_2out.append((player, player.two_out_runs_batted_in, None))
        if player.runs_batted_in:
            rbi.append(
                (player, player.runs_batted_in, player_totals["runs_batted_in"])
                )
        if player.ground_into_double_play:
            gidp.append(
                (player, player.ground_into_double_play, None))
        if player.sacrifice_flies:
            sf.append((player, player.sacrifice_flies, None))

        if player.stolen_bases:
            sb.append(
                (player, player.stolen_bases, player_totals["stolen_bases"]))
        if player.caught_stealing:
            cs.append(
                (player, player.caught_stealing,
                 player_totals["caught_stealing"]))
        if player.picked_off:
            po.append((player, player.picked_off, None))



    return (doubles, triples, homeruns, total_bases, rbi, rbi_2out, gidp, sf,
            sb, cs, po)

def format_stats(stats):
    """
    Formats boxscore extra stats that show under the box score.
    Ex, is Joe hits a homerun HR: Joe, Bob(8)

    Used in conjunction with format_stats to gather and display properly.
    i.e. format_stats(get_stats_info(<given_stats>))

    Params:
        stats: Stats returned from get_stats_info(<stats>) function.

    View - league/views.py - game_boxscore_page_view
    Templates - league/game_boxscore_page.html
    """
    stat_list = []
    for stat in stats:
        stat_type = stat.pop(0)
        stat_str = ""
        for player, stat_value, total in stat:
            last = player.player.player.last_name
            first = player.player.player.first_name[0]
            if stat_value == 1:
                stat_value=""
            if total:
                player_str = f" {last}, {first}. {str(stat_value)} ({total});"
            else:
                player_str = f" {last}, {first}. {str(stat_value)};"

            stat_str += player_str
        stat_list.append((stat_type, stat_str))
    return stat_list


def get_pitching_stats_info(stats_queryset):
    """
    get_pitching_stats_info - Get the extra info stats that shows under
    the pitching stats of a game summary.

    Used in conjunction with format_pitching_stats to gather and display
    properly.
        ie format_pitching_stats(get_pitching_stats_info(-given_stats-))

    Params:
        stats_queryset: Queryset of multiple PlayerHittingGameStats.
            Often gathered in reverse from a TeamGameStats object.
            ie teamgamestatsobject.playerhittinggamestats_set.all()

    Views - league/views.py game_boxscore_page_view
    Templates - league/game_boxscore_page.html
    """
    balks = ["Balk:",]
    hit_batters = ["HBP:",]
    batters_faced = ["Batters faced:",]

    for player in stats_queryset:
        player_totals = _get_extra_stat_totals(player)
        if player.balk:
            balks.append((player, player.balk, None))
        if player.hit_batters:
            hit_batters.append(
                (player, player.hit_batters, player_totals["hit_batters"])
                )
        if player.batters_faced:
            batters_faced.append(
                (player, player.batters_faced, None))

    return (balks, hit_batters, batters_faced)


"""Stadings Page"""
def get_all_season_standings_stats(league, featured_stage):
    """
    Gets all the standings data for the featured stage, and returns
    them in usable fashion for a django-tables2 standings page.

    Params:
        league - League model object
        featured_stage - The SeasonStage model object to be used for the
            gathering of stats.

    Views - stats/views.py - standings_display_view
    Template Featured - stats/standings_page.html
    """
    game_stats = TeamGameStats.objects.filter(season=featured_stage)

    initial = {"team_name": F("team__team__name")}
    annotate_dict = stats_dict(initial, basic_team_sums, basic_team_ratios)
    return_stats = annotate_stats(game_stats, annotate_dict, "team")

    return return_stats


