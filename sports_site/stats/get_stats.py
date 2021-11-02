from django.db.models import  F, FloatField, CharField, Sum, Count, Case, When, Value
from django.db.models.functions import Cast
from django.forms.models import model_to_dict
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameStats)
from league.models import SeasonStage


def annotate_stats(stats_queryset, annotate_value="player"):
    """
    WIP - function to reuse the often reused parts of annotate taken in all
    below querysets.

    TODO:
    - optional stats to grab
    - do the common ones, and combine it based on need of uncommon needs?
    """
    stats_queryset.values(annotate_value).annotate(
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            ),
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


def get_league_leaders(league, featured_stage):
    """
    Returns league leaders in Avg, HomeRuns, RBI, SB and Runs in use for the
    main home page widget.

    Params:
        league - League model object pulled from url GET.get function.
        featured_stage - The SeasonStage model object to be used for the
            gathering of stats.


    Views - news/views.py - home function
    Template - news/home.html
    """
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player__league=league,
                                                season=featured_stage)

    return_stats = hitting_stats.values("player").annotate(
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            )
        )
    return return_stats


def get_team_hitting_stats(league, featured_stage):
    """
    Gets all hittings stats and totals them for each team, and
    returns them in a usable fashion for main stats page/Team.
    """
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player__league=league,
                                                season=featured_stage)

    return_stats = hitting_stats.values("team_stats__team").annotate(
        team = F("team_stats__team__team__name"),
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            ),
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
    return return_stats


def get_all_season_hitting_stats(league, **kwargs):
    """
    Gets all hitting stats for all player, and returns them
    in a usable fashion for the main stats page. Currently used
    for the simple stats filter.

    Params:
        league - League model object

    Kwargs:
        season_stage: season stage object to pass to
        filter by.

    View - stats/views.py - StatsView
    Template - stats/stats_page.html
    """
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player__league=league)
    season_stage = kwargs.pop("season_stage", None)
    if season_stage:
        hitting_stats = hitting_stats.filter(season=season_stage)
    else:
        featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
        hitting_stats = hitting_stats.filter(season=featured_stage)

    return_stats = hitting_stats.values("player").annotate(
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            ),
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
    return return_stats


def get_team_pitching_stats(league, featured_stage):
    """
    Gets all piatching stats and totals them for each team, and
    returns them in a usable fashion for main stats page/Team.
    """
    pitching_stats = PlayerPitchingGameStats.objects.all().filter(
                                                player__player__league=league,
                                                season=featured_stage)

    return_stats = pitching_stats.values("team_stats__team").annotate(
        team = F("team_stats__team__team__name"),
        win = Sum('win'),
        loss = Sum('loss'),
        game = Sum('game_started'),
        game_started = Sum('game_started'),
        complete_game = Sum('complete_game'),
        shutout = Sum('shutout'),
        save_converted = Sum('save_converted'),
        save_op = Sum('save_op'),
        hits_allowed = Sum('hits_allowed'),
        runs_allowed = Sum('runs_allowed'),
        earned_runs = Sum('earned_runs'),
        homeruns_allowed = Sum('homeruns_allowed'),
        hit_batters = Sum('hit_batters'),
        walks_allowed = Sum('walks_allowed'),
        strikeouts = Sum('strikeouts'),
        innings_pitched = Sum('_innings'),
        era = (
            Cast(F('earned_runs'),FloatField()) * 9 /
            Cast(F('innings_pitched'), FloatField())
            ),
        whip = (
            Cast(F('walks_allowed'), FloatField()) +
            Cast(F('hits_allowed'), FloatField())
            ) /
            (
            Cast(F('innings_pitched'), FloatField())
            )
        )

    ##Future Fix: Combine bottom code with top, probably by
    ##Converting to model-to-dict and adding in game counter.
    # test = TeamGameStats.objects.all().filter(
    #     season=featured_stage,
    #     team__team__league=league)
    # x = test.values("team").annotate(
    #     game = Count(
    #         Case(
    #             When(win=True, then=Value(1)),
    #             When(loss=True, then=Value(1)),
    #             When(tie=True, then=Value(1))
    #             ) )
    #     )

    return return_stats


def get_all_season_pitching_stats(league, **kwargs):
    """
    Gets all pitching stats for all player, and returns them in
    a usable fashion for the main stats page.

    Params:
        league - League model object
        featured_stage - The SeasonStage model object to be used
        for the gathering of stats.

    View - stats/views.py - stats_display_view
    Template - stats/pitching_stats_page.html
    """
    pitching_stats = PlayerPitchingGameStats.objects.all().filter(
                                                player__player__league=league)
    season_stage = kwargs.pop("season_stage", None)
    if season_stage:
        pitching_stats = pitching_stats.filter(season=season_stage)
    else:
        featured_stage = SeasonStage.objects.get(season__league=league,
                                             featured=True)
        pitching_stats = pitching_stats.filter(season=featured_stage)

    return_stats = pitching_stats.values("player").annotate(
        first = F("player__player__first_name"),
        last = F("player__player__last_name"),
        win = Sum('win'),
        loss = Sum('loss'),
        game = Sum('game'),
        game_started = Sum('game_started'),
        complete_game = Sum('complete_game'),
        shutout = Sum('shutout'),
        save_converted = Sum('save_converted'),
        save_op = Sum('save_op'),
        hits_allowed = Sum('hits_allowed'),
        runs_allowed = Sum('runs_allowed'),
        earned_runs = Sum('earned_runs'),
        homeruns_allowed = Sum('homeruns_allowed'),
        hit_batters = Sum('hit_batters'),
        walks_allowed = Sum('walks_allowed'),
        strikeouts = Sum('strikeouts'),
        innings_pitched = Sum('_innings'),
        era = (
            Cast(F('earned_runs'),FloatField()) * 9 /
            Cast(F('innings_pitched'), FloatField())
            ),
        whip = (
            Cast(F('walks_allowed'), FloatField()) +
            Cast(F('hits_allowed'), FloatField())
            ) /
            (
            Cast(F('innings_pitched'), FloatField())
            )
        )
    return return_stats


"""Player Page Stats Functions"""
def get_player_season_hitting_stats(player, league, featured_stage):
    """
    Gets hitting stats for a given player, and a given stage.

    Params:
        player - Player Model Object
        league - League model object
        featured_stage - The SeasonStage model object to be used for the
            gathering of stats.

    View - league/views.py player_page_view
    currently deprecated -- note? Already filter by player, do we need to
    annotate by player, or can we aggregate.
    """
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player=player,
                                                player__player__league=league,
                                                season=featured_stage)

    return_stats = hitting_stats.values("player").annotate(
        year = F("season__season__year"),
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
        average = Cast(F('hits'),FloatField()) /
                  Cast(F('at_bats'), FloatField()),
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
    return return_stats


def get_player_last_x_hitting_stats(player, league, num_games):
    """
    Gets last x games played for a hitter to use in display last
    X games table. Does so for the featured stage.

    Params:
        Params:
        player - Player Model Object
        league - League model object
        num_games - Int, number of games wanting to be displayed. Starting from
            most recent, up until the nth number of game described by this int.

    View - league/views.py player_page_view
    """

    hitting_stats = PlayerHittingGameStats.objects.filter(
                                    player__player=player,
                                    player__player__league=league,
                                    season__featured=True).order_by(
                                        "-team_stats__game__date"
                                        )[:num_games]

    return_stats = hitting_stats.values("team_stats__game__date").annotate(
        date = F("team_stats__game__date"),
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            ),
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
    return return_stats


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
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                    player__player=player,
                                    player__player__league=league,
                                    season__featured=True).order_by(
                                        "-team_stats__game__date")[:num_games]

    return_stats = hitting_stats.aggregate(
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
        )

    return_stats["duration"] = f"Last {num_games} Games"
    try:
        return_stats["average"] = return_stats["hits"] / return_stats["at_bats"]
    except:
        return_stats["average"] = .000
    try:
        return_stats["on_base_percentage"] = (
            (
            return_stats["hits"] +
            return_stats["walks"] +
            return_stats["hit_by_pitch"]
            ) /
            (
            return_stats["at_bats"] +
            return_stats["walks"] +
            return_stats["hit_by_pitch"] +
            return_stats["sacrifice_flies"]
            ))
    except:
        return_stats["on_base_percentage"] = .000

    print(f"return stats {return_stats}")

    return return_stats



def get_all_player_season_hitting_stats(player, league,
                                        stage_type=SeasonStage.REGULAR):
    """
    Retrieves the hittings stats for each season participated
    in for given stage type.
    """
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player=player,
                                                player__player__league=league,
                                                season__stage=stage_type)

    return_stats = hitting_stats.values("season__season__year").annotate(
        year = F("season__season__year"),
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
        average = (
            Cast(F('hits'),FloatField()) /
            Cast(F('at_bats'), FloatField())
            ),
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
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
                                                player__player=player,
                                                player__player__league=league,
                                                season__stage=stage_type)

    return_stats = hitting_stats.aggregate(
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
        )

    return_stats["year"] = "Career"
    return_stats["average"] = return_stats["hits"] / return_stats["at_bats"]
    return_stats["on_base_percentage"] = (
        (
        return_stats["hits"] +
        return_stats["walks"] +
        return_stats["hit_by_pitch"]
        ) /
        (
        return_stats["at_bats"] +
        return_stats["walks"] +
        return_stats["hit_by_pitch"] +
        return_stats["sacrifice_flies"]
        ))

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
    """
    game = player.team_stats.game
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
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
    game_stats = TeamGameStats.objects.all().filter(season=featured_stage)
    standings_stats = game_stats.values("team").annotate(
        team_name = F("team__team__name"),
        win = Count(Case(When(win=True, then=1))),
        loss = Count(Case(When(loss=True, then=1))),
        tie = Count(Case(When(tie=True, then=1))),
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
    return standings_stats


