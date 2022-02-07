import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now




class League(models.Model):
    name = models.CharField(max_length=100, null=False, default="League Name Here")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    url = models.SlugField(max_length=25, null=False, default=None, unique=True)


    class Meta:
        permissions = (
            ("league_admin", "Has league admin permissions"),
            )

    def __str__(self):
        return f"{self.name}"


"""Season Related Models"""
class Season(models.Model):
    year = models.CharField(max_length=10, null=False, default=now().year, help_text="Year in YYYY format, ie 2020")
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.year}"


class SeasonStage(models.Model):
    STAGE_PRINT = {"R":"Regular Season","P":"Postseason", "O": "Other"}
    REGULAR = 'R'
    POST = 'P'
    OTHER = 'O'
    SEASON_STAGE = [
        (REGULAR, 'Regular Season'),
        (POST, 'Postseason'),
        (OTHER, 'Other'),
    ]

    stage = models.CharField(choices=SEASON_STAGE, max_length=20, null=True, help_text="The stage the season is in. Each season can contain multiple stages.")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    stage_name = models.CharField(max_length=50, null=True, default=None, blank=True, help_text="Used to denote name of stage. IE, Tournament, Preseason. Recommended when selecting stage as other.")
    featured = models.BooleanField(null=False, default=False, verbose_name="Featured", help_text="Denotes whether the stage should be the main showcase for stats, standings etc.")

    def __str__(self):
        if self.stage_name:
            return f"{self.season} {self.stage_name}"
        else:
            return f"{self.season} {self.STAGE_PRINT[self.stage]}"


    def save(self, *args, **kwargs):
        if self.featured:
            try:
                temp = SeasonStage.objects.get(season__league=self.season.league, featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except SeasonStage.DoesNotExist:
                pass

        super(SeasonStage, self).save(*args, **kwargs)



"""Team Related Models"""
def unique_abbreviation(obj_instance, obj_abbreviation=None, iterations=0):
    """
    A function to calculate a unique abbrev. for instance. Works by checking if
    abbrev is provided, if not, creates one, then checks if it exists.
    If it does, it check next letter in the place string and tries again..
    """
    if obj_abbreviation:
        abbreviation = obj_abbreviation
    else:
        abbreviation = obj_instance.place[0:3].upper()

    obj_class = obj_instance.__class__
    queryset_exists = obj_class.objects.filter(abbreviation=abbreviation).exists()

    if queryset_exists:
        if obj_class.objects.get(abbreviation=abbreviation) == obj_instance:
            return abbreviation
        else:
            if len(obj_instance.place) >= iterations+4:
                new_abbreviation = obj_instance.place[0:2].upper() + obj_instance.place[3+iterations:4+iterations].upper()
                return unique_abbreviation(obj_instance, obj_abbreviation=new_abbreviation, iterations=iterations+1)
            else:
                return None
    return abbreviation


class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    place = models.CharField(max_length=30, null=True, blank=True)
    abbreviation = models.SlugField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f"{self.place} {self.name}"

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.abbreviation = unique_abbreviation(self, self.abbreviation)
        super(Team, self).save(*args, **kwargs)


class TeamSeason(models.Model):
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.team} {self.season}"


    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Roster.objects.get_or_create(team=self)


class Roster(models.Model):
    team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (
            ("user_roster_add", "User can add existing players to rosters"),
            ("user_roster_delete", "User can delete rosters"),
            ("user_roster_remove", "User can remove players from roster"),
            ("user_roster_create", "User can create new rosters"),
            ("user_roster_create_players", "User can create new players to add to roster"),
            )


    def __str__(self):
        return f"{self.team}"

    def save(self, *args, **kwargs):
        self.season = self.team.season
        super().save(*args, **kwargs)


"""Player Related Models"""
class Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=35, null=True, blank=True)
    last_name = models.CharField(max_length=35, null=True, blank=True)

    birthdate = models.DateField(null=True, blank=True, default=None)
    bats = models.CharField(max_length=10, null=True, blank=True, default=None)
    throw = models.CharField(max_length=10, null=True, blank=True, default=None)

    height_feet = models.PositiveIntegerField(null=True, blank=True, default=None)
    height_inches = models.PositiveIntegerField(null=True, blank=True, default=None)
    weight = models.PositiveIntegerField(null=True, blank=True, default=None)



    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class PlayerSeason(models.Model):
    """Player Season model. Holds All the information the player has for any
    given season/season stage. Ie, 2018 season, 2019 playoffs etc."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Roster, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True, blank=True)


    number = models.PositiveIntegerField(null=True, blank=True, default=None)
    position = models.CharField(max_length=35, null=True, blank=True, default=None)


    def __str__(self):
        return f"{self.player} {self.season}"


    def save(self, *args, **kwargs):
        super(PlayerSeason, self).save(*args, **kwargs)


class Game(models.Model):
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    home_team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True, related_name="HomeTeam", verbose_name="Home")
    away_team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True, related_name="AwayTeam", verbose_name="Visitor")
    date = models.DateField()
    start_time = models.TimeField(default=datetime.time(hour=19,minute=00), null=True, blank=True, verbose_name="Time")
    location = models.CharField(max_length=50, null=True, blank=True, help_text="Defaults to home team.")
    stats_entered = models.BooleanField(null=True, default=False, verbose_name="Stats Entered")

    home_stats_entered = models.BooleanField(null=True, default=False, verbose_name="Stats Entered")
    away_stats_entered = models.BooleanField(null=True, default=False, verbose_name="Stats Entered")
    home_score = models.IntegerField(null=True, blank=True, default=0)
    away_score = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.date} - {self.away_team.team.name} @ {self.home_team.team.name}"

    def save(self, *args, **kwargs):
        if self.location == False:
            self.location = f"{self.home_team.team.place}"
        super(Game, self).save(*args, **kwargs)


