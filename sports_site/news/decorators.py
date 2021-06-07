from django.core.exceptions import PermissionDenied
from news.models import Article
from functools import wraps


def user_owns_article(function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        article = Article.objects.get(slug=kwargs['slug'])
        if article.league == request.user.userprofile.league:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap