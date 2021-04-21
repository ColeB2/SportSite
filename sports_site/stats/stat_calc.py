def _convert_to_int(string_value):
    if '.' in string_value:
        ret_val = ''
        for char in string_value:
            if char != '.':
                ret_val += char
        return int(ret_val)
    elif string_value[0:1] == '.' :
        return int(string_value[1:])

def _calc_average(hits, at_bats):
    """Calcuates batting average and returns its as a string in .### format"""
    if at_bats == 0:
        return f".000"

    average = int(1000*round((hits / at_bats), 3))

    if average == 1000:
        return f"{str(average)[0:1]}.{str(average)[1:]}"
    else:
        return f".{average}"

def _calc_obp(hits, walks, hit_by_pitch, at_bats, sacrifice_flies):
    if at_bats == 0:
        return f".000"
    top = hits + walks + hit_by_pitch
    bot = at_bats + walks + hit_by_pitch + sacrifice_flies

    obp = int(1000*round((top / bot),3))

    if obp == 1000:
        return f"{str(obp)[0:1]}.{str(obp)[1:]}"
    else:
        return f".{obp}"

def _calc_slugging(singles, doubles, triples, homeruns, at_bats):
    if at_bats == 0:
        return f".000"

    top = singles + (doubles*2) + (triples*3) + (homeruns*4)
    bot = at_bats

    slg = int(1000*round((top / bot),3))

    if slg >= 1000:
        return f"{str(slg)[0:1]}.{str(slg)[1:]}"
    else:
        return f".{slg}"

def _calc_ops(on_base_percentage, slugging_percentage):
    obp = _convert_to_int(on_base_percentage)
    slg = _convert_to_int(slugging_percentage)
    try:
        ops = obp+slg
    except:
        return f".000"

    if ops >= 1000:
        return f"{str(ops)[0:1]}.{str(ops)[1:]}"
    else:
        return f".{ops}"

def _calc_win_pct(wins, losses, ties):
    if wins == 0 and losses == 0:
        return f".000"

    pct = int(1000*round(( (wins+(ties/2)) / (wins+losses+ties) ),3))

    if pct == 1000:
        return f"{str(pct)[0:1]}.{str(pct)[1:]}"
    else:
        return f".{pct}"