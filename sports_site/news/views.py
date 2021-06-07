from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render#, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm
from .decorators import user_owns_article


# Create your views here.
def home(request):
    league_slug = request.GET.get('league', None)
    Article_data = Article.objects.all().filter(league__url=league_slug).order_by('-id')[:10]
    context = {
        "articles": Article_data,
        }
    return render(request, 'news/home.html', context)


def news_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        "article": article
        }
    return render(request, 'news/news_detail.html', context)


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'league.league_admin'
    template_name = 'news/new_article.html'
    model = Article
    form_class = ArticleCreateForm

    def get_success_url(self):
        league_slug = self.request.GET.get('league', None)
        if league_slug:
            url = f"/league/?league={league_slug}"
        else:
            url = f"/league/?league={self.request.user.userprofile.league.url}"

        return url


    def form_valid(self, form):
        self.object = form.save()
        self.object.league = self.request.user.userprofile.league
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ArticleEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'league.league_admin'
    template_name = 'news/article_edit.html'
    model = Article
    form_class = ArticleCreateForm


    @method_decorator(user_owns_article)
    def dispatch(self, *args, **kwargs):
        return super(ArticleEditView, self).dispatch(*args, **kwargs)


    def get_success_url(self):
        league_slug = self.request.GET.get('league', None)
        if league_slug:
            url = f"/league/?league={league_slug}"
        else:
            print("league slug not")
            url = f"/league/?league={self.request.user.userprofile.league.url}"

        return url


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'league.league_admin'
    template_name = 'news/confirm_delete.html'
    model = Article

    @method_decorator(user_owns_article)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        league_slug = self.request.GET.get('league', None)
        if league_slug:
            url = f"/league/?league={league_slug}"
        else:
            print("league slug not")
            url = f"/league/?league={self.request.user.userprofile.league.url}"

        return url


class ArticlesView(ListView):
    template_name = 'news/news_page.html'
    paginate_by=5
    model = Article
    context_object_name= 'articles'

    def get_queryset(self):
        league_slug = self.request.GET.get('league', None)
        queryset = Article.objects.all().filter(league__url=league_slug).order_by('-id')
        return queryset



