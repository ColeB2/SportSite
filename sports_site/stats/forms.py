from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Row, Column)
from django import forms
from django.forms.models import inlineformset_factory
from .models import (PlayerHittingGameStats, PlayerPitchingGameStats,
    TeamGameLineScore, TeamGameStats)
from league.models import PlayerSeason


class PlayerStatsCreateForm(forms.Form):
    """Creates all player stats objects to be edited later"""
    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('team_game_stats')
        super(PlayerStatsCreateForm, self).__init__(*args, **kwargs)
        self.player_queryset = PlayerSeason.objects.all().filter(team__team=self._team_season)

        self.fields["player"] = forms.ModelChoiceField(
            queryset=self.player_queryset,
            label=False,
            required=False,
            )

        self.fields["pitched"] = forms.BooleanField(
            required=False,
            )

        #crispy layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("player", css_class="form-group col-md-5"),
                Column("pitched", css_class="form-group col-md-4"),
                css_class="form-row"
                ),
            )
        self.helper.form_tag = False



    def process(self):
        _player = self.cleaned_data.get("player")
        hitting_stats, hit_created, pitching_stats, pitch_created, pitched =(
            _player, False, _player, False, None)
        if _player:
            hitting_stats, hit_created = PlayerHittingGameStats.objects.get_or_create(
                team_stats=self._team_game_stats,
                season=self._team_season.season,
                player=_player)
            hitting_stats.save()
            if self.cleaned_data.get("pitched") == True:
                pitching_stats, pitch_created = PlayerPitchingGameStats.objects.get_or_create(
                    team_stats=self._team_game_stats,
                    season=self._team_season.season,
                    player=_player)

                pitched=True

                pitching_stats.save()

        return (hitting_stats, hit_created, pitching_stats, pitch_created, pitched)


class LinescoreEditForm(forms.ModelForm):
    class Meta:
        model = TeamGameLineScore
        exclude = ["game",]

    def process(self):
        linescore_save = self.save()
        linescore_save.save()
        return linescore_save


class PHGSFHelper(FormHelper):
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
    class Meta:
        model = PlayerHittingGameStats
        exclude = ['team_stats', 'season', 'average','on_base_percentage',
            'slugging_percentage', 'on_base_plus_slugging', 'hits',
        ]

    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('game_stats')
        super(PlayerHittingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(team__team=self._team_season)
        self.fields['player'].label = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
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
        self.helper.form_tag = False


    def process(self):
        player_stats = self.save()
        player_stats.save()
        return player_stats


class PPGSFHelper(FormHelper):
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
                Column("save"),
                Column("save_op"),
                Column("innings_pitched"),
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
    class Meta:
        model = PlayerPitchingGameStats
        exclude = ['team_stats', 'season', 'average','game', 'whip', 'era',
        ]

    def __init__(self, *args, **kwargs):
        self._team_season = kwargs.pop('team_season')
        self._team_game_stats = kwargs.pop('game_stats')
        super(PlayerPitchingGameStatsForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = PlayerSeason.objects.all().filter(team__team=self._team_season)
        self.fields['player'].label = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
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
                Column("save"),
                Column("save_op"),
                Column("innings_pitched"),
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
        self.helper.form_tag = False


    def process(self):
        player_stats = self.save()
        player_stats.save()
        return player_stats

HittingGameStatsFormset = inlineformset_factory(TeamGameStats,
    PlayerHittingGameStats, form=PlayerHittingGameStatsForm, extra=0)

PitchingGameStatsFormset = inlineformset_factory(TeamGameStats,
    PlayerPitchingGameStats, form=PlayerPitchingGameStatsForm, extra=0)




