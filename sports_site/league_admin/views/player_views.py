from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import router
from django.shortcuts import render, redirect
from ..filters import PlayerFilter
from ..forms import (PlayerCreateForm, EditPlayerForm)
from league.models import (League, Player)
from ..decorators import user_owns_player



@login_required
@permission_required('league.league_admin')
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
@permission_required('league.league_admin')
def league_admin_player_select_view(request):
    league = League.objects.get(admin=request.user)
    players = Player.objects.all().filter(league=league)
    f = PlayerFilter(request.GET, queryset=players)
    players_list = f.qs

    paginator = Paginator(players_list, 25)
    page = request.GET.get('page', 1)

    try:
        all_players = paginator.page(page)
    except PageNotAnInteger:
        all_players = paginator.page(1)
    except EmptyPage:
        all_players = paginator.page(paginator.num_pages)

    context = {
        "filter": f,
        "paginator":paginator,
        "all_players":all_players
        }

    return render(request, "league_admin/player_select.html", context)


@permission_required('league.league_admin')
@user_owns_player
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
        "form":form,
        "player_instance":player_instance
        }
    return render(request, "league_admin/player_edit.html", context)


@permission_required('league.league_admin')
@user_owns_player
def league_admin_player_delete_info_view(request, player_pk):
    player = Player.objects.get(pk=player_pk)

    using = router.db_for_write(player._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([player])

    if request.method == 'POST':
        player.delete()
        messages.success(request, f"{player} and all releated object were deleted")
        return redirect('league-admin-player-select')
    else:
        pass

    context = {
        'player':player,
        'nested_object':nested_object,
    }
    return render(request, "league_admin/player_delete.html", context)