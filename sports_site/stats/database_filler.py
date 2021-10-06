from league.models import League, Game, SeasonStage
from random import randint, choice
from django.db.models import  Sum
from math import floor



def get_league(url="SBBL"):
    """Gets and returns league model object based of url slug."""
    league = League.objects.get(url=url)
    return league


def get_featured_season_stage(league=None):
    """Gets featured season stage and returns it given league object."""
    season_stage = SeasonStage.objects.get(featured=True, season__league=league)
    return season_stage


def get_games(season_stage):
    """Gets all games in given season stage."""
    games = season_stage.game_set.all()
    return games


def create_schedule(dates, games, team_dict):
    """
    Creates a schedule given list of dates, a same len list of games
    for said date, and a team_dict to map numbers from games to
    teamseason objects.
    Params:
        dates - list of dates using datetime.date objects.
        games - list of lists of games, outer list being list of games,
            inner lists being the list of games for given date,
        team_dict - dictionary value that maps to proper team.
    """
    ss = SeasonStage.objects.all()[2]
    for i in range(len(games)):
        game_date = dates[i]
        for value in games[i]:
            new_game = Game(season=ss, home_team=team_dict[str(value)[1]],
                away_team=team_dict[str(value)[0]], date=game_date)
            new_game.save()


def random_hitting_stats(pgs):
    """
    Params:
        pgs - player game stats queryset.
    """
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


def create_pitching_stats(tgs):
    """
    Params:
        tgs - TeamGameStats object
    """
    for game in tgs:
        pgs = game.playerpitchinggamestats_set.all()


        team1 = pgs[0].team_stats
        team_one = []
        team_two = []
        for player in pgs:
            if player.team_stats == team1:
                team_one.append(player)
            else:
                team_two.append(player)

        tgs1 = team_one[0].team_stats
        tgs2 = team_two[0].team_stats


        random_pitching_stats(team_one, tgs1, tgs2)
        random_pitching_stats(team_two, tgs2, tgs1)


def total_hitting_stats(hqs):
    """Totals up a queryset of players hitting stats in a game.
    Params:
        hgs - Queryset of PlayerHittingGameStats"""


    return_stats = hqs.aggregate(
        at_bats = Sum('at_bats'),
        plate_appearances = Sum('plate_appearances'),
        runs = Sum('runs'),
        hits = Sum('hits'),
        doubles = Sum('doubles'),
        triples = Sum('triples'),
        homeruns = Sum('homeruns'),
        runs_batted_in = Sum('runs_batted_in'),
        walks = Sum('walks'),
        strikeouts = Sum('strikeouts'),
        stolen_bases = Sum('stolen_bases'),
        caught_stealing = Sum('caught_stealing'),
        hit_by_pitch = Sum('hit_by_pitch'),
        sacrifice_flies = Sum('sacrifice_flies'),
        )

    return return_stats


"""
For random_pitching_innings: Copy base into bash, tabs are spaces.
from stats.models import TeamGameStats
from league.models import SeasonStage
from stats.database_filler import random_pitching_innings
ss = SeasonStage.objects.all()[2]
tgs = TeamGameStats.objects.all().filter(season=ss, game__date__year=2021)
for game in tgs:
    pgs = game.playerpitchinggamestats_set.all()
    random_pitching_innings(pgs)
    print('Done')
"""
def random_pitching_innings(pgs):
    """
    Params:
        pgs - List of all PlayerPitchingGameStats for a team in a game.
        tgs1 - TeamGameStats of the team listed in pgs
        tgs2 - TeamGameStats of opposing team
    """
    starter_innings = [5, 5.1, 5.2, 6, 6.1, 6.2, 7]
    inning_outs = {0:0, 0.1:1, 0.2:2, 1:3, 1.1:4, 1.2:5, 2:6, 2.1:7, 2.2:8, 3:9,
        3.1:10, 3.2:11, 4:12, 4.1:13, 4.2:14, 5:15, 5.1:16, 5.2:17, 6:18,
        6.1:19, 6.2:20, 7:21, 7.1:22, 7.2:23, 8:24, 8.1:25, 8.2:26, 9:27}
    outs_inning = {0: 0, 1: 0.1, 2: 0.2, 3: 1, 4: 1.1, 5: 1.2, 6: 2, 7: 2.1,
        8: 2.2, 9: 3, 10: 3.1, 11: 3.2, 12: 4, 13: 4.1, 14: 4.2, 15: 5, 16: 5.1,
        17: 5.2, 18: 6, 19: 6.1, 20: 6.2, 21: 7, 22: 7.1, 23: 7.2, 24: 8,
        25: 8.1, 26: 8.2, 27: 9}
    totals_outs = 27
    pitchers = len(pgs)

    starter = False

    if len(pgs) == 1 and starter == False:
        pgs[0].complete_game == 1
        pgs[0].innings_pitched == 9

    for player in pgs:
        if starter == False:
            player.innings_pitched = choice(starter_innings)
            player.game_started = 1
            player.game = 1
            starter = True
            starter_outs = inning_outs[player.innings_pitched]
            totals_outs -= starter_outs
            pitchers -= 1
        elif pitchers == 1:
            player.innings_pitched = outs_inning[totals_outs]
            player.game = 1
        else:
            possible_outs = totals_outs - pitchers
            if possible_outs > 1:
                player.innings_pitched = outs_inning[randint(1, possible_outs)]
            elif possible_outs == 1:
                player.innings_pitched = possible_outs
            else:
                pass

            real_outs = inning_outs[player.innings_pitched]

            totals_outs -= real_outs
            pitchers -= 1
            player.game = 1


        player.save()


'''
For random_pitching_stats: Copy base into bash, tabs are spaces.

from stats.models import TeamGameStats
from league.models import SeasonStage, Game
from stats.database_filler import random_pitching_stats
ss = SeasonStage.objects.all()[2]
games = Game.objects.all().filter(season=ss, date__year=2021)
for game in games:
    tgs = game.teamgamestats_set.all()
    tgs1 = tgs[0]
    tgs2 = tgs[1]
    for g in tgs:
        print(g, end='')
        pgs = g.playerpitchinggamestats_set.all()
        if g == tgs1:
            random_pitching_stats(pgs, g, tgs2)
        else:
            random_pitching_stats(pgs, g, tgs1)
    print("Done Game")
'''
def random_pitching_stats(pgs, tgs1, tgs2):
    """
    Params:
        pgs - List of all PlayerPitchingGameStats for a team in a game.
        tgs1 - TeamGameStats of the team listed in pgs
        tgs2 - TeamGameStats of opposing team

    """
    inning_outs = {0:0, 0.1:1, 0.2:2, 1:3, 1.1:4, 1.2:5, 2:6, 2.1:7, 2.2:8, 3:9,
        3.1:10, 3.2:11, 4:12, 4.1:13, 4.2:14, 5:15, 5.1:16, 5.2:17, 6:18,
        6.1:19, 6.2:20, 7:21, 7.1:22, 7.2:23, 8:24, 8.1:25, 8.2:26, 9:27}

    total_outs = 27

    ths2 = total_hitting_stats(tgs2.playerhittinggamestats_set.all())
    total_hits = hits_left = ths2["hits"]
    total_bb = bb_left = ths2["walks"]
    total_k = k_left = ths2["strikeouts"]
    total_sb = sb_left = ths2["stolen_bases"]
    total_cs = cs_left = ths2["caught_stealing"]
    total_hbp = hbp_left = ths2["hit_by_pitch"]

    last_player = pgs.last()
    for player in pgs:
        pitch_outs = inning_outs[player.innings_pitched]

        #hits:
        if player == last_player:
            if hits_left > 0:
                hits_allowed = hits_left
            else:
                hits_allowed = 0
        elif hits_left:
            hits_allowed = floor((pitch_outs/total_outs)*total_hits)
            hits_left -= hits_allowed
        else:
            hits_allowed = 0
        player.hits_allowed = hits_allowed

        #walks:
        if player == last_player:
            if bb_left > 0:
                bb_allowed = bb_left
            else:
                bb_allowed = 0
        elif bb_left:
            bb_allowed = floor((pitch_outs/total_outs)*total_bb)
            bb_left -= bb_allowed
        else:
            bb_allowed = 0
        player.walks_allowed = bb_allowed

        #hit by pitch
        if player == last_player:
            if hbp_left > 0:
                hbp_allowed = hbp_left
            else:
                hbp_allowed = 0
        elif hbp_left:
            hbp_allowed = floor((pitch_outs/total_outs)*total_hbp)
            hbp_left -= hbp_allowed
        else:
            hbp_allowed = 0
        player.hit_batters = hbp_allowed

        #strikeouts
        if player == last_player:
            if k_left > 0:
                k_allowed = k_left
            else:
                k_allowed = 0
        elif k_left:
            k_allowed = floor((pitch_outs/total_outs)*total_k)
            k_left -= k_allowed
        else:
            k_allowed = 0
        player.strikeouts = k_allowed


        #caught_stealing
        if player == last_player:
            if cs_left > 0:
                cs_allowed = cs_left
            else:
                cs_allowed = 0
        elif cs_left:
            cs_allowed = floor((pitch_outs/total_outs)*total_cs)
            cs_left -= cs_allowed
        else:
            cs_allowed = 0
        player.runners_caught_stealing = cs_allowed

        #stolen bases
        if player == last_player:
            if sb_left > 0:
                sb_allowed = sb_left
            else:
                sb_allowed = 0
        elif sb_left:
            sb_allowed = floor((pitch_outs/total_outs)*total_sb)
            sb_left -= sb_allowed
        else:
            sb_allowed = 0
        player.stolen_bases_allowed = sb_allowed


        player.save()



'''
For random_pitching_runs: Copy base into bash, tabs are spaces.

from stats.models import TeamGameStats
from league.models import SeasonStage, Game
from stats.database_filler import random_pitching_runs
ss = SeasonStage.objects.all()[2]
games = Game.objects.all().filter(season=ss, date__year=2021)
for game in games:
    tgs = game.teamgamestats_set.all()
    tgs1 = tgs[0]
    tgs2 = tgs[1]
    for g in tgs:
        print(g, end='')
        pgs = g.playerpitchinggamestats_set.all()
        if g == tgs1:
            random_pitching_runs(pgs, g, tgs2)
        else:
            random_pitching_runs(pgs, g, tgs1)
    print("Done Game")
'''
def random_pitching_runs(pgs, tgs1, tgs2):
    """
    Params:
        pgs - List of all PlayerPitchingGameStats for a team in a game.
        tgs1 - TeamGameStats of the team listed in pgs
        tgs2 - TeamGameStats of opposing team
    """
    inning_outs = {0:0, 0.1:1, 0.2:2, 1:3, 1.1:4, 1.2:5, 2:6, 2.1:7, 2.2:8, 3:9,
        3.1:10, 3.2:11, 4:12, 4.1:13, 4.2:14, 5:15, 5.1:16, 5.2:17, 6:18,
        6.1:19, 6.2:20, 7:21, 7.1:22, 7.2:23, 8:24, 8.1:25, 8.2:26, 9:27}

    outs_left = 27

    t1_linescore = tgs1.teamgamelinescore_set.get()
    tls1 = [
        t1_linescore.first,   t1_linescore.second, t1_linescore.third,
        t1_linescore.fourth,  t1_linescore.fifth,  t1_linescore.sixth,
        t1_linescore.seventh, t1_linescore.eighth,  t1_linescore.ninth
        ]

    t2_linescore = tgs2.teamgamelinescore_set.get()
    tls2 = [
        t2_linescore.first,   t2_linescore.second, t2_linescore.third,
        t2_linescore.fourth,  t2_linescore.fifth,  t2_linescore.sixth,
        t2_linescore.seventh, t2_linescore.eighth,  t2_linescore.ninth
        ]
    ths2 = total_hitting_stats(tgs2.playerhittinggamestats_set.all())
    total_runs = runs_left = ths2["runs"]
    total_homeruns = hr_left = ths2["homeruns"]


    outs = 0
    last_player = pgs.last()
    for player in pgs:
        pitch_outs = inning_outs[player.innings_pitched]
        outs_left -= pitch_outs
        rf = 0
        ra = 0

        for index in range(outs, outs+pitch_outs, 3):
            inning_index = index//3
            rf += tls1[inning_index]
            ra += tls2[inning_index]
            tls1[inning_index] = tls2[inning_index] = 0
        outs+= pitch_outs

        player.runs_allowed = ra
        player.earned_runs = ra
        runs_left -= ra

        if player == last_player:
            hr = hr_left
        elif hr_left:
            hr = floor((ra/total_runs)* total_homeruns)
            hr_left -= hr
        else:
            hr = 0
        player.homeruns_allowed = hr

        player.save()



'''
For random_pitching_decision: Copy base into bash, tabs are spaces.

from stats.models import TeamGameStats
from league.models import SeasonStage, Game
from stats.database_filler import random_pitching_decision
ss = SeasonStage.objects.all()[2]
games = Game.objects.all().filter(season=ss, date__year=2021)
for game in games:
    tgs = game.teamgamestats_set.all()
    tgs1 = tgs[0]
    tgs2 = tgs[1]
    for g in tgs:
        print(g, end='')
        pgs = g.playerpitchinggamestats_set.all()
        if g == tgs1:
            random_pitching_decision(pgs, g, tgs2)
        else:
            random_pitching_decision(pgs, g, tgs1)
    print("Done Game")
'''
def random_pitching_decision(pgs, tgs1, tgs2):
    """
    Params:
        pgs - List of all PlayerPitchingGameStats for a team in a game.
        tgs1 - TeamGameStats of the team listed in pgs
        tgs2 - TeamGameStats of opposing team

        Asumptions:
            1st pitcher pitches >5 innings, so sets leading teams
            starter as initial winning pitcher.
    """
    inning_outs = {0:0, 0.1:1, 0.2:2, 1:3, 1.1:4, 1.2:5, 2:6, 2.1:7, 2.2:8, 3:9,
        3.1:10, 3.2:11, 4:12, 4.1:13, 4.2:14, 5:15, 5.1:16, 5.2:17, 6:18,
        6.1:19, 6.2:20, 7:21, 7.1:22, 7.2:23, 8:24, 8.1:25, 8.2:26, 9:27}

    outs_left = 27

    t1_linescore = tgs1.teamgamelinescore_set.get()
    tls1 = [
        t1_linescore.first,   t1_linescore.second, t1_linescore.third,
        t1_linescore.fourth,  t1_linescore.fifth,  t1_linescore.sixth,
        t1_linescore.seventh, t1_linescore.eighth,  t1_linescore.ninth
        ]

    t2_linescore = tgs2.teamgamelinescore_set.get()
    tls2 = [
        t2_linescore.first,   t2_linescore.second, t2_linescore.third,
        t2_linescore.fourth,  t2_linescore.fifth,  t2_linescore.sixth,
        t2_linescore.seventh, t2_linescore.eighth,  t2_linescore.ninth
        ]

    outs = 0
    lead = None
    tied = None
    deciding_pitcher = pgs.first()
    pitcher_save = None
    cur_rf = 0
    cur_ra = 0
    for player in pgs:
        pitch_outs = inning_outs[player.innings_pitched]
        outs_left -= pitch_outs
        rf = 0
        ra = 0

        #update runs and score for current player.
        for index in range(outs, outs+pitch_outs, 3):
            inning_index = index//3
            rf += tls1[inning_index]
            ra += tls2[inning_index]
            tls1[inning_index] = tls2[inning_index] = 0



        outs+= pitch_outs
        cur_rf += rf
        cur_ra += ra

        if cur_rf > cur_ra:
            if lead:
                #were winning, still winning - nothing
                pass
            else:
                #tied/losing - now winning
                deciding_pitcher = player
            lead = True
            tied = False
        elif cur_rf == cur_ra:
            #currently tied -- inline for win, lose, draw
            deciding_pitcher = player
            lead = False
            tied = True
        else:
            #else covers losing cur_rf < cur_ra:
            if lead:
                #were winning, now losing
                deciding_pitcher = player
            elif tied:
                #were tied, now losing
                deciding_pitcher = player
            else:
                #were losing, still losing
                pass

            lead = False
            tied = False

        if inning_index == 8 and player.innings_pitched >= 1 and 1 <= cur_rf - cur_ra <= 3:
            if player != deciding_pitcher:
                player.save_op += 1
                pitcher_save = player
                player.save()
        elif inning_index == 8 and player.innings_pitched >= 0.2 and 1 <= cur_rf - cur_ra >= 2:
            if player != deciding_pitcher:
                player.save_op += 1
                pitcher_save = player
                player.save()
        elif inning_index == 7 and player.innings_pitched >= 1.1 and 1 <= cur_rf - cur_ra <= 3:
            if player != deciding_pitcher:
                player.save_op += 1
                pitcher_save = player
                player.save()
        else:
            player.save_op = 0

    if tgs1.runs_for == tgs1.runs_against:
        deciding_pitcher.win = 0
        deciding_pitcher.loss = 0
    elif lead:
        deciding_pitcher.win = 1
        deciding_pitcher.save_op = 0
    elif not lead:
        deciding_pitcher.loss = 1

    deciding_pitcher.save()

    if pitcher_save and pitcher_save != deciding_pitcher:
        if tgs1.runs_for > tgs1.runs_against:
            pitcher_save.save_converted = 1
            pitcher_save.save()


