from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .filters import RosterFilter
from .forms import SeasonCreateForm, SeasonStageCreateForm
from league.models import League, Roster, Season, SeasonStage

# Create your views here.


@login_required
def league_admin_dashboard_view(request):
    context = {}
    return render(request, "league_admin/dashboard.html",context)

@login_required
def league_admin_roster_select(request):
    f = RosterFilter(request.GET, queryset=Roster.objects.all() )
    context = {
        'filter': f,
        }
    return render(request, "league_admin/roster_select.html", context)


@login_required
def league_admin_season_view(request):
    seasons = Season.objects.all().filter(league__admin=request.user)
    stages = SeasonStage.objects.all().filter(season__league__admin=request.user)

    context = {
        'seasons':seasons,
        'stages':stages,
        }
    return render(request, "league_admin/season_page.html", context)


@login_required
def league_admin_create_season_view(request):
    league = League.objects.get(admin=request.user)
    seasons = Season.objects.all().filter(league__admin=request.user)

    if request.method == 'POST':
        form = SeasonCreateForm(data = request.POST)
        if form.is_valid():
            year_data = form.cleaned_data.get('year')

            new_season, created = Season.objects.get_or_create(year=year_data, league=league)
            if created:
                new_season.save()


        return redirect('league-admin-season')
    else:
        form = SeasonCreateForm()

    context = {
        'seasons':seasons,
        "form": form
    }
    return render(request, "league_admin/season_create.html", context)



@login_required
def league_admin_season_stage_view(request, season_year):
    stages = SeasonStage.objects.all().filter(season__year=season_year, season__league__admin=request.user)

    context = {
        'season_year': season_year,
        'stages':stages,
        }
    return render(request, "league_admin/season_stage_page.html", context)


@login_required
def league_admin_create_season_stage_view(request, season_year):
    league = League.objects.get(admin=request.user)
    stages = SeasonStage.objects.all().filter(season__league__admin=request.user, season__year=season_year)

    if request.method == 'POST':
        form = SeasonStageCreateForm(data = request.POST)
        if form.is_valid():
            stage_data = form.cleaned_data.get('stage')
            season_obj = Season.objects.get(league=league, year=season_year)


            new_stage, created = SeasonStage.objects.get_or_create(stage=stage_data, season=season_obj)
            if created:
                new_stage.save()


        return redirect('league-admin-season-stage', season_year)
    else:
        form = SeasonStageCreateForm()

    context = {
        'season_year': season_year,
        'stages':stages,
        "form": form
    }
    return render(request, "league_admin/season_stage_create.html", context)
