from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import SeasonStageCreateForm, TeamSelectForm
from league.models import League, Season, SeasonStage, Team, TeamSeason
from ..decorators import user_owns_season, user_owns_season_stage



@permission_required('league.league_admin')
@user_owns_season
def league_admin_season_stage_select_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    stages = SeasonStage.objects.filter(season=season)

    context = {
        'season':season,
        'season_year': season_year,
        'stages':stages,
        }
    return render(
        request,
        "league_admin/season_stage_templates/season_stage_select_page.html",
        context)


@permission_required('league.league_admin')
@user_owns_season
def league_admin_create_season_stage_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    league = League.objects.get(admin=request.user)
    stages = SeasonStage.objects.filter(season__pk=season_pk)
    teams = Team.objects.filter(league=league)
    TeamFormset = formset_factory(TeamSelectForm, extra=len(teams))

    if request.method == 'POST':
        formset = TeamFormset(data=request.POST,
                              form_kwargs={'team_queryset':teams})
        form = SeasonStageCreateForm(data = request.POST)
        if form.is_valid():
            new_stage, created = form.process(season=season)
            if created:
                new_stage.save()
                messages.success(request, f"{new_stage} created.")

                if formset.is_valid():
                    for form in formset:
                        new_teamseason, created = form.process(season=new_stage)

                        if new_teamseason:
                            if created:
                                messages.success(request,
                                                 f"{new_teamseason} created")
                            else:
                                messages.info(request,
                                    f"{new_teamseason} already exists")
            else:
                messages.info(request, f"{new_stage} already exists.")


        return redirect('league-admin-season-stage', season_year, season_pk)

    else:
        form = SeasonStageCreateForm()
        formset = TeamFormset(form_kwargs={'team_queryset':teams})

    context = {
        'season':season,
        'season_year': season_year,
        'stages':stages,
        "form": form,
        "formset": formset,
    }
    return render(
        request,
        "league_admin/season_stage_templates/season_stage_create.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_info_view(request, season_year, season_pk,
                                        season_stage_pk):

    league = League.objects.get(admin=request.user)
    stage = SeasonStage.objects.get(pk=season_stage_pk)
    teams = TeamSeason.objects.filter(team__league=league,
                                      season__pk=season_stage_pk)

    context = {
        'stage': stage,
        'teams': teams,
        }
    return render(
        request,
        "league_admin/season_stage_templates/season_stage_page.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_delete_info_view(request, season_year, season_pk,
                                               season_stage_pk):

    stage = SeasonStage.objects.get(pk=season_stage_pk)

    using = router.db_for_write(stage._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([stage])

    if request.method == 'POST':
        stage.delete()
        messages.success(request,
                         f"{stage} and all releated object were deleted")
        return redirect('league-admin-season-stage', season_year, season_pk)

    context = {
        'stage':stage,
        'nested_object':nested_object,
    }
    return render(
        request,
        "league_admin/season_stage_templates/season_stage_delete.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_add_teams_view(request, season_year, season_pk,
                                             season_stage_pk):
    season = Season.objects.get(pk=season_pk)
    stage = SeasonStage.objects.get(pk=season_stage_pk)

    league = League.objects.get(pk = request.user.userprofile.league.pk)
    teams = Team.objects.filter(league=league)
    existing_teams = TeamSeason.objects.filter(season=stage)

    TeamFormset = formset_factory(TeamSelectForm, extra=len(teams))

    if request.method == 'POST':
        formset = TeamFormset(data=request.POST,
                              form_kwargs={'team_queryset':teams})
        if formset.is_valid():
            for form in formset:
                new_teamseason, created = form.process(season=stage)

                if new_teamseason:
                    if created:
                        messages.success(request, f"{new_teamseason} created")
                    else:
                        messages.info(request,
                                      f"{new_teamseason} already exists")


        return redirect('league-admin-season-stage-info', season_year,
                        season_pk, season_stage_pk)

    else:
        formset = TeamFormset(form_kwargs={'team_queryset':teams})

    context = {
        'season':season,
        'season_year': season_year,
        'stage':stage,
        'teams': existing_teams,
        'formset': formset,
    }
    return render(
        request,
        "league_admin/season_stage_templates/season_stage_add_teams.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_set_featured_view(request,season_year, season_pk,
                                                season_stage_pk):

    stage = SeasonStage.objects.get(pk=season_stage_pk)
    stage.featured = True
    stage.save()

    return redirect(
        'league-admin-season-stage-info',
        season_year,
        season_pk,
        season_stage_pk)





