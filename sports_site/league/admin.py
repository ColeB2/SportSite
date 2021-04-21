from django.contrib import admin
from .models import (League, Season, SeasonStage, Team, TeamSeason, Roster, Player, PlayerSeason, Game)

# Register your models here.

"""Admin Models"""
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name",)


"""Season Admin Models"""
class SeasonStageInline(admin.TabularInline):
    model = SeasonStage
    extra = 1

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("year",)
    inlines = [SeasonStageInline,]

@admin.register(SeasonStage)
class SeasonStageAdmin(admin.ModelAdmin):
    list_display = ('season', 'stage',)


    # list_filter = ('season')

"""Player Admin Models"""
class PlayerSeasonInline(admin.TabularInline):
    model = PlayerSeason
    fields = ['player', 'season', 'team']
    extra = 1

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerSeasonInline,]
    list_display = ('last_name','first_name',)
    search_fields = ('first_name', 'last_name')

@admin.register(PlayerSeason)
class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'season')
    list_filter = ('team', 'season')
    search_fields = ['player__first_name', 'player__last_name']

"""Team Admin Models"""
class TeamSeasonInline(admin.TabularInline):
    model = TeamSeason
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('place','name',)
    inlines = [TeamSeasonInline,]


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ('team',)
    inlines = [PlayerSeasonInline,]

@admin.register(TeamSeason)
class TeamSeasonAdmin(admin.ModelAdmin):
    list_display = ('team', 'season',)
    list_filter = ('season','team')

    #TEST
    ordering = ['season']
    search_fields = ['season']

    def get_queryset(self, request):
            qs = super().get_queryset(request)

            if request.user.is_superuser:
                return qs
            return qs.filter(team__owner=request.user)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('date','away_team','home_team','stats_entered')