from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import UpdateView
from ..forms import SeasonStageCreateForm, TeamSelectForm, SeasonForm
from league.models import (League, Season, SeasonStage, Team, TeamSeason)
from ..decorators import (user_owns_season, user_owns_season_stage,
    user_owns_team_season)



@permission_required('league.league_admin')
def league_admin_season_view(request):
    seasons = Season.objects.all().filter(league__admin=request.user)
    stages = SeasonStage.objects.all().filter(
        season__league__admin=request.user)

    context = {
        'seasons':seasons,
        'stages':stages,
        }
    return render(request, "league_admin/season_page.html", context)


@permission_required('league.league_admin')
def league_admin_create_season_view(request):
    seasons = Season.objects.all().filter(league__admin=request.user)

    if request.method == 'POST':
        form = SeasonForm(data = request.POST)
        if form.is_valid():
            new_season, created = form.process(
                league=request.user.userprofile.league)

            if created:
                messages.success(request, f"{new_season} created.")
            else:
                messages.info(request, f"{new_season} already exists.")

        return redirect('league-admin-season')
    else:
        form = SeasonForm()

    context = {
        'seasons':seasons,
        "form": form
    }
    return render(request, "league_admin/season_create.html", context)


@permission_required('league.league_admin')
@user_owns_season
def league_admin_season_delete_info_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)

    using = router.db_for_write(season._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([season])

    if request.method == 'POST':
        season.delete()
        messages.success(request,
                         f"{season} and all releated object were deleted")
        return redirect('league-admin-season')

    context = {
        'season':season,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/season_delete.html", context)


class SeasonEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'league.league_admin'
    template_name = 'league_admin/season_edit.html'
    model = Season
    form_class = SeasonForm


    @method_decorator(user_owns_season)
    def dispatch(self, *args, **kwargs):
        return super(SeasonEditView, self).dispatch(*args, **kwargs)


    def get_success_url(self):
        url = reverse('league-admin-season-stage',
                      args=[self.object.year, self.object.pk])
        return url


"""SeasonStage Views"""
@permission_required('league.league_admin')
@user_owns_season
def league_admin_season_stage_select_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    stages = SeasonStage.objects.all().filter(season=season)

    context = {
        'season':season,
        'season_year': season_year,
        'stages':stages,
        }
    return render(request, "league_admin/season_stage_select_page.html", context)


@permission_required('league.league_admin')
@user_owns_season
def league_admin_create_season_stage_view(request, season_year, season_pk):
    season = Season.objects.get(pk=season_pk)
    league = League.objects.get(admin=request.user)
    stages = SeasonStage.objects.all().filter(season__pk=season_pk)
    teams = Team.objects.all().filter(league=league)
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
    return render(request, "league_admin/season_stage_create.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_info_view(request, season_year, season_pk,
                                                               season_stage_pk):

    league = League.objects.get(admin=request.user)
    stage = SeasonStage.objects.get(pk=season_stage_pk)
    teams = TeamSeason.objects.all().filter(team__league=league,
                                            season__pk=season_stage_pk)

    context = {
        'stage': stage,
        'teams': teams,
        }
    return render(request, "league_admin/season_stage_page.html", context)


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
    return render(request, "league_admin/season_stage_delete.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_add_teams_view(request, season_year, season_pk,
                                                               season_stage_pk):
    season = Season.objects.get(pk=season_pk)
    stage = SeasonStage.objects.get(pk=season_stage_pk)

    league = League.objects.get(pk = request.user.userprofile.league.pk)
    teams = Team.objects.all().filter(league=league)
    existing_teams = TeamSeason.objects.all().filter(season=stage)

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
    return render(request, "league_admin/season_stage_add_teams.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_season_stage_set_featured_view(request,season_year, season_pk,
                                                               season_stage_pk):

    stage = SeasonStage.objects.get(pk=season_stage_pk)
    stage.featured = True
    stage.save()

    return redirect('league-admin-season-stage-info', season_year, season_pk,
                    season_stage_pk)



"""Team Season"""
@permission_required('league.league_admin')
@user_owns_team_season
def league_admin_team_season_info_view(request, season_year, season_pk,
                                    season_stage_pk, team_name, team_season_pk):

    team = TeamSeason.objects.get(pk=team_season_pk)
    roster = team.roster_set.get(team__pk=team_season_pk)
    players = roster.playerseason_set.all()

    context = {
        'season_year':season_year,
        'season_pk': season_pk,
        'season_stage_pk': season_stage_pk,
        'team_name': team_name,
        'team':team,
        'roster':roster,
        'players': players,
        }
    return render(request, "league_admin/team_season_info.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_team_season_delete_info_view(request, season_year, season_pk,
                                    season_stage_pk, team_name, team_season_pk):

    teamseason = TeamSeason.objects.get(pk=team_season_pk)

    using = router.db_for_write(teamseason._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([teamseason])

    if request.method == 'POST':
        teamseason.delete()
        messages.success(request,
                         f"{teamseason} and all releated object were deleted")

        return redirect('league-admin-season-stage', season_year, season_pk)

    context = {
        'season_year':season_year,
        'season_pk': season_pk,
        'season_stage_pk': season_stage_pk,
        'team_name': team_name,
        'teamseason':teamseason,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/team_season_delete.html", context)


