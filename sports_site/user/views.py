from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import login_required
from django.db import router
from django.forms import formset_factory
from django.shortcuts import render, redirect
from league.models import (Player, PlayerSeason, Roster, SeasonStage, Team,
    TeamSeason)
from .decorators import user_owns_roster
from .forms import ( PlayerCreateForm, PlayerDeleteForm, PlayerSelectForm,
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
            roster_data = form.cleaned_data.get("roster")
            if roster_data:
                season_data = roster.team.season

                roster_copy = roster_data.playerseason_set.all()
                for player in roster_copy:
                    new_playerseason, playerseason_created = PlayerSeason.objects.get_or_create(player=player.player, team=roster, season=season_data)
                    if playerseason_created:
                        new_playerseason.save()
                        messages.success(request, f"{new_playerseason} created and added to {roster}")

            return redirect('roster-view', team_name=team_name, season=season, roster_pk=roster_pk)
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
    """Creates PlayerSeason object based on existing Player"""
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
                data = form.cleaned_data.get('players')
                # Create player season
                if data is not None:
                    playerseason, created = PlayerSeason.objects.get_or_create(
                        player=data,
                        team=roster,
                        season=roster.team.season)
                    playerseason.save()

            return redirect('roster-view',
                            team_name=team_name,
                            season=season,
                            pk=roster_pk)

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
    """Create New Player Object, and Player Season."""
    roster = Roster.objects.get(pk=roster_pk)
    players = roster.playerseason_set.all()
    PlayerFormset = formset_factory(PlayerSelectForm)
    player_formset = PlayerFormset()
    CreatePlayerFormset = formset_factory(PlayerCreateForm,
                                          extra=(21-len(players)) )


    if request.method == 'POST':
        formset = CreatePlayerFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                first = form.cleaned_data.get('first_name')
                last = form.cleaned_data.get('last_name')

                # Create player object
                if first and last:
                    player = Player(first_name=first, last_name=last,
                                    league=roster.team.team.league)
                    player.save()

                # Create player season
                if first and last:
                    playerseason, created = PlayerSeason.objects.get_or_create(
                        player=player,
                        team=roster,
                        season=roster.team.season)
                    playerseason.save()

            return redirect('roster-view',
                            team_name=team_name,
                            season=season,
                            pk=roster_pk)

    else:
        formset = CreatePlayerFormset()

    context = {
        'roster': roster,
        'players': players,
        'formset':formset,
        'player_formset':player_formset
        }
    return render(request, 'user/roster_edit_create.html', context)


@login_required
@user_owns_roster
def roster_edit_remove(request, team_name, season, roster_pk):
    """Creates PlayerSeason object based on existing Player"""
    roster = Roster.objects.get(pk=roster_pk)
    players = roster.playerseason_set.all()


    PlayerFormset = formset_factory(PlayerDeleteForm, extra=len(players))


    if request.method == 'POST':
        formset = PlayerFormset(request.POST,
            form_kwargs={'roster_queryset':players})

        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data.get('players')
                # Delete Player Season
                if data is not None:
                    if type(PlayerSeason()) == type(data):
                        data.delete()

            if 'remove' in request.POST:
                return redirect('roster-view', team_name=team_name,
                                season=season, pk=roster_pk)
            elif 'remove_and_continue' in request.POST:
                return redirect('roster-edit-remove', team_name=team_name,
                                season=season, pk=roster_pk)

    else:
        formset = PlayerFormset(form_kwargs={'roster_queryset':players})

    context = {
        'roster': roster,
        'players': players,
        'formset':formset
        }
    return render(request, 'user/roster_edit_remove.html', context)


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
            season_data = form.cleaned_data.get("seasons")
            roster_data = form.cleaned_data.get("roster")

            if roster_data:
                #If roster_data exists, ie. User wants to copy a previous roster.
                new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(
                    season=season_data, team=user_team)
                new_teamseason.save()
                if teamseason_created:
                    new_roster = Roster.objects.get(team=new_teamseason)

                    roster = roster_data.playerseason_set.all()
                    for player in roster:
                        new_playerseason = PlayerSeason(player=player.player,
                                                        team=new_roster,
                                                        season=season_data)
                        new_playerseason.save()


            else:
                new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(
                    season=season_data, team=user_team)
                new_teamseason.save()


            return redirect("roster-select")

    else:
        form = RosterCreateForm(season_queryset=seasons, roster_queryset=rosters)

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

