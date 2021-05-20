from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import login_required, permission_required
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import (SeasonCreateForm, SeasonStageCreateForm, TeamSelectForm)
from league.models import (League, Season, SeasonStage, Team, TeamSeason)



"""Season Views"""
@login_required
@permission_required('league.league_admin')
def league_admin_season_view(request):
    seasons = Season.objects.all().filter(league__admin=request.user)
    stages = SeasonStage.objects.all().filter(season__league__admin=request.user)

    context = {
        'seasons':seasons,
        'stages':stages,
        }
    return render(request, "league_admin/season_page.html", context)


@login_required
@permission_required('league.league_admin')
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
                messages.success(request, f"{new_season} created.")
            else:
                messages.info(request, f"{new_season} already exists.")


        return redirect('league-admin-season')
    else:
        form = SeasonCreateForm()

    context = {
        'seasons':seasons,
        "form": form
    }
    return render(request, "league_admin/season_create.html", context)


@login_required
@permission_required('league.league_admin')
def league_admin_season_delete_info_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)

    using = router.db_for_write(season._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([season])

    if request.method == 'POST':
        season.delete()
        messages.success(request, f"{season} and all releated object were deleted")
        return redirect('league-admin-season')
    else:
        pass

    context = {
        'season':season,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/season_delete.html", context)


"""SeasonStage Views"""
@login_required
@permission_required('league.league_admin')
def league_admin_season_stage_select_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    stages = SeasonStage.objects.all().filter(season=season)

    context = {
        'season':season,
        'season_year': season_year,
        'stages':stages,
        }
    return render(request, "league_admin/season_stage_select_page.html", context)


@login_required
@permission_required('league.league_admin')
def league_admin_create_season_stage_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    league = League.objects.get(admin=request.user)
    stages = SeasonStage.objects.all().filter(season__pk=season_pk)
    teams = Team.objects.all().filter(league=league)
    TeamFormset = formset_factory(TeamSelectForm, extra=len(teams))

    if request.method == 'POST':
        formset = TeamFormset(data=request.POST, form_kwargs={'team_queryset':teams})
        form = SeasonStageCreateForm(data = request.POST)
        if form.is_valid():
            stage_data = form.cleaned_data.get('stage')
            new_stage, created = SeasonStage.objects.get_or_create(stage=stage_data, season=season)
            if created:
                new_stage.save()
                messages.success(request, f"{new_stage} created.")

                if formset.is_valid():
                    for form in formset:
                        team_data = form.cleaned_data.get('teams')

                        if team_data:
                            new_teamseason, created = TeamSeason.objects.get_or_create(season=new_stage, team=team_data)
                            if created:
                                new_teamseason.save()
                                messages.success(request, f"{new_teamseason} created")
                            else:
                                messages.info(request, f"{new_teamseason} already exists")

            else:
                messages.info(request, f"{new_stage} already exists.")


        return redirect('league-admin-season-stage', season_year)
    else:
        form = SeasonStageCreateForm()
        formset = TeamFormset(form_kwargs={'team_queryset':teams})

    context = {
        'season':'season',
        'season_year': season_year,
        'stages':stages,
        "form": form,
        "formset": formset,
    }
    return render(request, "league_admin/season_stage_create.html", context)

@login_required
@permission_required('league.league_admin')
def league_admin_season_stage_info_view(request, season_year, season_pk, season_stage):
    league = League.objects.get(admin=request.user)
    teams = TeamSeason.objects.all().filter(team__league=league, season__season__year=season_year, season__stage=season_stage)
    teams2 = TeamSeason.objects.all()
    context = {
        'season_year': season_year,
        'season_stage': season_stage,
        'teams': teams,
        'teams2': teams2,
        }
    return render(request, "league_admin/season_stage_page.html", context)


