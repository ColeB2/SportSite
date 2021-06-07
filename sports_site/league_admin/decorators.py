from django.core.exceptions import PermissionDenied
from league.models import SeasonStage


def user_owns_season_stage(function):
    def wrap (request, *args, **kwargs):
        stage = SeasonStage.objects.get(pk=kwargs['season_stage_pk'])
        if stage.season.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap