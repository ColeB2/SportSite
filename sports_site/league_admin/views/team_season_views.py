from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.db import router
from django.shortcuts import render, redirect
from league.models import TeamSeason
from ..decorators import user_owns_season_stage, user_owns_team_season



@permission_required('league.league_admin')
@user_owns_team_season
def league_admin_team_season_info_view(request, season_year, season_pk,
                                       season_stage_pk, team_name,
                                       team_season_pk):

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
    return render(
        request,
        "league_admin/team_season_templates/team_season_info.html",
        context)


@permission_required('league.league_admin')
@user_owns_season_stage
def league_admin_team_season_delete_info_view(request, season_year, season_pk,
                                              season_stage_pk, team_name,
                                              team_season_pk):

    teamseason = TeamSeason.objects.get(pk=team_season_pk)

    using = router.db_for_write(teamseason._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([teamseason])

    if request.method == 'POST':
        teamseason.delete()
        messages.success(request,
                         f"{teamseason} and all related objects were deleted.")

        return redirect('league-admin-season-stage', season_year, season_pk)

    context = {
        'season_year':season_year,
        'season_pk': season_pk,
        'season_stage_pk': season_stage_pk,
        'team_name': team_name,
        'teamseason':teamseason,
        'nested_object':nested_object,
    }
    return render(
        request,
        "league_admin/team_season_templates/team_season_delete.html",
        context)

