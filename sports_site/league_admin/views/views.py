from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, TemplateView
from league.models import (League, Roster)
from news.models import Article
from ..filters import RosterFilter, ArticleFilter
from ..forms import LeagueHittingOptionsForm, LeagueHittingStatsOptionsForm
from ..models import LeagueHittingOptions, LeagueHittingStatsOptions



@login_required
@permission_required('league.league_admin')
def league_admin_dashboard_view(request):
    context = {}
    return render(request, "league_admin/dashboard.html",context)


@login_required
@permission_required('league.league_admin')
def league_admin_roster_select(request):
    roster_qs = Roster.objects.all().filter(
        team__team__league=request.user.userprofile.league)
    f = RosterFilter(request.GET, request=request, queryset=roster_qs)
    roster_list = f.qs

    paginator = Paginator(roster_list, 10)
    page = request.GET.get('page', 1)

    try:
        all_rosters = paginator.page(page)
    except PageNotAnInteger:
        all_rosters = paginator.page(1)
    except EmptyPage:
        all_rosters = paginator.page(paginator.num_pages)


    context = {
        "filter": f,
        "paginator": paginator,
        "all_rosters": all_rosters
        }
    return render(request, "league_admin/roster_select.html", context)


@permission_required('league.league_admin')
def league_admin_news_select(request):
    league = League.objects.get(admin=request.user)
    articles = Article.objects.all().filter(league=league).order_by('-id')
    f = ArticleFilter(request.GET, queryset=articles)
    article_list = f.qs

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page', 1)

    try:
        all_articles = paginator.page(page)
    except PageNotAnInteger:
        all_articles = paginator.page(1)
    except EmptyPage:
        all_articles = paginator.page(paginator.num_pages)

    context = {
        "filter": f,
        "paginator":paginator,
        "all_articles":all_articles
        }
    return render(request, "league_admin/article_select.html", context)






