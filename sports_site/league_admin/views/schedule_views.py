from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import CreateGameForm
from league.models import (SeasonStage, Game, TeamSeason)
from ..decorators import user_owns_season_stage


@permission_required('league.league_admin')
def league_admin_schedule_select_view(request):
    stages = SeasonStage.objects.filter(season__league__admin=request.user)

    context = {
        "stages":stages,
        }
    return render(
        request,
        "league_admin/schedule_templates/schedule_select.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_view(request, season_year, season_stage_pk):
    stage = SeasonStage.objects.get(pk=season_stage_pk)
    schedule = Game.objects.filter(season__pk=season_stage_pk)
    context = {
        "schedule": schedule,
        "season_year": season_year,
        "season_stage_pk":season_stage_pk,
        "stage":stage,
        }

    return render(
        request,
        "league_admin/schedule_templates/schedule_view.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_create_view(request, season_year, season_stage_pk):

    GameFormset = formset_factory(CreateGameForm, extra=5)
    current_stage = SeasonStage.objects.get(pk=season_stage_pk)
    teamseason_query = TeamSeason.objects.filter(season=current_stage)

    formset = GameFormset(data=request.POST or None,
                          form_kwargs={'team_queryset':teamseason_query})

    if request.method == 'POST':

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    ng = form.process(current_stage=current_stage)
                    if ng:
                        messages.success(request,
                            f"{ng} created and added to {current_stage}")

        if 'create' in request.POST:
            return redirect('league-admin-schedule',
                            season_year, season_stage_pk)

        elif 'create-and-continue' in request.POST:
            return redirect('league-admin-schedule-create',
                            season_year, season_stage_pk)

    context={
        "formset": formset,
        "current_stage": current_stage,
        }
    return render(
        request,
        "league_admin/schedule_templates/schedule_create.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_delete_info_view(request, season_year,
                                           season_stage_pk):
    """
    To Do: Delete schedule. Different from other deletes,
    as schedule isn't and object/model. So will need to
    delete all games in a given season stage.
    """
    stage = SeasonStage.objects.get(pk=season_stage_pk)
    nested_games = []
    games = stage.game_set.all()

    for game in games:
        using = router.db_for_write(game._meta.model)
        nested_object = NestedObjects(using)
        nested_object.collect([game])
        nested_games.append(nested_object)

    if request.method == 'POST':
        for game in games:
            game.delete()
            messages.success(request,
                             f"{game} and all related objects were deleted.")
        return redirect('league-admin-schedule', season_year, season_stage_pk)

    context = {
        'season_year': season_year,
        'season_stage_pk': season_stage_pk,
        'games':games,
        'stage':stage,
        'nested_games':nested_games,
    }
    return render(
        request,
        "league_admin/schedule_templates/schedule_delete.html",
        context)
