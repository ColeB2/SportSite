from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import (PlayerSelectForm, PlayerCreateForm, PlayerSeasonForm, PlayerDeleteForm,
    RosterCreateForm)

from django.forms import formset_factory, modelformset_factory
from league.models import Roster, PlayerSeason, Player, Team, TeamSeason, SeasonStage



# Create your views here.
@login_required
def roster_select(request):
    roster = Roster.objects.all().filter(team__team__owner=request.user)
    context = {
        'rosters': roster,
        }
    return render(request, "user/roster_select.html", context)


@login_required
def roster_view(request, team_name, season, pk):
    roster = Roster.objects.get(team__team__name=team_name, team__season__season__year=season, pk=pk)

    players = roster.playerseason_set.all()
    context = {
        'roster': roster,
        'players': players
        }
    return render(request, 'user/roster_view.html', context)


@login_required
def roster_edit_add(request, team_name, season, pk):
    """Creates PlayerSeason object based on existing Player"""
    roster = Roster.objects.get(team__team__name=team_name, team__season__season__year=season, pk=pk)
    players = roster.playerseason_set.all()

    exclude_list = []
    for player in players:
        exclude_list.append(player.player)

    PlayerFormset = formset_factory(PlayerSelectForm, extra=(21-len(exclude_list)) )


    if request.method == 'POST':
        formset = PlayerFormset(request.POST, form_kwargs={'exclude_list':exclude_list})
        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data.get('players')
                # Create player season
                if data is not None:
                    playerseason, created = PlayerSeason.objects.get_or_create(player=data, team=roster, season=roster.team.season)
                    playerseason.save()

            return redirect('roster-view', team_name=team_name, season=season, pk=pk)
        else:
            print('Something went wrong with formset')
    else:
        formset = PlayerFormset(form_kwargs={'exclude_list':exclude_list})

    context = {
        'roster': roster,
        'players': players,
        'formset':formset
        }
    return render(request, 'user/roster_edit_add.html', context)


@login_required
def roster_edit_create(request, team_name, season, pk):
    """Create New Player Object, and Player Season."""
    roster = Roster.objects.get(team__team__name=team_name, team__season__season__year=season, pk=pk)
    players = roster.playerseason_set.all()
    PlayerFormset = formset_factory(PlayerSelectForm)
    player_formset = PlayerFormset()
    CreatePlayerFormset = formset_factory(PlayerCreateForm, extra=(21-len(players)) )


    if request.method == 'POST':
        formset = CreatePlayerFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                first = form.cleaned_data.get('first_name')
                last = form.cleaned_data.get('last_name')

                # Create player object
                if first is not None and last is not None:
                    player = Player(first_name=first, last_name=last)
                    player.save()

                # Create player season
                if first is not None and last is not None:
                    playerseason, created = PlayerSeason.objects.get_or_create(player=player, team=roster, season=roster.team.season)
                    playerseason.save()

            return redirect('roster-view', team_name=team_name, season=season, pk=pk)
        else:
            print('Something went wrong with formset')
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
def roster_edit_remove(request, team_name, season, pk):
    """Creates PlayerSeason object based on existing Player"""
    roster = Roster.objects.get(team__team__name=team_name, team__season__season__year=season, pk=pk)
    players = roster.playerseason_set.all()


    PlayerFormset = formset_factory(PlayerDeleteForm, extra=21)


    if request.method == 'POST':
        formset = PlayerFormset(request.POST, form_kwargs={'roster_queryset':players})
        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data.get('players')
                # Delete Player Season
                if data is not None:
                    if type(PlayerSeason()) == type(data):
                        data.delete()

            if 'remove' in request.POST:
                return redirect('roster-view', team_name=team_name, season=season, pk=pk)
            elif 'remove_and_continue' in request.POST:
                return redirect('roster-edit-remove', team_name=team_name, season=season, pk=pk)
        else:
            print('Something went wrong with formset')
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
    rosters = Roster.objects.all().filter(team__team__owner=request.user)
    seasons = SeasonStage.objects.all()


    if request.method == 'POST':
        form = RosterCreateForm(season_queryset=seasons, roster_queryset=rosters, data=request.POST)
        if form.is_valid():
            season_data = form.cleaned_data.get("seasons")
            roster_data = form.cleaned_data.get("roster")

            if roster_data:
                #If roster_data exists, ie. User wants to copy a previous roster.
                new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(season=season_data, team=user_team)
                new_teamseason.save()
                if teamseason_created:
                    new_roster = Roster.objects.get(team=new_teamseason)

                    roster = roster_data.playerseason_set.all()
                    for player in roster:
                        new_playerseason = PlayerSeason(player=player.player, team=new_roster, season=season_data)
                        new_playerseason.save()


            else:
                print('not postseason R')
                new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(season=season_data, team=user_team)
                new_teamseason.save()


            return redirect("roster-select")

        else:
            print(f"Form not valid, roster_create {form}")
    else:
        form = RosterCreateForm(season_queryset=seasons, roster_queryset=rosters)

    context = {
        "rosters":rosters,
        "form": form,
        }
    return render(request, 'user/roster_new.html', context)

