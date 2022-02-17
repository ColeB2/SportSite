from django.core.exceptions import PermissionDenied
from functools import wraps
from news.models import Article
from league.models import League



def user_owns_article(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs['slug'])
        league = League.objects.get(admin=request.user)

        # if article.league == request.user.userprofile.league:
        #     return function(request, *args, **kwargs)
        if article.league == league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap