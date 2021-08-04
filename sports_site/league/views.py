from django.shortcuts import render
from .models import (Game, League, Player, PlayerSeason, SeasonStage, Team,
    TeamSeason)


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

    context = {
        "featured_stage": featured_stage,
        "league": league,
        "team": team,

        }
    return render(request, "league/team_page.html", context)


