from league.models import League, Game, TeamSeason, SeasonStage
from stats.models import TeamGameLineScore, TeamGameStats
from random import randint
'''
dates = [datetime.date(2021,5,14), datetime.date(2021,5,16),datetime.date(2021,5,21),datetime.date(2021,5,23),datetime.date(2021,5,28),datetime.date(2021,5,30),datetime.date(2021,6,4),datetime.date(2021,6,6),datetime.date(2021,6,11),datetime.date(2021,6,13),datetime.date(2021,6,18),datetime.date(2021,6,20),datetime.date(2021,6,25),datetime.date(2021,6,27),datetime.date(2021,7,2),datetime.date(2021,7,4)]
g = [[41,52,36], [21,43,65],[13,62,54],[16,35,24],[15,64,32],[41,25,63],[12,34,56],[31,26,45],[61,53,42],[51,46,23],[14,52,36],[21,43,65],[13,62,54],[16,35,24],[15,64,32],[41,25,63]]
td = {'2':teams[0], '1':teams[1], '3':teams[2], '4':teams[3], '5':teams[4], '6':teams[5]}
'''

def get_league(url="SBBL"):
    league = League.objects.get(url=url)
    return league

def get_featured_season_stage(league=None):
    season_stage = SeasonStage.objects.get(featured=True, season__league=league)
    return season_stage


def create_schedule(dates, games, team_dict):
    """Creates a schedule given list of dates, a same len list of games for said
    date, and a team_dict to map numbers from games to teamseason objects.
    dates - list of dates using datetime.date objects.
    games - list of lists of games, outer list being list of games, inner lists
        being the list of games for given date,
    team_dict - dictionary value that maps to proper team."""
    ss = SeasonStage.objects.all()[2]
    for i in range(len(games)):
        game_date = dates[i]
        for value in games[i]:
            new_game = Game(season=ss, home_team=team_dict[str(value)[1]],
                away_team=team_dict[str(value)[0]], date=game_date)
            new_game.save()

def random_hitting_stats(pgs):
    for p in pgs:
        ab = 3 + randint(0,2)
        bb = randint(0, 5-ab)
        hbp = randint(0,1)
        pa = ab + bb + hbp
        singles = randint(0, ab)
        doubles = 0
        triples = 0
        hr = 0
        xb = randint(0,3)
        if xb in (1,2,3):
                if xb == 1:
                    doubles = 1
                elif xb == 2:
                    triples = 1
                elif xb == 3:
                    hr = 1
        k = 0
        if (singles + doubles + triples + hr) < ab:
            k = randint(0, ab-(singles + doubles + triples + hr))
        runs = randint(0,10)
        run = rbi = hr
        if runs in (4,5,6):
            run = 1 + hr
        if runs in (1,2,3):
            rbi = 1 + hr
        p.at_bats = ab
        p.plate_appearances = pa
        p.runs = run
        p.strikeouts = k
        p.walks = bb
        p.singles = singles
        p.doubles = doubles
        p.triples = triples
        p.homeruns = hr
        p.runs_batted_in = rbi
        p.hit_by_pitch = hbp
        sb = randint(0,10)
        if sb == 9:
            p.stolen_bases = 1
        elif sb == 6:
            p.stolen_bases = 1
        p.save()


def tally_game_runs(games_queryset):
    games = games_queryset

    for game in games:
        tgs = game.teamgamestats_set.all()
        for team in tgs:
            ps = team.playerhittinggamestats_set.all()
            runs = 0
            for p in ps:
                runs += p.runs
            if team.team == game.home_team:
                game.home_score = runs
            elif team.team == game.away_team:
                game.away_score = runs
            game.save()



def equalize_runs_rbis(games_queryset):
    games = games_queryset
    for game in games:
        tgs = game.teamgamestats_set.all()
        for team in tgs:
            ps = team.playerhittinggamestats_set.all()
            runs = 0
            rbi = 0
            for p in ps:
                runs += p.runs
                rbi += p.runs_batted_in
            if rbi > runs:
                for p in ps:
                    if p.runs < (p.hits + p.walks + p.hit_by_pitch):
                        p.runs += (rbi - runs)
                        p.save()
                        break








