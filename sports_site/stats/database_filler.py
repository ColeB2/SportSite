from league.models import Game, TeamSeason, SeasonStage
'''
dates = [datetime.date(2021,5,14), datetime.date(2021,5,16),datetime.date(2021,5,21),datetime.date(2021,5,23),datetime.date(2021,5,28),datetime.date(2021,5,30),datetime.date(2021,6,4),datetime.date(2021,6,6),datetime.date(2021,6,11),datetime.date(2021,6,13),datetime.date(2021,6,18),datetime.date(2021,6,20),datetime.date(2021,6,25),datetime.date(2021,6,27),datetime.date(2021,7,2),datetime.date(2021,7,4)]
g = [[41,52,36], [21,43,65],[13,62,54],[16,35,24],[15,64,32],[41,25,63],[12,34,56],[31,26,45],[61,53,42],[51,46,23],[14,52,36],[21,43,65],[13,62,54],[16,35,24],[15,64,32],[41,25,63]]
td = {'2':teams[0], '1':teams[1], '3':teams[2], '4':teams[3], '5':teams[4], '6':teams[5]}
'''
def create_schedule(dates, games, team_dict):
    """Creates a schedule given list of dates, a same len list of games for said
    date, and a team_dict to map numbers from games to teamseason objects.
    dates - list of dates using datetime.date objects.
    games - list of lists of games, outer list being list of games, inner lists
        being the list of games for given date,
    team_dict - dictionary value that maps to proper team."""
    for i in range(len(games)):
        game_date = dates[i]
        for value in games[i]:
            new_game = Game(season=ss, home_team=team_dict[str(value)[1]],
                away_team=team_dict[str(value)[0]], date=game_date)
            new_game.save()