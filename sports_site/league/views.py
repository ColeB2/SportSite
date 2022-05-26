from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from stats.get_stats import (format_stats, get_stats, get_stats_aggregate,
    get_extra_innings, get_stats_info)
from stats.models import TeamGameStats, PlayerHittingGameStats
from stats.tables import (BattingOrderTable, PitchingOrderTable,
    PlayerHittingGameStatsTable, PlayerPageGameHittingStatsSplitsTable,
    PlayerPageHittingStatsTable, PlayerPageHittingStatsSplitsTable,
    PlayerPitchingGameStatsTable, TeamGameLineScoreTable,)
from .models import Game, League, Player, PlayerSeason, SeasonStage, Team



def player_page_view(request, player_pk):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)

    player = get_object_or_404(Player, pk=player_pk, league=league)
    player_seasons = PlayerSeason.objects.filter(player=player)

    num_games = 5
    qs = PlayerHittingGameStats.objects.filter(
                                            player__player=player,
                                            player__player__league=league)

    player_splits_qs = qs.filter(
        season__featured=True).order_by("-team_stats__game__date")


    all_stats_filters = {"season__stage": SeasonStage.REGULAR}
    all_stats = get_stats(qs, "player_career_hitting_stats", filters=all_stats_filters)
    player_splits = get_stats(player_splits_qs[:num_games], "last_x_hitting_date")
    career_stats = get_stats_aggregate(qs, "player_career_hitting_stats_totals", filters=all_stats_filters)
    last_x = [3,5,7]
    last_x_splits = []
    for val in last_x:
        extra_keys = {"duration": f"Last {val} Games"}
        last_x_splits.append(
            get_stats_aggregate(player_splits_qs[:val], "last_x_hitting_stats_totals", extra_keys=extra_keys)
            )

    table_data = []
    for statline in all_stats:
        table_data.append(statline)
    table_data.append(career_stats)

    table = PlayerPageHittingStatsTable(table_data)
    split_table = PlayerPageGameHittingStatsSplitsTable(player_splits)
    last_x_table = PlayerPageHittingStatsSplitsTable(last_x_splits)

    context = {
        "league": league,
        "player": player,
        "player_seasons": player_seasons,
        "table_data": table_data,
        "table": table,
        "split_table": split_table,
        "last_x_table": last_x_table,
        }
    return render(request, "league/player_page.html", context)


def schedule_page_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league, featured=True)
    schedule = Game.objects.filter(season=featured_stage)

    context = {
        "league": league,
        "schedule": schedule,
        "featured_stage": featured_stage,
    }
    return render(request, "league/schedule_page.html", context)


def team_page_view(request, team_pk):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    team = Team.objects.get(pk=team_pk)
    featured_stage = SeasonStage.objects.get(season__league=league, featured=True)

    team_season = team.teamseason_set.all()

    context = {
        "featured_stage": featured_stage,
        "league": league,
        "team_season": team_season,
        "team": team,
        }
    return render(request, "league/team_page.html", context)


def team_select_page_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    teams = Team.objects.filter(league=league)

    context = {
        "league": league,
        "teams": teams,
    }
    return render(request, "league/team_select_page.html", context)


def game_boxscore_page_view(request, game_pk):
    """Page that shows all the stats for a given game, the boxscore etc."""
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    game = Game.objects.get(pk=game_pk)

    # home_game_stats = TeamGameStats.objects.get(game=game, team=game.home_team)
    home_game_stats = get_object_or_404(TeamGameStats, game=game, team=game.home_team)
    home_stats = home_game_stats.playerhittinggamestats_set.all()
    home_stats_table = PlayerHittingGameStatsTable(home_stats)
    home_pitching_stats = home_game_stats.playerpitchinggamestats_set.all()
    home_pitching_stats_table = PlayerPitchingGameStatsTable(home_pitching_stats)

    home_boxscore = BattingOrderTable(home_stats)
    home_pitching = PitchingOrderTable(home_pitching_stats)
    home_extra = format_stats(get_stats_info(home_stats))


    away_game_stats = TeamGameStats.objects.get(game=game, team=game.away_team)
    away_stats = away_game_stats.playerhittinggamestats_set.all()
    away_stats_table = PlayerHittingGameStatsTable(away_stats)
    away_pitching_stats = away_game_stats.playerpitchinggamestats_set.all()
    away_pitching_stats_table = PlayerPitchingGameStatsTable(away_pitching_stats)

    away_boxscore = BattingOrderTable(away_stats)
    away_pitching = PitchingOrderTable(away_pitching_stats)
    away_extra = format_stats(get_stats_info(away_stats))


    try:
        home_linescore = home_game_stats.teamgamelinescore_set.all()[0]
        away_linescore = away_game_stats.teamgamelinescore_set.all()[0]
        table_data = [
            get_extra_innings(away_linescore),
            get_extra_innings(home_linescore)
        ]
        boxscore_table = TeamGameLineScoreTable(table_data)
    except (ObjectDoesNotExist, IndexError):
        home_linescore = None
        away_linescore = None
        table_data = None
        boxscore_table = None


    context = {
        "game": game,
        "league": league,
        "home_game_stats": home_game_stats,
        "home_stats": home_stats,
        "home_stats_table": home_stats_table,
        "home_boxscore": home_boxscore,
        "home_pitching": home_pitching,
        "home_extra": home_extra,
        "home_pitching_stats_table": home_pitching_stats_table,
        "home_linescore": home_linescore,
        "away_game_stats": away_game_stats,
        "away_stats": away_stats,
        "away_stats_table": away_stats_table,
        "away_boxscore": away_boxscore,
        "away_pitching": away_pitching,
        "away_extra": away_extra,
        "away_pitching_stats_table": away_pitching_stats_table,
        "away_linescore": away_linescore,
        "boxscore_table": boxscore_table
        }
    return render(request, "league/game_boxscore_page.html", context)



