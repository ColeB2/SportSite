from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Row, Column, MultiWidgetField, HTML)
from django import forms
from django.contrib.auth.models import Permission
from datetime import datetime
from league.models import Game, Player, Season, SeasonStage, Team, TeamSeason
from stats.models import TeamGameStats



class SeasonSelectForm(forms.ModelForm):
    class Meta:
        model = SeasonStage
        fields = ['season', 'stage',]

    def __init__(self, *args, **kwargs):
        super(SeasonSelectForm, self).__init__(*args, **kwargs)
        self.fields['season'].required = False
        self.fields['stage'].required = False


class SeasonForm(forms.ModelForm):
    """
    Form that creates a Season model object, takes a year input and
    automatically inputs the league value depending on user.

    Used: league_admin/views/season/views.py
        league_admin_create_season_view()
        SeasonEditView()
    """
    class Meta:
        model = Season
        fields = ['year',]

    def process(self, league):
        year_data = self.cleaned_data.get('year')

        new_season, created = Season.objects.get_or_create(year=year_data,
                                                           league=league)

        if created:
            new_season.save()

        return new_season, created



class SeasonStageCreateForm(forms.ModelForm):
    """
    Used to create a SeasonStage model object.

    Used: league_admin/views/season_stage_views.py
        league_admin_create_season_stage_view()
    """
    class Meta:
        model = SeasonStage
        fields = ['stage', 'stage_name', 'featured']


    def process(self, season):
        stage_data = self.cleaned_data.get('stage')
        featured_data = self.cleaned_data.get('featured')
        stage_name_data = self.cleaned_data.get('stage_name')

        new_stage, created = SeasonStage.objects.get_or_create(
            stage=stage_data,
            season=season,
            featured=featured_data,
            stage_name=stage_name_data)

        if created:
            new_stage.save()

        return new_stage, created


class TeamSelectForm(forms.Form):
    """
    Used as a select form for select teams that will participate in a
    new season stage.

    Used: league_admin/views/season_stage_views.py
        league_admin_create_season_stage_view()
        league_admin_season_stage_add_teams_view()
    """
    def __init__(self, team_queryset, *args, **kwargs):
        super(TeamSelectForm,self).__init__(*args, **kwargs)
        self.fields['teams'] = forms.ModelChoiceField(
            queryset=team_queryset,
            label=False,
            required=False,
            )

        self.fields['teams'].widget.attrs.update(style='max-width: 24em')


    def process(self, season):
        team_data = self.cleaned_data.get('teams')

        if team_data:
            new_teamseason, created = TeamSeason.objects.get_or_create(
                season=season,
                team=team_data)

            if created:
                new_teamseason.save()

            return new_teamseason, created

        else:
            return None, None


class PlayerCreateForm(forms.ModelForm):
    """
    Used to created a Player model object.

    Used: league_admin/views/player_views.py
        league_admin_player_create_view()
        league_admin_player_edit_view()
    """
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', "birthdate", "bats", "throw",
            "height_feet", "height_inches", "weight"]


    def __init__(self, *args, **kwargs):
        super(PlayerCreateForm, self).__init__(*args, **kwargs)
        self.fields["birthdate"].label = "Birthdate - YYYY-MM-DD format"
        self.fields["height_feet"].label = "Height, feet, ie 5,6, etc."
        self.fields["height_inches"].label = "Height, inches, ie 1,2,3... etc."
        self.fields["weight"].label = "Weight, lbs"


    def process(self, league):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        new_player = Player(league=league, first_name=first_name,
                            last_name=last_name)
        new_player.save()

        return new_player


    def process_edit(self):
        player = self.save(commit=True)

        return player


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['owner', 'name', 'place', 'abbreviation']

    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['owner'].label = "Owner/Team Admin Account"
        self.fields['place'].required = False

    def process(self, league):
        owner = self.cleaned_data.get('owner')
        name = self.cleaned_data.get('name')
        place = self.cleaned_data.get('place')
        abbreviation = self.cleaned_data.get('abbreviation')

        new_team = Team(owner=owner, name=name, place=place, league=league,
            abbreviation=abbreviation)
        new_team.save()

        return new_team

    def process_edit(self):
        team = self.save(commit=True)

        return team


class EditGameForm(forms.ModelForm):
    """
    Used to edit the Game model.

    Used: league_admin/views/games_views.py
        league_admin_edit_game_view()

    """
    class Meta:
        model = Game
        fields = ['home_team', 'away_team','location', 'date' , 'start_time',
            'stats_entered', 'home_score', 'away_score',]
        cur_date = datetime.today()
        year_range = tuple(
            [i for i in range(cur_date.year - 5, cur_date.year + 5) ] )
        widgets = {
            'date': forms.SelectDateWidget(
                empty_label=('Year', 'Month', 'Day'), years=(year_range) )
            }

    def __init__(self, *args, **kwargs):
        super(EditGameForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("home_team", css_class="form-group col-md-4"),
                Column("away_team", css_class="form-group col-md-4"),
                Column("location", css_class="form-group col-md-4"),
                css_class='form-row'
                ),
            Row(
                Column(
                    MultiWidgetField('date', attrs=(
                        {'style': 'width: 33%; display: inline-block; '})),
                    css_class='form-group col-md-8'
                    ),
                Column('start_time', css_class='form-group col-md-4'),
                css_class='form-row'
                ),
            Row(
                Column("home_score", css_class="form-group col-md-4"),
                Column("away_score", css_class="form-group col-md-4"),
                Column("stats_enetered", css_class="form-group col-md-4"),
                css_class='form-row'
                ),
            )

        self.helper.form_method = 'post'
        self.helper.layout.append(HTML("""
            <input type="submit" value="Save" class="btn btn-primary">

            <a class="btn btn-danger"
                href="{% url 'league-admin-game-delete' season_year season_stage_pk game_instance.pk  %}">
                Delete {{game_instance}}
            </a>"""))


    def process(self):
        game = self.save(commit=True)

        return game


class CreateGameForm(forms.Form):
    """
    Used to create a Game model object via a formset factory to create
    multiple game objects at the same time.

    Used: league_admin/views/schedule_views.py
        league_admin_schedule_create_view()
    """
    def __init__(self, team_queryset=None, *args, **kwargs):
        super(CreateGameForm, self).__init__(*args, **kwargs)

        self.fields['home_team'] = forms.ModelChoiceField(
            queryset=team_queryset,
            required = False)

        self.fields['away_team'] = forms.ModelChoiceField(
            queryset=team_queryset,
            required = False)

        cur_date = datetime.today()
        year_range = tuple(
            [i for i in range(cur_date.year - 5, cur_date.year + 5)])
        self.fields['date'] = forms.DateField(initial=cur_date,
            widget=forms.SelectDateWidget(
                empty_label=("Year", "Month", "Day"), years=(year_range) ) )
        self.fields['date'].required = False

        self.fields['start_time'] = forms.TimeField(
            label='Start Time (24:00 clock)', required=False)
        self.fields['location'] = forms.CharField(max_length=20, required=False,
            label='Location (default: Home)')

        #crispylayout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('home_team', css_class="form-group col-md-4"),
                Column('away_team', css_class="form-group col-md-4"),
                Column('location', css_class="form-group col-md-4"),
                css_class='form-row'
                ),
            Row(
                Column(
                    MultiWidgetField('date', attrs=(
                        {'style': 'width: 33%; display: inline-block; '})),
                    css_class='form-group col-md-8'
                    ),
                Column('start_time', css_class='form-group col-md-4'),
                css_class='form-row'
                )
            )

    def process(self, current_stage=None):
        """To be called only after form.is_valid() method has been called"""
        home_data = self.cleaned_data.get('home_team')
        away_data = self.cleaned_data.get('away_team')
        date_data = self.cleaned_data.get('date')
        time_data = self.cleaned_data.get('start_time')
        location_data = self.cleaned_data.get('location')
        new_game = None

        if home_data is not None and away_data is not None:

            new_game = Game(season=current_stage, home_team=home_data,
                away_team=away_data, date=date_data)

            if time_data:
                new_game.start_time = time_data
            if location_data:
                new_game.location = location_data

            new_game.save()

            home_game_stats = TeamGameStats(season=current_stage,
                team=home_data, game=new_game)
            away_game_stats = TeamGameStats(season=current_stage,
                team=away_data, game=new_game)

            home_game_stats.save()
            away_game_stats.save()

        return new_game


class EditUserRosterPermissionsForm(forms.Form):
    def __init__(self, selected_user, *args, **kwargs):
        self.selected_user = selected_user
        super(EditUserRosterPermissionsForm, self).__init__(*args, **kwargs)

        self.fields['roster_add'] = forms.BooleanField(
            label="Add existing players to team roster",
            required=False,
            initial=selected_user.has_perm('league.user_roster_add'))

        self.fields['roster_create_players'] = forms.BooleanField(
            label="Create new players to add to team roster",
            required=False,
            initial=selected_user.has_perm('league.user_roster_create_players'))

        self.fields['roster_remove'] = forms.BooleanField(
            label="Remove players from team roster",
            required=False,
            initial=selected_user.has_perm('league.user_roster_remove'))

        self.fields['roster_create'] = forms.BooleanField(
            label="Create new roster for own team",
            required=False,
            initial=selected_user.has_perm('league.user_roster_create'))

        self.fields['roster_delete'] = forms.BooleanField(
            label="Delete own team's existing rosters",
            required=False,
            initial=selected_user.has_perm('league.user_roster_delete'))

    def process(self):
        for field in self.changed_data:

            updated_perm_name = f"user_{field}"
            updated_perm = Permission.objects.get(codename=updated_perm_name)


            if self.cleaned_data.get(field) == True:
                self.selected_user.user_permissions.add(updated_perm)
            else:
                self.selected_user.user_permissions.remove(updated_perm)

        self.selected_user.save()






