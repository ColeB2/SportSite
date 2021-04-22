from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RosterForm, PlayerSelectForm, PlayerCreateForm

from django.forms import inlineformset_factory, formset_factory
from league.models import Roster, PlayerSeason, Player

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse



# Create your views here.
@login_required
def roster_select(request):
    roster = Roster.objects.all().filter(team__team__owner=request.user)
    context = {
        'rosters': roster,
        }
    return render(request, "user/roster_select.html", context)


@login_required
def roster_view(request, team, season, pk):
    roster = Roster.objects.get(team__team__name=team, team__season__season__year=season, pk=pk)

    players = roster.playerseason_set.all()
    context = {
        'roster': roster,
        'players': players
        }
    return render(request, 'user/roster_view.html', context)


@login_required
def roster_edit_add(request, team, season, pk):
    """Creates PlayerSeason object based on existing Player"""
    roster = Roster.objects.get(team__team__name=team, team__season__season__year=season, pk=pk)
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

            return redirect('roster-view', team=team, season=season, pk=pk)
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
def roster_edit_create(request, team, season, pk):
    """Create New Player Object, and Player Season."""
    roster = Roster.objects.get(team__team__name=team, team__season__season__year=season, pk=pk)
    players = roster.playerseason_set.all()
    PlayerFormset = formset_factory(PlayerSelectForm)
    player_formset = PlayerFormset()
    CreatePlayerFormset = formset_factory(PlayerCreateForm)


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

            return redirect('roster-view', team=team, season=season, pk=pk)
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
def roster_edit_remove(request, team, season, pk):
    roster = Roster.objects.get(team__team__name=team, team__season__season__year=season, pk=pk)
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

            return redirect('roster-view', team=team, season=season, pk=pk)
        else:
            print('Something went wrong with formset')
    else:
        formset = PlayerFormset(form_kwargs={'exclude_list':exclude_list})

    context = {
        'roster': roster,
        'players': players,
        'formset':formset
        }
    return render(request, 'user/roster_edit_remove.html', context)



class RosterView(UpdateView):
    template_name = 'user/roster1.html'
    model = Roster

    success_url = '/'
    fields = '__all__'

