from django.shortcuts import render
from .models import Player, PlayerSeason

# Create your views here.
def player_page_view(request, player_pk):
    player = Player.objects.get(pk=player_pk)
    player_seasons = PlayerSeason.objects.all().filter(player=player)
    context = {
        "player": player,
        "player_seasons": player_seasons,
        }
    return render(request, "league/player_page.html", context)