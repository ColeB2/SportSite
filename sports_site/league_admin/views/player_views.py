from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import formset_factory
from ..filters import PlayerFilter
from ..forms import (PlayerCreateForm, EditPlayerForm)
from league.models import (League, Player)



@login_required
def league_admin_player_create_view(request):
    league = League.objects.get(admin=request.user)

    if request.method == 'POST':
        form = PlayerCreateForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            new_player = Player(league=league, first_name=first_name, last_name=last_name)
            new_player.save()
            messages.success(request, f"{new_player} created.")




        return redirect('league-admin-dashboard')
    else:
        form = PlayerCreateForm()

    context = {
        "form": form,
    }
    return render(request, "league_admin/player_create.html", context)

@login_required
def league_admin_player_select_view(request):
    league = League.objects.get(admin=request.user)
    players = Player.objects.all().filter(league=league)
    f = PlayerFilter(request.GET, queryset=players)

    context = {
        "filter": f
        }

    return render(request, "league_admin/player_select.html", context)



def league_admin_player_edit_view(request, player_pk):
    player_instance = Player.objects.get(pk=player_pk)

    if request.method == "POST":
        form = EditPlayerForm(data=request.POST, instance=player_instance)
        if form.is_valid():
            player = form.save(commit=False)
            player.save()

        return redirect('league-admin-player-select')
    else:
        form = EditPlayerForm(instance=player_instance)

    context = {
        "form":form
        }
    return render(request, "league_admin/player_edit.html", context)