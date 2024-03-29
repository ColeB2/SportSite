from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.shortcuts import render, redirect
from ..forms import EditGameForm
from league.models import Game, TeamSeason
from ..decorators import user_owns_season_stage




@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_edit_game_view(request, season_year, season_stage_pk, game_pk):
    game_instance = Game.objects.get(pk=game_pk)
    team_seasons = TeamSeason.objects.filter(season__pk=season_stage_pk)


    if request.method == "POST":
        form = EditGameForm(data=request.POST, instance=game_instance)

        form.fields["home_team"].queryset = team_seasons
        form.fields["away_team"].queryset = team_seasons

        if form.is_valid():
            game = form.process()
            messages.success(request, f"{game} changed.")

        return redirect('league-admin-schedule', season_year, season_stage_pk)
    else:
        form = EditGameForm(instance=game_instance)
        form.fields["home_team"].queryset = team_seasons
        form.fields["away_team"].queryset = team_seasons

    context = {
        "form":form,
        "game_instance":game_instance,
        "season_year": season_year,
        "season_stage_pk":season_stage_pk
        }
    return render(
        request, "league_admin/game_templates/game_edit.html", context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_delete_game_info_view(
        request, season_year, season_stage_pk, game_pk):
    
    game = Game.objects.get(pk=game_pk)

    using = router.db_for_write(game._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([game])

    if request.method == 'POST':
        game.delete()
        messages.success(request,
                         f"{game} and all related objects were deleted.")
        return redirect('league-admin-schedule', season_year, season_stage_pk)

    context = {
        "season_year":season_year,
        "season_stage_pk":season_stage_pk,
        "game":game,
        "nested_object":nested_object,
    }
    return render(
        request, "league_admin/game_templates/game_delete.html", context)

