from django.contrib import admin
from django.contrib.auth.models import User
from .models import (PlayerHittingStats, PlayerPitchingStats,
    TeamGameStats, PlayerHittingGameStats, PlayerPitchingGameStats)



from django.db.models import Q
from django import forms

from .vars import SeasonStageYear


"""Game and Game Related objects"""
class PlayerHittingGameStatsInline(admin.TabularInline):
    """Player Hitting stats per game inline."""
    model = PlayerHittingGameStats
    #extra = 1
    verbose_name = "Team Hitting Stats"
    # fields = ('player','at_bats','singles', 'doubles')
    fieldsets = [
        (None, {
            'fields': ('player','at_bats','singles', 'doubles','triples',
                'homeruns','hits' ,'runs', 'runs_batted_in', 'strikeouts', 'walks',
                'hit_by_pitch', 'stolen_bases', 'caught_stealing',
                'sacrifice_flies', 'sacrifice_bunts')
        })
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            pass
        elif db_field.name == "player":
            roster = PlayerSeason.objects.filter(team__team__team__owner=request.user)
            kwargs["queryset"] = roster
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TeamGameStats)
class TeamGameStatsAdmin(admin.ModelAdmin):
    # inlines = [PlayerHittingGameStatsInline, PlayerHittingGameStatsInline2(None)]
    inlines = [PlayerHittingGameStatsInline,]
    list_display = ('game',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Sets it so a teamadmin can only select his only player for stat
        lines"""
        if request.user.is_superuser:
            pass
        elif db_field.name == "season":
            kwargs["queryset"] = SeasonStage.objects.filter(season__year=SeasonStageYear)
        elif db_field.name == "owner":
            kwargs["queryset"] = User.objects.filter(username=request.user)
        elif db_field.name == "team":
            kwargs["queryset"] = TeamSeason.objects.filter(team__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):
            qs = super().get_queryset(request)

            if request.user.is_superuser:
                return qs
            return qs.filter(owner=request.user)



@admin.register(PlayerHittingGameStats)
class PlayerHittingGameStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'team_stats')

@admin.register(PlayerPitchingGameStats)
class PlayerPitchingGameStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'team_stats')


