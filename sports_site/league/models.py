from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

import datetime

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=100, null=False, default="League Name Here")


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
    STAGE_PRINT = {"R":"Regular Season","P":"Postseason"}
    REGULAR = 'R'
    POST = 'P'
    SEASON_STAGE = [
        (REGULAR, 'Regular Season'),
        (POST, 'Postseason'),
    ]

    stage = models.CharField(choices=SEASON_STAGE, max_length=20, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.season} {self.STAGE_PRINT[self.stage]}"



"""Team Related Models"""
class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    place = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.place} {self.name}"


class TeamSeason(models.Model):
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.team} {self.season}"


    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Roster.objects.create(team=self)


class Roster(models.Model):
    team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.team}"

    def save(self, *args, **kwargs):
        self.season = self.team.season
        super().save(*args, **kwargs)


"""Player Related Models"""
class Player(models.Model):
    first_name = models.CharField(max_length=35, null=True, blank=True)
    last_name = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class PlayerSeason(models.Model):
    """Player Season model. Holds All the information the player has for any
    given season/season stage. Ie, 2018 season, 2019 playoffs etc."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Roster, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(SeasonStage, on_delete=models.CASCADE, null=True, blank=True)

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
    location = models.CharField(max_length=20, null=True, blank=True, help_text="Defaults to home team.")
    stats_entered = models.BooleanField(null=True, default=False, verbose_name="Stats Entered")
    final_score = models.CharField(max_length=20, null=True, blank=True, default='---')

    def __str__(self):
        return f"{self.date} - {self.away_team.team.name} @ {self.home_team.team.name}"

    def save(self, *args, **kwargs):
        self.location = f"{self.home_team.team.place}"
        super(Game, self).save(*args, **kwargs)