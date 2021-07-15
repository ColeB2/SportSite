def _convert_to_int(string_value):
    if '.' in string_value:
        ret_val = ''
        for char in string_value:
            if char != '.':
                ret_val += char
        return int(ret_val)
    elif string_value[0:1] == '.' :
        return int(string_value[1:])

def _normalize_str_length(str_value, req_length):
    if len(str_value) != req_length:
        for i in range(req_length - len(str_value)):
            str_value +='0'
    return str_value


def _convert_to_str(float):
    if float == 0:
        return ".000"

    str_value = str(round(float,3))

    if str_value[0] != '0':
        str_value = _normalize_str_length(str_value, 5)
    else:
        str_value = str_value[1:]
        str_value = _normalize_str_length(str_value, 4)



    return str_value

def _calc_average(hits, at_bats):
    if at_bats:
        return round(float(hits/at_bats),3)
    else:
        return float(0)

def _calc_obp(hits, walks, hit_by_pitch, at_bats, sacrifice_flies):
    top = hits + walks + hit_by_pitch
    bot = at_bats + walks + hit_by_pitch + sacrifice_flies
    if bot != 0:
        return round(float(top/bot),3)
    else:
        return float(0)

def _calc_slugging(singles, doubles, triples, homeruns, at_bats):
    top = singles + (doubles*2) + (triples*3) + (homeruns*4)
    if at_bats:
        return round(float(top/at_bats),3)
    else:
        return float(0)

def _calc_ops(on_base_percentage, slugging_percentage):
    return round(float(on_base_percentage + slugging_percentage),3)

def _calc_whip(walks, hits, innings_pitched):
    if innings_pitched:
        return round(float( (walks+hits) / innings_pitched),2)
    else:
        return float(0)

def _calc_era(earned_runs, innings_pitched, innings=9):
    if innings_pitched:
        return round(float((earned_runs*innings)/innings_pitched), 2)
    else:
        return float(0)

def _calc_win_pct(wins, losses, ties):
    return ((wins+(ties/2)) / (wins+losses+ties))

def _convert_ip_to_outs(innings_pitched):
    value = round(innings_pitched)
    putouts = value*3
    decimal = round(innings_pitched%1, 1)
    if decimal == 0.1:
        putouts += 1
    elif decimal == 0.2:
        putouts += 2

    return putouts


def _calc_pitchers_avg(hits_allowed, innings_pitched, PK, CS):
    """rudimentary basic way to calculate average for pitchers"""
    outs = _convert_ip_to_outs(innings_pitched)
    return hits_allowed / ((hits_allowed+outs)-(PK+ CS))
