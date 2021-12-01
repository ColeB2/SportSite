from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.forms.models import inlineformset_factory
from league.models import PlayerSeason
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameLineScore, TeamGameStats)



class PlayerStatsCreateForm(forms.Form):
    """
    Creates all player stats objects to be edited later

    Used: views/tgs_hitting_views.py
       team_game_stats_create_view()
    """
    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('team_game_stats')
        super(PlayerStatsCreateForm, self).__init__(*args, **kwargs)
        self.player_queryset = PlayerSeason.objects.all().filter(
            team__team=self._team_season)

        self.fields["player"] = forms.ModelChoiceField(
            queryset=self.player_queryset,
            label=False,
            required=False,
            )


        #crispy layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-5"),
                css_class="form-row"
                ),
            )
        self.helper.form_tag = False



    def process(self):
        _player = self.cleaned_data.get("player")
        if _player:
            hitting_stats, created = PlayerHittingGameStats.objects.get_or_create(
                team_stats=self._team_game_stats,
                season=self._team_season.season,
                player=_player)
            hitting_stats.save()
        else:
            return None, None
        return hitting_stats, created



class PlayerPitchingStatsCreateForm(forms.Form):
    """
    Creates all player pitching stats objects to be edited later

    Used: tgs_pitching_views.py
        team_game_pitching_stats_create_view()
    """
    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('team_game_stats')
        super(PlayerPitchingStatsCreateForm, self).__init__(*args, **kwargs)
        self.player_queryset = PlayerSeason.objects.all().filter(
            team__team=self._team_season)

        self.fields["player"] = forms.ModelChoiceField(
            queryset=self.player_queryset,
            label=False,
            required=False,
            )


        #crispy layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-5"),
                css_class="form-row"
                ),
            )
        self.helper.form_tag = False



    def process(self):
        _player = self.cleaned_data.get("player")
        if _player:
            pitching_stats, created = PlayerPitchingGameStats.objects.get_or_create(
                team_stats=self._team_game_stats,
                season=self._team_season.season,
                player=_player)
            pitching_stats.save()
        else:
            return None, None
        return pitching_stats, created


class LinescoreEditForm(forms.ModelForm):
    """
    Used: views/tg_linescore_views.py
        team_game_linescore_edit_view()
    """
    class Meta:
        model = TeamGameLineScore
        exclude = ["game",]

    def process(self):
        linescore_save = self.save()
        linescore_save.save()
        return linescore_save


class PHGSFHelper(FormHelper):
    """
    Helper form used in HittingGameStatsFormset
    Used: tgs_hitting_views.py
        team_game_stats_edit_view()
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-6"),
                css_class="form-row"
                ),
            Row(
                Column("plate_appearances"),
                Column("at_bats"),
                Column("singles"),
                Column("doubles"),
                Column("triples"),
                Column("homeruns"),
                Column("strikeouts"),
                Column("walks"),
                Column("hit_by_pitch"),
                css_class="form-row"),
            Row(
                Column("runs_batted_in"),
                Column("runs"),
                Column("stolen_bases"),
                Column("caught_stealing"),
                Column("sacrifice_flies"),
                Column("sacrifice_bunts"),
                Column("reached_on_error"),
                Column("fielders_choice"),
                css_class="form-row"),
            )

class PlayerHittingGameStatsForm(forms.ModelForm):
    """
    Used to edit player hitting game stats.
    Used in inline form factory below.
    """
    class Meta:
        model = PlayerHittingGameStats
        exclude = ['team_stats', 'season', 'average','on_base_percentage',
            'slugging_percentage', 'on_base_plus_slugging', 'hits',
        ]

    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('game_stats')
        super(PlayerHittingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(
            team__team=self._team_season)
        self.fields['player'].label = False


    def process(self):
        player_stats = self.save()
        player_stats.save()
        return player_stats


class PPGSFHelper(FormHelper):
    """
    Helper form used in to help PitchingGameStatsFormset

    Used: tgs_pitching_views.py
        team_game_pitching_stats_edit_view()

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-6"),
                css_class="form-row"
                ),
            Row(
                Column("win"),
                Column("loss"),
                Column("game_started"),
                Column("complete_game"),
                Column("shutout"),
                Column("save_converted"),
                Column("save_op"),
                Column("innings_pitched"),
                Column("outs"),
                css_class="form-row"),
            Row(
                Column("hits_allowed"),
                Column("runs_allowed"),
                Column("earned_runs"),
                Column("homeruns_allowed"),
                Column("hit_batters"),
                Column("walks_allowed"),
                Column("strikeouts"),
                css_class="form-row"),
            )


class PlayerPitchingGameStatsForm(forms.ModelForm):
    """
    Used to edit player pitching game stats.
    Used in the inline form below.
    """
    outs = forms.IntegerField(label="Outs",
        help_text="Extra outs gotten after the full inning ie. 6 2/3 -- 2 outs",
        max_value=2, min_value=0, required=False)
    class Meta:
        model = PlayerPitchingGameStats
        exclude = ['team_stats', 'season', 'average','game', 'whip', 'era',
        ]

    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('game_stats')
        super(PlayerPitchingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(
            team__team=self._team_season)
        self.fields['player'].label = False


    def process(self):
        outs = self.cleaned_data["outs"]
        if outs == None:
            outs = 0
        innings_pitched = self.cleaned_data["innings_pitched"]
        player_stats = self.save()
        player_stats._innings = innings_pitched + round((outs/3),2)
        player_stats.save()
        return player_stats

HittingGameStatsFormset = inlineformset_factory(TeamGameStats,
    PlayerHittingGameStats, form=PlayerHittingGameStatsForm, extra=0)

PitchingGameStatsFormset = inlineformset_factory(TeamGameStats,
    PlayerPitchingGameStats, form=PlayerPitchingGameStatsForm, extra=0)




