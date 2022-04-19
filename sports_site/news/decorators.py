from django.core.exceptions import PermissionDenied
from functools import wraps
from news.models import Article
from league.models import League



def user_owns_article(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs['slug'])
        league_slug = request.GET.get('league', request.user.userprofile.league.url)
        league = League.objects.get(url=league_slug)

        
        if article.league == league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap