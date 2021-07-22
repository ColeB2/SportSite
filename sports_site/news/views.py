from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import  F, FloatField, Sum
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import render#, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Article
from league.models import League, SeasonStage
from stats.stat_calc import _calc_average, _convert_to_str
from stats.models import PlayerHittingGameStats
from stats.tables import PlayerHittingStatsTable
from .forms import ArticleCreateForm
from .decorators import user_owns_article


# Create your views here.
def home(request):
    league_slug = request.GET.get('league', None)
    league = League.objects.get(url=league_slug)
    Article_data = Article.objects.all().filter(league__url=league_slug).order_by('-id')[:10]

    """Leaders"""
    stats = league_leaders_widget(league)
    avg = stats.order_by('-average')[0]
    avg["average"] = _convert_to_str(avg["average"])
    homeruns = stats.order_by('-homeruns')[0]
    runs_batted_in = stats.order_by('-runs_batted_in')[0]
    runs = stats.order_by('-runs')[0]
    stolen_bases = stats.order_by('-stolen_bases')[0]



    context = {
        "articles": Article_data,
        "league": league,
        "stats": stats,
        "avg":avg,
        "homeruns":homeruns,
        "runs_batted_in": runs_batted_in,
        "runs": runs,
        "stolen_bases":stolen_bases,
        }
    return render(request, 'news/home.html', context)


def league_leaders_widget(league):
    """Returns league leaders in Avg, HomeRuns, RBI, SB and Runs"""
    featured_stage = SeasonStage.objects.get(season__league=league, featured=True)
    hitting_stats = PlayerHittingGameStats.objects.all().filter(player__player__league=league, season=featured_stage)
    hitting_stats1 = hitting_stats.values("player").annotate(
        first = F("player__player__first_name"),
        last = F("player__player__last_name"),
        team = F("player__team__team__team__name"),
        at_bats = Sum('at_bats'),
        runs = Sum('runs'),
        hits = Sum('hits'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        stolen_bases = Sum('stolen_bases'),
        average = Cast(F('hits'),FloatField())/ Cast(F('at_bats'), FloatField())
        )
    return hitting_stats1



def news_detail(request, slug):
    article = Article.objects.get(slug=slug)
    league = League.objects.get(pk=article.league.pk)
    context = {
        "article": article,
        "league": league,
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['league'] = League.objects.get(url=self.request.GET.get('league', None))
        return data



