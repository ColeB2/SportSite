from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RosterForm, PlayerSelectForm

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


# @login_required
# def roster_edit_view(request):
#     context = {}

#     form = RosterForm(request.user, request.POST or None, request.FILES or None, )

#     player_formset = inlineformset_factory(Roster, PlayerSeason, fields=('player', 'season'))
#     roster = Roster.objects.get(team__team__owner=request.user)

#     formset = player_formset(instance=roster)

#     # if form.is_valid():
#         # form.save()

#     context['form'] = form
#     context['formset'] = formset
#     return render(request, "user/roster_edit.html", context)

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
def roster_edit(request, team, season, pk):
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
    return render(request, 'user/roster_edit.html', context)



class RosterView(UpdateView):
    template_name = 'user/roster1.html'
    model = Roster

    success_url = '/'
    fields = '__all__'

