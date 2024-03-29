from django import forms
from league.models import Roster, TeamSeason, PlayerSeason, Player



class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['team',]

    def __init__(self, user, *args, **kwargs):
        super(RosterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['team'].queryset = TeamSeason.objects.filter(team__owner=user)


class PlayerSelectForm(forms.Form):
    """
    Form used in the roster_edit_add view in users/views.py.
    Displays a list of all players apart of the league with
    exceptions for players that are currently on the viewed roster.

    form_kwarg={
        'player_qs': qs of all players in the league
        'exclude_list': list of all players currently on the roster,
            so as to exclude them from the seletion list.

    """
    def __init__(self, player_qs, exclude_list=[], *args, **kwargs):
        super(PlayerSelectForm,self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelChoiceField(
            queryset=player_qs.exclude(id__in=[o.id for o in exclude_list]),
            label=False,
            required=False,
            )

        self.fields['players'].widget.attrs.update(style='max-width: 24em')


    def process(self, roster):
        player_data = self.cleaned_data.get("players")

        if player_data:
            playerseason, created = PlayerSeason.objects.get_or_create(
                player=player_data,
                team = roster,
                season = roster.team.season)
            playerseason.save()

            return playerseason


class PlayerCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlayerCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=35)
        self.fields['last_name'] = forms.CharField(max_length=35)


    def process(self, league, roster):
        _first = self.cleaned_data.get('first_name')
        _last = self.cleaned_data.get('last_name')

        if _first and _last:
            player = Player(first_name=_first, last_name=_last, league=league)
            player.save()

            playerseason, created = PlayerSeason.objects.get_or_create(
                player=player,
                team=roster,
                season=roster.team.season)
            playerseason.save()


class PlayerRemoveForm(forms.Form):
    def __init__(self, roster_queryset, *args, **kwargs):
        super(PlayerRemoveForm,self).__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelChoiceField(
            # queryset=Player.objects.all(),
            queryset=roster_queryset,
            label=False,
            required=False,
            )

        self.fields['players'].widget.attrs.update(style='max-width: 24em')

    def process(self):
        _player = self.cleaned_data.get('players')

        if _player:
            if type(PlayerSeason()) == type(_player):
                _player.delete()



class PlayerSeasonForm(forms.ModelForm):

    class Meta:
        model = PlayerSeason
        fields = ['player', 'team']


class RosterSelectForm(forms.Form):
    """
    Used: roster_edit_copy --> users/views.py view.
    """
    def __init__(self,roster_queryset, *args, **kwargs):
        super(RosterSelectForm, self).__init__(*args, **kwargs)
        self.fields['roster'] = forms.ModelChoiceField(
            queryset=roster_queryset,
            label="Select Roster:",
            required=False,
            )

    def process(self, current_roster):
        _roster_data = self.cleaned_data.get("roster")
        return_data = []

        if _roster_data:
            season_data = current_roster.team.season
            _roster_copy = _roster_data.playerseason_set.all()
            for player in _roster_copy:
                playerseason, created = PlayerSeason.objects.get_or_create(
                    player=player.player,
                    team=current_roster,
                    season=season_data)
                if created:
                    playerseason.save()
                    return_data.append(playerseason)
        return return_data



class RosterCreateForm(forms.Form):
    def __init__(self, season_queryset, roster_queryset, *args, **kwargs):
        super(RosterCreateForm, self).__init__(*args, **kwargs)
        self.fields['seasons'] = forms.ModelChoiceField(
            queryset=season_queryset,
            label="Select a season to create your roster for:",
            required=True,
            )
        self.fields['roster'] = forms.ModelChoiceField(
            queryset=roster_queryset,
            label="Select a roster you want to copy over(optional):",
            required=False,
            )


    def process(self, user_team):
        _season_data = self.cleaned_data.get("seasons")
        _roster_data = self.cleaned_data.get("roster")

        if _roster_data:
            new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(
                season=_season_data, team=user_team)
            new_teamseason.save()
            if teamseason_created:
                new_roster = Roster.objects.get(team=new_teamseason)

                _roster = _roster_data.playerseason_set.all()
                for player in _roster:
                    new_playerseason = PlayerSeason(player=player.player,
                                                    team=new_roster,
                                                    season=_season_data)
                    new_playerseason.save()
        else:
            new_teamseason, teamseason_created = TeamSeason.objects.get_or_create(
                season=_season_data, team=user_team)
            new_teamseason.save()













