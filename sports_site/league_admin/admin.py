from django.contrib import admin
from .models import LeagueOptions

# Register your models here.
@admin.register(LeagueOptions)
class LeagueOptionsAdmin(admin.ModelAdmin):
    list_display = ('stat_options',)