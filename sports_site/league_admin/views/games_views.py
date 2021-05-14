from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..forms import (CreateGameForm, EditGameForm)
from league.models import (SeasonStage, Game, TeamSeason)


@login_required
def league_admin_schedule_select_view(request):
    stages = SeasonStage.objects.all().filter(season__league__admin=request.user)

    context = {
        "stages":stages,
        }
    return render(request, "league_admin/schedule_select.html", context)

@login_required
def league_admin_schedule_view(request, season_year, season_stage_pk):
    schedule = Game.objects.all().filter(season__season__league__admin=request.user, season__season=season_stage_pk )
    context = {
        "schedule": schedule,
        "season_year": season_year,
        "season_stage_pk":season_stage_pk
        }

    return render(request, "league_admin/schedule_view.html", context)

@login_required
def league_admin_schedule_create_view(request, season_year, season_stage_pk):

    GameFormset = formset_factory(CreateGameForm, extra=5)
    current_stage = SeasonStage.objects.get(pk=season_stage_pk)
    teamseason_query = TeamSeason.objects.all().filter(season=current_stage)

    formset = GameFormset(data=request.POST or None, form_kwargs={'team_queryset':teamseason_query})

    if request.method == 'POST':

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.process(current_stage=current_stage)
        return redirect('league-admin-schedule', season_year, season_stage_pk)

    else:
        pass

    context={
        "formset": formset,
        "current_stage": current_stage,
        }
    return render(request, "league_admin/schedule_create.html", context)


def league_admin_edit_game_view(request, season_year, season_stage_pk, game_pk):
    game_instance = Game.objects.get(pk=game_pk)


    if request.method == "POST":
        form = EditGameForm(data=request.POST, instance=game_instance)
        if form.is_valid():
            game = form.save(commit=False)
            game.save()

        return redirect('league-admin-schedule', season_year, season_stage_pk)
    else:
        form = EditGameForm(instance=game_instance)


    context = {
        "form":form,
        }
    return render(request, "league_admin/game_edit.html", context)