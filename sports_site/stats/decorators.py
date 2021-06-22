from django.core.exceptions import PermissionDenied
from league.models import Game
from functools import wraps


def user_owns_game(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        game = Game.objects.get(pk=kwargs['game_pk'])
        if game.season.season.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap