from django.core.exceptions import PermissionDenied
from functools import wraps
from news.models import Article
from league.models import League



def user_owns_article(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs['slug'])
        league=None
        if request.user.is_authenticated:
            league_slug = request.user.userprofile.league.url
            league = League.objects.get(url=league_slug)

        if league and article.league == league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap