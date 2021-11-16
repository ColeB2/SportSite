from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import login_required
from django.db import router
from django.forms import formset_factory
from django.shortcuts import render, redirect
from league.models import Player, PlayerSeason, Roster, SeasonStage, Team
from .decorators import user_owns_roster
from .forms import ( PlayerCreateForm, PlayerRemoveForm, PlayerSelectForm,
    RosterCreateForm, RosterSelectForm)



@login_required
def user_dashboard_view(request):
    context = {}
    return render(request, "user/dashboard.html",context)


@login_required
def roster_select(request):
    roster = Roster.objects.all().filter(
        team__team__league=request.user.userprofile.league,
        team__team__owner=request.user)
    context = {
        'rosters': roster,
        }
    return render(request, "user/roster_select.html", context)


@login_required
@user_owns_roster
def roster_view(request, team_name, season, roster_pk):
    roster = Roster.objects.get(pk=roster_pk)

    players = roster.playerseason_set.all()
    context = {
        'roster': roster,
        'players': players
        }
    return render(request, 'user/roster_view.html', context)


@login_required
@user_owns_roster
def roster_edit_copy(request, team_name, season, roster_pk):
    roster = Roster.objects.get(pk=roster_pk)
    rosters = Roster.objects.all().filter(team__team__pk=roster.team.team.pk)

    if request.method == 'POST':
        form = RosterSelectForm(data=request.POST, roster_queryset=rosters)
        if form.is_valid():
            return_data = form.process(current_roster=roster)
            if return_data:
                for data in return_data:
                    messages.success(request,
                        f"{data} created and added to {roster}")

            return redirect('user-roster-view', team_name=team_name,
                            season=season, roster_pk=roster_pk)
    else:
        form = RosterSelectForm(roster_queryset=rosters)


    context = {
        'roster': roster,
        'rosters': rosters,
        'form':form
        }
    return render(request, 'user/roster_edit_copy.html', context)


@login_required
@user_owns_roster
def roster_edit_add(request, team_name, season, roster_pk):
    """
    View used to create a brand new PlayerSeason object
    for the season the roster is a part of.
    Used as a part of the "Add Existing Players" functionality.
    """
    roster = Roster.objects.get(pk=roster_pk)
    league = roster.team.team.league
    players = roster.playerseason_set.all().filter(player__league=league)
    player_qs = Player.objects.all().filter(league=league)

    exclude_list = []
    for player in players:
        exclude_list.append(player.player)

    PlayerFormset = formset_factory(PlayerSelectForm,
                                    extra=(21-len(exclude_list)) )


    if request.method == 'POST':
        formset = PlayerFormset(request.POST, form_kwargs={
            'player_qs':player_qs,
            'exclude_list':exclude_list})
        if formset.is_valid():
            for form in formset:
                playerseason = form.process(roster=roster)
                messages.success(request,
                    f"{playerseason.player} added to {roster}")

            return redirect('user-roster-view',
                            team_name=team_name,
                            season=season,
                            roster_pk=roster_pk)

    else:
        formset = PlayerFormset(form_kwargs={
            'player_qs':player_qs,
            'exclude_list':exclude_list})

    context = {
        'roster': roster,
        'players': players,
        'formset':formset
        }
    return render(request, 'user/roster_edit_add.html', context)


@login_required
@user_owns_roster
def roster_edit_create(request, team_name, season, roster_pk):
    """
    View used to create a brand new Player object, and a
    PlayerSeason object for the season the roster is a part
    of.
    Used as a part of the "Add New Players" functionality.
    """
    roster = Roster.objects.get(pk=roster_pk)
    players = roster.playerseason_set.all()
    CreatePlayerFormset = formset_factory(PlayerCreateForm,
                                          extra=(21-len(players)))


    if request.method == 'POST':
        formset = CreatePlayerFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.process(league=roster.team.team.league, roster=roster)

            return redirect('user-roster-view',
                            team_name=team_name,
                            season=season,
                            roster_pk=roster_pk)

    else:
        formset = CreatePlayerFormset()

    context = {
        'roster': roster,
        'players': players,
        'formset':formset,
        }
    return render(request, 'user/roster_edit_create.html', context)


@login_required
@user_owns_roster
def roster_edit_remove(request, team_name, season, roster_pk):
    """Creates PlayerSeason object based on existing Player"""
    roster = Roster.objects.get(pk=roster_pk)
    players = roster.playerseason_set.all()


    PlayerFormset = formset_factory(PlayerRemoveForm, extra=len(players))


    if request.method == 'POST':
        formset = PlayerFormset(request.POST,
            form_kwargs={'roster_queryset':players})

        if formset.is_valid():
            for form in formset:
                form.process()

            if 'remove' in request.POST:
                return redirect('user-roster-view', team_name=team_name,
                                season=season, roster_pk=roster_pk)
            elif 'remove_and_continue' in request.POST:
                return redirect('roster-edit-remove', team_name=team_name,
                                season=season, roster_pk=roster_pk)

    else:
        formset = PlayerFormset(form_kwargs={'roster_queryset':players})

    context = {
        'roster': roster,
        'players': players,
        'formset':formset
        }
    return render(request, 'user/roster_edit_remove.html', context)



@login_required
@user_owns_roster
def roster_playerseason_delete_info(request, team_name, season, roster_pk,
                                                            playerseason_pk):

    playerseason = PlayerSeason.objects.get(pk=playerseason_pk)

    using = router.db_for_write(playerseason._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([playerseason])

    if request.method == 'POST':
        playerseason.delete()
        messages.success(request,
                         f"{playerseason} and all releated object were deleted")
        return redirect('roster-edit-remove',
                        team_name=team_name,
                        season=season, roster_pk=roster_pk,
                        playerseason_pk=playerseason_pk)

    context = {
        'playerseason':playerseason,
        'nested_object':nested_object,
    }
    return render(request, "user/playerseason_delete.html", context)



@login_required
def roster_create(request, team_name):
    user_team = Team.objects.get(owner=request.user)
    rosters = Roster.objects.all().filter(team__team=user_team)
    seasons = SeasonStage.objects.all().filter(
        season__league=request.user.userprofile.league)


    if request.method == 'POST':
        form = RosterCreateForm(season_queryset=seasons,
                                roster_queryset=rosters,
                                data=request.POST)

        if form.is_valid():
            form.process(user_team)
            return redirect("roster-select")

    else:
        form = RosterCreateForm(season_queryset=seasons,
                                roster_queryset=rosters)

    context = {
        "rosters":rosters,
        "form": form,
        }
    return render(request, 'user/roster_new.html', context)


@login_required
@user_owns_roster
def roster_delete_info_view(request, team_name, season_year, roster_pk):
    roster = Roster.objects.get(pk=roster_pk)

    using = router.db_for_write(roster._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([roster])

    if request.method == 'POST':
        roster.delete()
        messages.success(request,
                         f"{roster} and all releated object were deleted")
        return redirect('roster-select')

    context = {
        'roster':roster,
        'nested_object':nested_object,
    }
    return render(request, "user/roster_delete.html", context)

