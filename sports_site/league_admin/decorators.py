from django.core.exceptions import PermissionDenied
from league.models import Player, Season, SeasonStage, Team, TeamSeason
from functools import wraps


def user_owns_season_stage(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        stage = SeasonStage.objects.get(pk=kwargs['season_stage_pk'])
        if (
            request.user.is_authenticated and
            stage.season.league == request.user.userprofile.league
            ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_owns_player(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        player = Player.objects.get(pk=kwargs['player_pk'])
        if (
            request.user.is_authenticated and 
            player.league == request.user.userprofile.league
            ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_owns_season(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        season = Season.objects.get(pk=kwargs['season_pk'])
        if (
            request.user.is_authenticated and
            season.league == request.user.userprofile.league
            ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_owns_team_season(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        teamseason = TeamSeason.objects.get(pk=kwargs['team_season_pk'])
        if (
            request.user.is_authenticated and
            teamseason.team.league == request.user.userprofile.league
            ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_owns_team(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['team_pk'])
        
        if (
            request.user.is_authenticated and
            team.league == request.user.userprofile.league
            ):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap