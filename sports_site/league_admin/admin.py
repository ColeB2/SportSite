from django.contrib import admin
from .models import LeagueHittingOptions

# Register your models here.
@admin.register(LeagueHittingOptions)
class LeagueHittingOptionsAdmin(admin.ModelAdmin):
    list_display = ('stat_options',)