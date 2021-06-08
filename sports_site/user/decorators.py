from django.core.exceptions import PermissionDenied
from league.models import Roster
from functools import wraps


def user_owns_roster(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        roster = Roster.objects.get(pk=kwargs['roster_pk'])
        if roster.team.team.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap