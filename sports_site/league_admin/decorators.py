from django.core.exceptions import PermissionDenied
from league.models import SeasonStage, Player
from functools import wraps


def user_owns_season_stage(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        stage = SeasonStage.objects.get(pk=kwargs['season_stage_pk'])
        if stage.season.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_owns_player(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        player = Player.objects.get(pk=kwargs['player_pk'])
        if player.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap