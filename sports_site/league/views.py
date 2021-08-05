from django.shortcuts import render
from .models import (Game, League, Player, PlayerSeason, SeasonStage, Team,
    TeamSeason)
from stats.models import (TeamGameStats, TeamGameLineScore)
from stats.tables import PlayerHittingGameStatsTable


def player_page_view(request, player_pk):
    player = Player.objects.get(pk=player_pk)
    league = player.league
    player_seasons = PlayerSeason.objects.all().filter(player=player)

    context = {
        "league": league,
        "player": player,
        "player_seasons": player_seasons,
        }
    return render(request, "league/player_page.html", context)


def schedule_page_view(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    featured_stage = SeasonStage.objects.get(season__league=league, featured=True)
    schedule = Game.objects.all().filter(season=featured_stage)

    context = {
        "league": league,
        "schedule": schedule,
        "featured_stage": featured_stage,
    }
    return render(request, "league/schedule_page.html", context)


def team_page_view(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    league = team.league
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
    teams = Team.objects.all().filter(league=league)

    context = {
        "league": league,
        "teams": teams,
    }
    return render(request, "league/team_select_page.html", context)


def game_boxscore_page_view(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    league = game.season.season.league

    home_game_stats = TeamGameStats.objects.get(game=game, team=game.home_team)
    home_stats = home_game_stats.playerhittinggamestats_set.all()
    home_stats_table = PlayerHittingGameStatsTable(home_stats)
    home_linescore = home_game_stats.teamgamelinescore_set.all()

    away_game_stats = TeamGameStats.objects.get(game=game, team=game.away_team)
    away_stats = away_game_stats.playerhittinggamestats_set.all()
    away_stats_table = PlayerHittingGameStatsTable(away_stats)
    away_linescore = away_game_stats.teamgamelinescore_set.all()

    context = {
        "game": game,
        "league": league,
        "home_game_stats": home_game_stats,
        "home_stats": home_stats,
        "home_stats_table": home_stats_table,
        "home_linescore": home_linescore,
        "away_game_stats": away_game_stats,
        "away_stats": away_stats,
        "away_stats_table": away_stats_table,
        "away_linescore": away_linescore,
        }
    return render(request, "league/game_boxscore_page.html", context)



