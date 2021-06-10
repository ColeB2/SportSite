from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import (CreateGameForm, EditGameForm)
from league.models import (SeasonStage, Game, TeamSeason)
from ..decorators import user_owns_season_stage



@permission_required('league.league_admin')
def league_admin_schedule_select_view(request):
    stages = SeasonStage.objects.all().filter(season__league__admin=request.user)

    context = {
        "stages":stages,
        }
    return render(request, "league_admin/schedule_select.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_view(request, season_year, season_stage_pk):
    stage = SeasonStage.objects.get(pk=season_stage_pk)
    schedule = Game.objects.all().filter(season__pk=season_stage_pk )
    context = {
        "schedule": schedule,
        "season_year": season_year,
        "season_stage_pk":season_stage_pk,
        "stage":stage,
        }

    return render(request, "league_admin/schedule_view.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_create_view(request, season_year, season_stage_pk):

    GameFormset = formset_factory(CreateGameForm, extra=5)
    current_stage = SeasonStage.objects.get(pk=season_stage_pk)
    teamseason_query = TeamSeason.objects.all().filter(season=current_stage)

    formset = GameFormset(data=request.POST or None, form_kwargs={'team_queryset':teamseason_query})

    if request.method == 'POST':

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    ng = form.process(current_stage=current_stage)
                    if ng:
                        messages.success(request, f"{ng} created and added to {current_stage}")

        if 'create' in request.POST:
            return redirect('league-admin-schedule', season_year, season_stage_pk)
        elif 'create-and-continue' in request.POST:
            return redirect('league-admin-schedule-create', season_year, season_stage_pk)

    else:
        pass

    context={
        "formset": formset,
        "current_stage": current_stage,
        }
    return render(request, "league_admin/schedule_create.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_schedule_delete_info_view(request, season_year, season_stage_pk):
    """ To Do: Delete schedule. Different from other deletes, as schedule isn't
    and object/model. So will need to delete all games in a given season stage."""
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
            messages.success(request, f"{game} and all releated object were deleted")
        return redirect('league-admin-schedule', season_year, season_stage_pk)
    else:
        pass

    context = {
        'season_year': season_year,
        'season_stage_pk': season_stage_pk,
        'games':games,
        'stage':stage,
        'nested_games':nested_games,
    }
    return render(request, "league_admin/schedule_delete.html", context)






"""League Admin Game Views"""
@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_edit_game_view(request, season_year, season_stage_pk, game_pk):
    game_instance = Game.objects.get(pk=game_pk)


    if request.method == "POST":
        form = EditGameForm(data=request.POST, instance=game_instance)

        form.fields["home_team"].queryset = TeamSeason.objects.all().filter(season__pk=season_stage_pk)
        form.fields["away_team"].queryset = TeamSeason.objects.all().filter(season__pk=season_stage_pk)

        if form.is_valid():
            game = form.process()
            messages.success(request, f"{game} changed.")

        return redirect('league-admin-schedule', season_year, season_stage_pk)
    else:
        form = EditGameForm(instance=game_instance)
        form.fields["home_team"].queryset = TeamSeason.objects.all().filter(season__pk=season_stage_pk)
        form.fields["away_team"].queryset = TeamSeason.objects.all().filter(season__pk=season_stage_pk)


    context = {
        "form":form,
        "game_instance":game_instance,
        "season_year": season_year,
        "season_stage_pk":season_stage_pk
        }
    return render(request, "league_admin/game_edit.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_delete_game_info_view(request, season_year, season_stage_pk, game_pk):
    game = Game.objects.get(pk=game_pk)

    using = router.db_for_write(game._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([game])

    if request.method == 'POST':
        game.delete()
        messages.success(request, f"{game} and all releated object were deleted")
        return redirect('league-admin-schedule', season_year, season_stage_pk)
    else:
        pass

    context = {
        "season_year":season_year,
        "season_stage_pk":season_stage_pk,
        "game":game,
        "nested_object":nested_object,
    }
    return render(request, "league_admin/game_delete.html", context)

