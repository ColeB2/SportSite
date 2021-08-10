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


def get_extra_stat_totals(player):
    """Gets totals for extra stats given playerhitting gamestats object
    player - PlayerHittingGameStats object"""
    game = player.team_stats.game
    hitting_stats = PlayerHittingGameStats.objects.all().filter(
        player__player=player.player, season=game.season, team_stats__game__date__range=["2021-05-14",game.date])
    hitting_stats1 = hitting_stats.values("player").annotate(
        doubles = Sum('doubles'),
        triples = Sum('triples'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        two_out_runs_batted_in = Sum('two_out_runs_batted_in'),
        stolen_bases = Sum('stolen_bases'),
        caught_stealing = Sum('caught_stealing'),
        sacrifice_flies = Sum('sacrifice_flies'),
        gidp = Sum('ground_into_double_play'),
        po = Sum('picked_off')
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
    return standings_stats


def get_extra_innings(linescore_obj):
    """Takes linescore object turns it into a dictionary, removes the game and
    id values from it, then turns the extras values into own key/value pairs in
    the dictionary and returns the dict for use in django-tables."""
    table_data = model_to_dict(linescore_obj, fields=[field.name for field in linescore_obj._meta.fields])
    print(table_data)
    extra_innings = table_data.pop("extras")
    # game_obj = TeamGameStats.objects.get(pk=table_data.pop("game"))
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
    table_data["game"] = TeamGameStats.objects.get(pk=game_pk)
    # table_data["F"] = game_obj.team.team.name

    return table_data


def get_stats_info(stats_queryset):
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
        if player.hits:
            tb = player.singles
            if player.doubles:
                tb += player.doubles*2
                doubles.append((player, player.doubles))
            if player.triples:
                tb += player.triples*3
                triples.append((player, player.triples))
            if player.homeruns:
                tb += player.homeruns*4
                homeruns.append((player, player.homeruns))
        if player.two_out_runs_batted_in:
            rbi_2out.append((player, player.two_out_runs_batted_in))
        if player.runs_batted_in:
            rbi.append((player, player.runs_batted_in))
        if player.ground_into_double_play:
            gidp.append((player, player.ground_into_double_player))
        if player.sacrifice_flies:
            sf.append((player, player.sacrifice_flies))

        if player.stolen_bases:
            sb.append((player, player.stolen_bases))
        if player.caught_stealing:
            cs.append((player, player.caught_stealing))
        if player.picked_off:
            po.append((player, player.picked_off))



    return (doubles, triples, homeruns, total_bases, rbi, rbi_2out, gidp, sf, sb,cs,po)

def format_stats(stats):
    stat_list = []
    print(f"stats {stats}")
    for stat in stats:
        print(f"stat: {stat}")
        stat_type = stat.pop(0)
        print(f"stat_type {stat_type}")
        stat_str = ""
        for player, stat_value in stat:
            last = player.player.player.last_name
            first = player.player.player.first_name[0]
            player_str = f" {last}, {first}. {str(stat_value)};"

            stat_str += player_str
        stat_list.append((stat_type, stat_str))
    return stat_list



