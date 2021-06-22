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

    return float(hits/at_bats)

def _calc_obp(hits, walks, hit_by_pitch, at_bats, sacrifice_flies):
    top = hits + walks + hit_by_pitch
    bot = at_bats + walks + hit_by_pitch + sacrifice_flies
    return float(top/bot)

def _calc_slugging(singles, doubles, triples, homeruns, at_bats):
    top = singles + (doubles*2) + (triples*3) + (homeruns*4)
    bot = at_bats
    return float(top/bot)

def _calc_ops(on_base_percentage, slugging_percentage):
    return float(on_base_percentage + slugging_percentage)

def _calc_win_pct(wins, losses, ties):
    if wins == 0 and losses == 0:
        return f".000"

    pct = int(1000*round(( (wins+(ties/2)) / (wins+losses+ties) ),3))

    if pct == 1000:
        return f"{str(pct)[0:1]}.{str(pct)[1:]}"
    else:
        return f".{pct}"