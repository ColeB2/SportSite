from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import router
from django.shortcuts import render, redirect
from ..decorators import user_owns_game
from ..forms import LinescoreEditForm
from ..models import TeamGameLineScore, TeamGameStats



@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_create_view(request, game_pk, team_season_pk,
                                    team_game_stats_pk):
    """View which creates a linescore model and if one doesn't exist and
    immediately redirects to  team game stats info view"""

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)

    linescore, created = TeamGameLineScore.objects.get_or_create(game=game_stats)
    if created:
        linescore.save()
        messages.success(request, f"{linescore} created.")
    else:
        messages.info(request, f"{linescore} already exists.")

    return redirect("stats-team-game-stats", game_pk, team_season_pk)


@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_edit_view(request, game_pk, team_season_pk,
                                  team_game_stats_pk, linescore_pk):

    game_stats = TeamGameStats.objects.get(pk=team_game_stats_pk)

    try:
        linescore = TeamGameLineScore.objects.get(game=game_stats,
                                                  game__team=team_season_pk)
    except ObjectDoesNotExist:
        linescore = None

    if request.method == "POST":
        form = LinescoreEditForm(data=request.POST,
                                 files=request.FILES,
                                 instance=linescore)
        if form.is_valid:
            linescore_save = form.process()
            messages.success(request, f"{linescore_save} saved.")
        return redirect("stats-team-game-stats", game_pk, team_season_pk)
    else:
        form = LinescoreEditForm(instance=linescore)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "game_stats":game_stats,
        "linescore": linescore,
        "form":form,
        }
    return render(request, "stats/game_linescore_create.html", context)


@permission_required('league.league_admin')
@user_owns_game
def team_game_linescore_delete_info_view(request, game_pk, team_season_pk,
                                         team_game_stats_pk, linescore_pk):
    linescore = TeamGameLineScore.objects.get(pk=linescore_pk)


    using = router.db_for_write(linescore._meta.model)
    nested_object = NestedObjects(using)
    nested_object.collect([linescore])

    if request.method == 'POST':
        linescore.delete()
        messages.success(request,
            f"{linescore} and all releated object were deleted")

        return redirect('stats-team-game-stats', game_pk, team_season_pk)

    context = {
        "game_pk": game_pk,
        "team_season_pk": team_season_pk,
        "linescore": linescore,
        "nested_object": nested_object,
        }
    return render(request, "stats/game_linescore_delete.html", context)