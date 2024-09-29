import discord
from discord import app_commands
from discord.ext import commands
import asyncio

import csv
import math
from math import log, pow
from timeit import default_timer as timer

with open("ceva.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    lista_csv = list(csv_reader)

max_day = int(lista_csv[-1][0])

matrice_babana = \
    [[0, 0, 0], [1000, 0, 0], [2000, 9, "ak"], [3000, 108, "at"], [4000, 254, "bc"], [5000, 11, "bm"],
     [6000, 19, "bv"],
     [7000, 127, "ce"], [8000, 650, "cn"], [9000, 3, "cx"], [10000, 17, "dg"], [11000, 59, "dp"], [12000, 2, "dz"],
     [13000, 12, "ei"], [14000, 70, "er"], [15000, 398, "fa"], [16000, 2, "fk"], [17000, 13, "ft"], [18000, 74, "gc"],
     [19000, 426, "gl"], [20000, 2, "gv"], [21000, 14, "he"], [22000, 80, "hn"], [23000, 455, "hw"], [24000, 3, "ig"],
     [25000, 15, "ip"], [26000, 85, "iy"], [27000, 486, "jh"], [28000, 3, "jr"], [29000, 16, "ka"], [30000, 91, "kj"],
     [31000, 519, "ks"], [32000, 3, "lc"], [33000, 17, "ll"], [34000, 97, "lu"], [35000, 555, "md"], [36000, 3, "mn"],
     [37000, 18, "mw"]]

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z"]

boss = ["demon", "caveman", "dragon", "caveman", "skeleton", "dragon", "minotaur", "skeleton", "demon", "minotaur",
        "demon", "caveman", "dragon", "caveman", "zombies", "dragon", "witch", "zombies", "demon", "witch"]
boss_scores = [0.31, 0.31, 0.41, 0.31, 0.31, 0.41, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.41, 0.31, 0.41, 0.41, 0.52,
               0.41, 0.31, 0.52]
boss_scores2 = [6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 8, 6, 8, 8, 10,
                8, 6, 10]
mobs = ["dino", "rex", "shade", "frosk", "blob", "gargoyle", "caps", "warmonger", "banshee"]
mob_scores = [1.93, 1.29, 1.94, 1.00, 1.92, 1.73, 1.92, 1.33, 1.65]

levels = [
    '', 'k', 'm', 'b', 't', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap',
    'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj',
    'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'bz', 'ca', 'cb', 'cc', 'cd',
    'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx',
    'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr',
    'ds', 'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el',
    'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff',
    'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo', 'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz',
    'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt',
    'gu', 'gv', 'gw', 'gx', 'gy', 'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn',
    'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw', 'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih',
    'ii', 'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'iw', 'ix', 'iy', 'iz', 'ja', 'jb',
    'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js', 'jt', 'ju', 'jv',
    'jw', 'jx', 'jy', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp',
    'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj',
    'lk', 'll', 'lm', 'ln', 'lo', 'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'lz', 'ma', 'mb', 'mc', 'md',
    'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx',
    'my', 'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk', 'nl', 'nm', 'nn', 'no', 'np', 'nq', 'nr',
    'ns', 'nt', 'nu', 'nv', 'nw', 'nx', 'ny', 'nz', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi', 'oj', 'ok', 'ol',
    'om', 'on', 'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou', 'ov', 'ow', 'ox', 'oy', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf',
    'pg', 'ph', 'pi', 'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps', 'pt', 'pu', 'pv', 'pw', 'px', 'py', 'pz',
    'qa', 'qb', 'qc', 'qd', 'qe', 'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt',
    'qu', 'qv', 'qw', 'qx', 'qy', 'qz', 'ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn',
    'ro', 'rp', 'rq', 'rr', 'rs', 'rt', 'ru', 'rv', 'rw', 'rx', 'ry', 'rz', 'sa', 'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh',
    'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy', 'sz', 'ta', 'tb',
    'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tq', 'tr', 'ts', 'tt', 'tu', 'tv',
    'tw', 'tx', 'ty', 'tz', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui', 'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up',
    'uq', 'ur', 'us', 'ut', 'uu', 'uv', 'uw', 'ux', 'uy', 'uz', 'va', 'vb', 'vc', 'vd', 've', 'vf', 'vg', 'vh', 'vi', 'vj',
    'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vq', 'vr', 'vs', 'vt', 'vu', 'vv', 'vw', 'vx', 'vy', 'vz', 'wa', 'wb', 'wc', 'wd',
    'we', 'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wq', 'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx',
    'wy', 'wz', 'xa', 'xb', 'xc', 'xd', 'xe', 'xf', 'xg', 'xh', 'xi', 'xj', 'xk', 'xl', 'xm', 'xn', 'xo', 'xp', 'xq', 'xr',
    'xs', 'xt', 'xu', 'xv', 'xw', 'xx', 'xy', 'xz', 'ya', 'yb', 'yc', 'yd', 'ye', 'yf', 'yg', 'yh', 'yi', 'yj', 'yk', 'yl',
    'ym', 'yn', 'yo', 'yp', 'yq', 'yr', 'ys', 'yt', 'yu', 'yv', 'yw', 'yx', 'yy', 'yz', 'za', 'zb', 'zc', 'zd', 'ze', 'zf',
    'zg', 'zh', 'zi', 'zj', 'zk', 'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw', 'zx', 'zy', 'zz'
]


def spot_score(day: int, titor: float, express: bool, tj: bool, double_rewind: bool, mode: int):
    lista = []
    score = 0
    fudge = 0
    if express:
        portal = 10 if day // 500 == 0 else (day // 500) * 10
    else:
        portal = 5 if day // 500 == 0 else (day // 500) * 5
    portal_count = 1
    initial = day
    if tj:
        if double_rewind:
            day = int(spot_round(spot_round(day * 0.75) * 0.75))
        else:
            day = int(spot_round(day * 0.75))
    else:
        if double_rewind:
            day = int(spot_round(spot_round(day * 0.5) * 0.5))
        else:
            day = int(spot_round(day * 0.5))

    froskScore = mob_scores[3]

    while day < initial:
        if mode == 1:
            mobScore = mob_scores[mobs.index(lista_csv[(day // 5) - 1][1].lower())]
        else:
            mobScore = float(lista_csv[(day // 5) - 1][2])
            fudge = get_fudge(initial)
            if fudge == 0:
                return 0

        # currentDay = day if day - 10000 > 0 else 0

        if mode == 1:
            bossScore = boss_scores[day % 100 // 5]
        else:
            bossScore = boss_scores2[day % 100 // 5]

        if express:
            speed = -12 * (day / initial) + 13
        else:
            speed = -4 * (max(day / initial, 0.75)) + 5

        if mode == 2:
            speed *= titor
        if mode == 1:
            score += (froskScore + (mobScore - froskScore) * (1 + (max(day - 10000, 0) / 20000)) + bossScore) / speed
        else:
            score += ((mobScore * fudge) + bossScore) / speed
        day += portal
        portal_count += 1

    dodo_score = score * 19.3191489361702
    lista.append(initial)
    lista.append(round(score, 2) if mode == 1 else round(score))
    lista.append(boss[(day - portal) % 100 // 5].title())
    lista.append(round(dodo_score))
    lista.append(initial - (day - portal))

    return lista


def next_fates_milestone(seconds: int, mode: str):
    if mode == 'easy':
        return exped_secunda(((seconds // 7200) + 1) * 7200)[0]
    elif mode == 'normal':
        return exped_secunda(((seconds // 3600) + 1) * 3600)[0]
    elif mode == 'hard':
        return exped_secunda(((seconds // 1800) + 1) * 1800)[0]
    elif mode == 'hell':
        return exped_secunda(((seconds // 900) + 1) * 900)[0]


def exped_time(daydmg: int, dayletter: str, day: int, damage: int, letter: str, multi: float):
    seconds = 240
    while levels.index(letter) <= levels.index(dayletter):
        if levels.index(letter) != levels.index(dayletter):
            damage *= (multi ** 10)
            if damage > 1000:
                letter = levels[levels.index(letter) + 1]
                damage /= 1000
            seconds += 10
        elif levels.index(letter) == levels.index(dayletter):
            if damage < daydmg:
                damage *= multi
                if damage > 1000:
                    letter = levels[levels.index(letter) + 1]
                    damage /= 1000
                seconds += 1
            else:
                if multi == 1.012874309:
                    return seconds + 1800
                elif multi == 1.032497215:
                    return seconds + 900
                else:
                    return seconds

    if multi == 1.012874309:
        return seconds + 1800
    elif multi == 1.032497215:
        return seconds + 900
    else:
        return seconds


def exped_secunda(numar: int):
    ceva = ""
    if numar >= 3600:
        if numar // 3600 < 10:
            ceva += "0"
        ceva += f"{numar // 3600}:"
    else:
        ceva += '00:'

    if numar // 60 % 60 < 10:
        ceva += '0'
    ceva += f"{numar // 60 % 60}:"
    if numar % 60 < 10:
        ceva += "0"
        ceva += f"{numar % 60}"
    else:
        ceva += f"{numar % 60}"

    print(ceva, numar)
    return ceva, numar


def spot_range(day: int, tj: bool, express: bool, mode: int, double_rewind: bool):
    copy = copy2 = day - 50
    upper, lower = 0, 0
    for i in range(copy, day + 50):
        if portal_compare(copy2, i, tj, express, double_rewind):
            pass
        else:
            if i <= day:
                lower = i
            copy2 = i
            upper = i - 1
            if upper >= day:
                if mode == 1:
                    return f'{lower}-{str(upper)[-2:]}'
                else:
                    return upper


def portal_compare(spot1: int, spot2: int, tj: bool, express: bool, double_rewind: bool):
    # mobs = ["dino", "rex", "shade", "frosk", "blob", "gargoyle", "caps", "warmonger", "banshee"]
    # with open("ceva.csv") as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     lista_csv = list(csv_reader)

    if express:
        portal1 = 10 if spot1 // 500 == 0 else (spot1 // 500) * 10
        portal2 = 10 if spot2 // 500 == 0 else (spot2 // 500) * 10
    else:
        portal1 = 5 if spot1 // 500 == 0 else (spot1 // 500) * 5
        portal2 = 5 if spot2 // 500 == 0 else (spot2 // 500) * 5

    if tj:
        if double_rewind:
            start1 = int(spot_round(spot_round(spot1 * 0.75) * 0.75))
            start2 = int(spot_round(spot_round(spot2 * 0.75) * 0.75))
        else:
            start1 = int(spot_round(spot1 * 0.75))
            start2 = int(spot_round(spot2 * 0.75))
    else:
        if double_rewind:
            start1 = int(spot_round(spot_round(spot1 * 0.5) * 0.5))
            start2 = int(spot_round(spot_round(spot2 * 0.5) * 0.5))
        else:
            start1 = int(spot_round(spot1 * 0.5))
            start2 = int(spot_round(spot2 * 0.5))

    while spot2 > start1:
        mob1 = start1
        mob2 = start2
        if mob1 != mob2:
            return 0

        if start1 < spot1:
            start1 += portal1
        else:
            return 0

        if start2 < spot2:
            start2 += portal2
        else:
            return 0
    # if

    return 1


def spot_round(day: float):
    if day % 10 == 7.5:
        return day + 2.5
    elif day % 10 == 2.5:
        return day - 2.5

    upper, lower = day, day
    while upper % 5 != 0 and lower % 5 != 0:
        upper += 0.25
        lower -= 0.25

    return upper if upper % 5 == 0 else lower


def get_fudge(initial: int):
    if initial < 1000:
        return 0
    elif initial < 2000:
        fudge = 0.7
    elif initial < 4000:
        fudge = 0.89
    elif initial < 5000:
        fudge = 0.82
    elif initial < 6000:
        fudge = 0.78
    elif initial < 8500:
        fudge = 0.87
    elif initial < 9500:
        fudge = 0.95
    elif initial < 10500:
        fudge = 1.05
    elif initial < 11500:
        fudge = 1.17
    elif initial < 12500:
        fudge = 1.31
    elif initial < 13500:
        fudge = 1.38
    elif initial < 14500:
        fudge = 1.45
    elif initial < 15000:
        fudge = 1.48
    elif initial < 15500:
        fudge = 1.53
    elif initial < 16000:
        fudge = 1.57
    elif initial < 20000:
        fudge = 1.63
    elif initial < 25000:
        fudge = (0.21 / 15000) * initial + (1.8 - (0.21 / 15000) * 23000)
    elif initial < 28000:
        fudge = 1.92
    elif initial < 30000:
        fudge = 1.95
    else:
        fudge = 1.99

    return fudge


def secunda(numar: int):
    ceva = ""
    ceva += f"{numar // 60}:"
    if numar % 60 < 10:
        ceva += "0"
        ceva += f"{numar % 60}"
    else:
        ceva += f"{numar % 60}"

    return ceva


def gold_sheet(cdmg: str, gold: str, gold_level: str, keys: str, target: float, invisible: bool):
    global start
    start = timer()
    stat_milestone, milestone = 0, 0
    milestone_suffix = ''

    def stupid_thing_work_please(gold_lvl, key_gold):
        gold_int, gold_suffix = nice_output(gold_lvl)
        gold_int += 0.01
        gold_int = float(gold_int)
        while sn(gold_int * (1000 ** levels.index(gold_suffix)) - gold_lvl, gold_lvl, 1) <= key_gold:
            end = timer()
            if end - start > 30:
                return 0, 0, 0
            gold_int += 0.01
            if gold_int >= 1000:
                gold_int /= 1000
                gold_suffix = levels[levels.index(gold_suffix) + 1]

        multi = (gold_int * (1000 ** levels.index(gold_suffix))) / gold_lvl

        return gold_lvl, int(gold_int * (1000 ** levels.index(gold_suffix))), multi

    def sn(p, b, x):
        if x == 0:
            return int(p * ((2 * (b * 150 + 150) + ((p - 1) * 150)) / 2))
        else:
            return int(p * ((2 * (b * 250000000000 + 250000000000) + ((p - 1) * 250000000000)) / 2))

    def newgold(cdmg_int, gold_int, x):
        p = 1
        while (sn(p, cdmg_int, x)) <= gold_int and len(str(sn(p, cdmg_int, x))) < len(str(gold_int)):
            p *= 10
        p //= 10

        prev = 0
        num_length = len(str(p))

        while sn(p, cdmg_int, x) <= gold_int:
            p += 10 ** (num_length - 1)
            if sn(p, cdmg_int, x) == prev:
                break
            prev = sn(p, cdmg_int, x)
            if sn(p, cdmg_int, 0) > gold_int:
                p -= 10 ** (num_length - 1)
                if num_length > 1:
                    num_length -= 1

        p += cdmg_int
        multii = p / cdmg_int
        return cdmg_int, p, multii

    def days(multi: float, stat_milestone: int):
        return math.log(multi ** 2, 2) * 11 + stat_milestone

    def nice_output(le_int):
        suffix = ''

        while le_int >= 1000:
            le_int /= 1000
            suffix = levels[levels.index(suffix) + 1]
        le_int = le_int

        return le_int, suffix

    def funni_loop(target_gold, gold_level_int, key_gold_int, key_copy):
        target_gold /= 10
        print(f"target {nice_output(target_gold)}\n")
        end = timer()
        if end - start > 30:
            return 0, 0, 0

        def funni_inner_loop(gold_level_int, key_gold_int, key_copy):
            end = timer()
            if end - start > 30:
                return 0, 0, 0
            min_target = 10 ** 250
            i = 10000

            while True:
                end = timer()
                a, b, c = stupid_thing_work_please(gold_level_int, int(key_copy * i))
                if a == 0 or b == 0 or c == 0 or end - start > 30:
                    return 0, 0, 0
                gold_milestone = len(str(b)) - len(str(a))
                new_keys = int(key_copy * c * (pow(2, gold_milestone)))
                zz = (target_gold / new_keys) + int(i * 10)
                if min_target >= ((target_gold / new_keys) * 10) + int(i * 10):
                    min_target = ((target_gold / new_keys) * 10) + int(i * 10)
                else:
                    gold_milestone = 0 if gold_milestone - 1 < 0 else gold_milestone - 1
                    break
                i *= 10

            i /= 10
            num_length = len(str(i))

            while True:
                end = timer()
                i += (10 ** (num_length - 1))
                d, e, f = stupid_thing_work_please(gold_level_int, int(key_copy * i))
                if d == 0 or e == 0 or f == 0 or end - start > 30:
                    return 0, 0, 0
                new_keys = int(key_copy * f * (pow(2, gold_milestone)))
                if min_target >= ((target_gold / new_keys) * 10) + int(i * 10):
                    min_target = ((target_gold / new_keys) * 10) + int(i * 10)
                else:
                    print(i)
                    i -= 10 ** (num_length - 1)
                    if num_length > 1:
                        num_length -= 1
                if num_length == 1:
                    break
            print("ej ok?")
            target_min = min_target
            target_keys = int(i * 10)
            target_cdmg = target_min - target_keys
            print("nu")

            return target_min, target_keys, target_cdmg

        target_min, target_keys, target_cdmg = funni_inner_loop(gold_level_int, key_copy, key_copy)
        if target_min == 0:
            return 0, 0, 0
        return target_min, target_keys, target_cdmg

    cdmg = cdmg.lower().strip()
    gold = gold.lower().strip()
    keys = keys.lower().strip()
    gold_level = gold_level.lower().strip()

    stat_milestone, milestone = 0, 0
    milestone_suffix = ''

    try:
        cdmg_suffix = '' if cdmg[-1].isdigit() else (cdmg[-1:] if cdmg[-2].isdigit() else cdmg[-2:])
        cdmg_int = abs(float(cdmg) if cdmg[-1].isdigit() else (float(cdmg[:-1]) if cdmg[-2].isdigit() else abs(float(cdmg[:-2]))))
        cdmg_int *= (1000 ** (levels.index(cdmg_suffix)))
        cdmg_int = int(cdmg_int)

        gold_suffix = '' if gold[-1].isdigit() else (gold[-1:] if gold[-2].isdigit() else gold[-2:])
        gold_int = abs(float(gold) if gold[-1].isdigit() else (float(gold[:-1]) if gold[-2].isdigit() else abs(float(gold[:-2]))))
        gold_int *= (1000 ** (levels.index(gold_suffix)))
        gold_int = int(gold_int)

        keys_suffix = '' if keys[-1].isdigit() else (keys[-1:] if keys[-2].isdigit() else keys[-2:])
        keys_int = abs(float(keys) if keys[-1].isdigit() else (float(keys[:-1]) if keys[-2].isdigit() else abs(float(keys[:-2]))))
        keys_int *= (1000 ** (levels.index(keys_suffix)))
        keys_int = int(keys_int)

        gold_level_suffix = '' if gold_level[-1].isdigit() else (gold_level[-1:] if gold_level[-2].isdigit() else gold_level[-2:])
        gold_level_int = abs(float(gold_level) if gold_level[-1].isdigit() else (float(gold_level[:-1]) if gold_level[-2].isdigit() else abs(float(gold_level[:-2]))))
        gold_level_int *= (1000 ** levels.index(gold_level_suffix))
        gold_level_int = int(gold_level_int)
        if keys_int > gold_int:
            return 0

    except ValueError:
        return 0

    key_gold_int = gold_int if keys_int <= 10 else int(gold_int / (keys_int // 10))
    key_copy = key_gold_int
    key_gold_int *= 1 if keys_int <= 10 else keys_int // 10
    gold_int = key_gold_int
    cdmg_copy = cdmg_int

    cdmg_copy_int, cdmg_copy_suffix = nice_output(cdmg_copy)
    cdmg_int, cdmg_suffix = nice_output(cdmg_int)

    cdmg_int_2, p, nothing = newgold(cdmg_copy, gold_int, 0)
    if len(str(int(cdmg_int))) == 1:
        milestone = 10
        milestone_suffix = cdmg_suffix
    elif len(str(int(cdmg_int))) == 2:
        milestone = 100
        milestone_suffix = cdmg_suffix
    elif len(str(int(cdmg_int))) == 3:
        milestone = 1
        milestone_suffix = levels[levels.index(cdmg_suffix) + 1]

    milestone_gold_int = sn((milestone * (1000 ** (levels.index(milestone_suffix)))) - cdmg_copy, cdmg_copy, 0)
    keys_req_int, keys_req_suffix = nice_output((milestone_gold_int / key_copy) * 10)
    keys_req_int = 10 if keys_req_suffix == '' and keys_req_int < 10 else keys_req_int
    target_start, target_start_suffix = nice_output(cdmg_copy)
    milestone_gold, milestone_gold_suffix = nice_output(milestone_gold_int)

    while days((target_start * (1000 ** (levels.index(target_start_suffix) - levels.index(cdmg_copy_suffix)))) / cdmg_copy_int, stat_milestone) <= target:
        target_start += 0.01
        stat_milestone = (len(str(int(target_start * (1000 ** levels.index(target_start_suffix))))) - len(str(int(cdmg_copy_int * (1000 ** levels.index(cdmg_copy_suffix)))))) * 22 if \
            len(str(int(cdmg_copy_int * (1000 ** levels.index(cdmg_copy_suffix))))) >= 5 else 0
        if target_start > 1000:
            target_start /= 1000
            target_start_suffix = levels[levels.index(target_start_suffix) + 1]

    p = int(p)
    target_gold = sn((target_start * (1000 ** (levels.index(target_start_suffix))) - cdmg_copy), cdmg_copy, 0) * 10
    target_gold_int, target_gold_suffix = nice_output(sn((target_start * (1000 ** (levels.index(target_start_suffix))) - cdmg_copy), cdmg_copy, 0))
    target_end, target_end_suffix = nice_output(target_start * (1000 ** (levels.index(target_start_suffix))))
    target_keys, target_keys_suffix = nice_output((sn((target_start * (1000 ** (levels.index(target_start_suffix))) - cdmg_copy), cdmg_copy, 0) / key_copy) * 10)
    target_keys = 10 if target_keys_suffix == '' and target_keys < 10 else target_keys
    current_days = days(p / cdmg_int_2, (len(str(int(p))) - len(str(int(cdmg_copy)))) * 22)
    milestone_days = days((milestone * (1000 ** levels.index(milestone_suffix))) / cdmg_copy, 22)

    min_target, min_target_keys, min_target_cdmg = funni_loop(target_gold, gold_level_int, key_gold_int, key_copy)
    min_milestone, min_milestone_keys, min_milestone_cdmg = funni_loop(milestone_gold_int * 10, gold_level_int, key_gold_int, key_copy)
    overshot = days((target_start * (1000 ** (levels.index(target_start_suffix) - levels.index(cdmg_copy_suffix)))) / cdmg_copy_int, stat_milestone) - target

    print("a ok")

    # if min_target == 0 or min_milestone == 0:
    #    return 0
    if min_milestone == 0:
        min_milestone = min_target
        min_milestone_keys = min_target_keys
        min_milestone_cdmg = min_target_cdmg

    print(f"final min {min_target}")
    print(f"final milestone {min_milestone}")

    print(f"{format(current_days, '.2f')} days din current keys")
    print(f"{format(target_keys, '.2f')}{target_keys_suffix} keys pt target")
    print(f"{format(target_gold_int, '.2f')}{target_gold_suffix} gold pt target")
    print(f"{format(target_end, '.2f')}{target_end_suffix} pt target")
    print(f"{format(keys_req_int, '.2f')}{keys_req_suffix} milestone keys req")
    print(f"{milestone}{milestone_suffix} milestone")
    print(f"{format(milestone_days, '.2f')} days from milestone")
    print(f"{format(milestone_gold, '.2f')}{milestone_gold_suffix} gold pt milestone")

    embed = discord.Embed(title="Dungeon Gold Calculator <a:kafkakurukuru:1118233531110412461>\n"
                                "__DISCLAIMER: It's only recommended to use this if you have V7 Runes__", color=0x71368a)
    embed.add_field(name="Do you want to make a quick adjustment? Long tap/copy the command you just used!",
                    value=f"/calc dungeon_gold crit_dmg_stat_level: {cdmg} gold_stat_level: {gold_level} gold_from_dungeon_keys: {gold} "
                          f"current_keys: {keys} days_you_want_to_progress: {target} invisible: {invisible}", inline=False)
    embed.add_field(name="----------- Target days data -----------",
                    value=f"- {format(nice_output(min_target)[0], '.2f')}{nice_output(min_target)[1].upper() if nice_output(min_target)[1] in ['k', 'm', 'b', 't'] else nice_output(min_target)[1]} Minimum Keys\n"
                          f" - {format(nice_output(min_target_keys)[0], '.2f')}{nice_output(min_target_keys)[1].upper() if nice_output(min_target_keys)[1] in ['k', 'm', 'b', 't'] else nice_output(min_target_keys)[1]} Keys into Gold Stat\n"
                          f" - {format(nice_output(min_target_cdmg)[0], '.2f')}"
                          f"{nice_output(min_target_cdmg)[1].upper() if nice_output(min_target_cdmg)[1] in ['k', 'm', 'b', 't'] else nice_output(min_target_cdmg)[1]} Keys into Crit Dmg Stat\n"
                          f"- {format(target_end, '.2f')}{target_end_suffix} Crit Dmg Level (overshot by {format(overshot, '.2f')} days)\n"
                          f"- {format(target_gold_int, '.2f')}{target_gold_suffix} Gold\n"
                          f"- {format(current_days, '.2f')} Days from current Keys", inline=False)

    embed.add_field(name="------ Nearest Crit DMG Milestone data ------",
                    value=f"- {format(nice_output(min_milestone)[0], '.2f')}{nice_output(min_milestone)[1].upper() if nice_output(min_milestone)[1] in ['k', 'm', 'b', 't'] else nice_output(min_milestone)[1]} Minimum Keys\n"
                          f" - {format(nice_output(min_milestone_keys)[0], '.2f')}{nice_output(min_milestone_keys)[1].upper() if nice_output(min_milestone_keys)[1] in ['k', 'm', 'b', 't'] else nice_output(min_milestone_keys)[1]} Keys into Gold Stat\n"
                          f" - {format(nice_output(min_milestone_cdmg)[0], '.2f')}"
                          f"{nice_output(min_milestone_cdmg)[1].upper() if nice_output(min_milestone_cdmg)[1] in ['k', 'm', 'b', 't'] else nice_output(min_milestone_cdmg)[1]} Keys into Crit Dmg Stat\n"
                          f"- {milestone}{milestone_suffix} Crit Dmg Level\n"
                          f"- {format(milestone_gold, '.2f')}{milestone_gold_suffix} Gold\n"
                          f"- {format(milestone_days, '.2f')} days from Milestone"
                    , inline=False)
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def elixirsheet(em_level: str, elixir_per_rewind: str, all_skills_old: str, all_skills_new: str, invisible: bool, include_boss_slayer: bool):
    timeout = 30
    em_level = em_level.lower()
    elixir_per_rewind = elixir_per_rewind.lower()
    all_skills_old = all_skills_old.lower()
    all_skills_new = all_skills_new.lower()
    start = timer()

    def sn(p, b):
        return int(p * ((2 * (b * 5) + (p - 1) * 5) / 2))

    def newem(em_level_int: int, elixir_rew_int: int):
        p = 1
        em_copy = em_level_int
        while sn(p, em_level_int) < elixir_rew_int and len(str(sn(p, em_level_int))) < len(str(elixir_rew_int)):
            p *= 10

        p //= 10
        p = int(p)
        prev = 0
        num_length = len(str(p))

        while sn(p, em_level_int) <= elixir_rew_int:
            p += 10 ** (num_length - 1)
            if sn(p, em_level_int) == prev:
                break
            prev = sn(p, em_level_int)
            if sn(p, em_level_int) > elixir_rew_int:
                p -= 10 ** (num_length - 1)
                if num_length > 1:
                    num_length -= 1

        p += em_copy
        em_multi = em_level_int / p

        return em_multi, p

    def funni_loop(min_rew: int, skills_int: float, em_level_int: int, elixir_rew_int: int, old_multi: int):
        i = 0
        min_skill = 0
        timeout_start = timer()

        while True:
            em_multi, p = newem(em_level_int=em_level_int, elixir_rew_int=elixir_rew_int)
            em_rewinds = i
            skill_rewinds = skills_int / elixir_rew_int

            if min_rew > skill_rewinds + em_rewinds:
                min_rew = skill_rewinds + em_rewinds
                min_skill = skill_rewinds
            else:
                min_rew -= 1
                em_rewinds -= 1
                em_level_int *= old_multi
                em_level_int = int(em_level_int)
                elixir_rew_int *= old_multi
                elixir_rew_int = int(elixir_rew_int)
                break

            em_level_int /= em_multi
            em_level_int = int(em_level_int)
            elixir_rew_int /= em_multi
            elixir_rew_int = int(elixir_rew_int)
            old_multi = em_multi

            i += 1

            timeout_end = timer()
            if timeout_end - timeout_start > timeout:
                return 0, 0, 0, 0, 0

        return min_rew, min_skill, em_rewinds, em_level_int, elixir_rew_int

    def nice_output(prim: int, secun: int):
        prim_suffix = ''

        while prim > 1000:
            prim /= 1000
            prim_suffix = levels[levels.index(prim_suffix) + 1]
        nice_em_level = prim

        secun_suffix = ''
        while secun > 1000:
            secun /= 1000
            secun_suffix = levels[levels.index(secun_suffix) + 1]

        nice_secun = secun

        return nice_em_level, prim_suffix, nice_secun, secun_suffix

    print("am inceput timeru fraiere")

    try:
        all_skills_old_suffix = '' if all_skills_old[-1].isdigit() else (all_skills_old[-1:] if all_skills_old[-2].isdigit() else all_skills_old[-2:])
        all_skills_old_int = abs(float(all_skills_old) if all_skills_old[-1].isdigit() else (float(all_skills_old[:-1]) if all_skills_old[-2].isdigit() else abs(float(all_skills_old[:-2]))))
        all_skills_old_int *= (1000 ** (levels.index(all_skills_old_suffix))) * 2

        all_skills_new_suffix = '' if all_skills_new[-1].isdigit() else (all_skills_new[-1:] if all_skills_new[-2].isdigit() else all_skills_new[-2:])
        all_skills_new_int = abs(float(all_skills_new) if all_skills_new[-1].isdigit() else (float(all_skills_new[:-1]) if all_skills_new[-2].isdigit() else abs(float(all_skills_new[:-2]))))
        all_skills_new_int *= ((1000 ** (levels.index(all_skills_new_suffix))) * 2)
        all_skills_new_int -= 2

        skills_int = ((((all_skills_new_int + 2) / 2 - all_skills_old_int / 2) / 2) * (all_skills_old_int + all_skills_new_int)) * 5
        skills_int2 = ((((all_skills_new_int + 2) / 2 - all_skills_old_int / 2) / 2) * (all_skills_old_int + all_skills_new_int)) * 6

        em_level_suffix = '' if em_level[-1].isdigit() else (em_level[-1:] if em_level[-2].isdigit() else em_level[-2:])
        original_em_suffix = em_level_suffix
        em_level_int = abs(float(em_level) if em_level[-1].isdigit() else (float(em_level[:-1]) if em_level[-2].isdigit() else abs(float(em_level[:-2]))))
        original_em_level = em_level_int
        em_level_int *= 1000 ** (levels.index(em_level_suffix))
        original_em_multi = em_level_int

        elixir_rew_suffix = '' if elixir_per_rewind[-1].isdigit() else (elixir_per_rewind[-1:] if elixir_per_rewind[-2].isdigit() else elixir_per_rewind[-2:])
        original_rewind_suffix = elixir_rew_suffix
        elixir_rew_int = abs(float(elixir_per_rewind) if elixir_per_rewind[-1].isdigit() else (float(elixir_per_rewind[:-1]) if elixir_per_rewind[-2].isdigit() else abs(float(elixir_per_rewind[:-2]))))
        original_rewind_level = elixir_rew_int
        elixir_rew_int *= 1000 ** (levels.index(elixir_rew_suffix))

        em_level_int = int(em_level_int)
        elixir_rew_int = int(elixir_rew_int)
    except ValueError:
        return 0

    if elixir_rew_int == 0.0 or em_level_int == 0.0 or all_skills_new_int == 0.0 or all_skills_old_int == 0.0:
        print('UNDE ESTE ANDY?')
        return 0

    print("intru in loop fraiere")

    p = 1
    old_multi = 1

    all_skills_old_int = abs(float(all_skills_old) if all_skills_old[-1].isdigit() else (float(all_skills_old[:-1]) if all_skills_old[-2].isdigit() else abs(float(all_skills_old[:-2]))))
    all_skills_new_int = abs(float(all_skills_new) if all_skills_new[-1].isdigit() else (float(all_skills_new[:-1]) if all_skills_new[-2].isdigit() else abs(float(all_skills_new[:-2]))))
    print("merge?")
    while original_rewind_level >= 1000:
        original_rewind_level /= 1000
        original_rewind_suffix = levels[levels.index(original_rewind_suffix) + 1]

    while original_rewind_level < 1:
        original_rewind_level *= 1000
        original_rewind_suffix = levels[levels.index(original_rewind_suffix) - 1]

    while original_em_level >= 1000:
        original_em_level /= 1000
        original_em_suffix = levels[levels.index(original_em_suffix) + 1]

    while original_em_level < 1:
        original_em_level *= 1000
        original_em_suffix = levels[levels.index(original_em_suffix) - 1]

    while all_skills_old_int < 1:
        all_skills_old_int *= 1000
        all_skills_old_suffix = levels[levels.index(all_skills_old_suffix) - 1]

    while all_skills_new_int < 1:
        all_skills_new_int *= 1000
        all_skills_new_suffix = levels[levels.index(all_skills_new_suffix) - 1]

    while all_skills_old_int >= 1000:
        all_skills_old_int /= 1000
        all_skills_old_suffix = levels[levels.index(all_skills_old_suffix) + 1]

    while all_skills_new_int >= 1000:
        all_skills_new_int /= 1000
        all_skills_new_suffix = levels[levels.index(all_skills_new_suffix) + 1]

    if levels.index(all_skills_old_suffix) > levels.index(all_skills_new_suffix):
        print("TALPA N PIEPT MERITI")
        return 0
    elif levels.index(all_skills_old_suffix) == levels.index(all_skills_new_suffix):
        if all_skills_old_int > all_skills_new_int:
            print("TALPA N PIEPT MERITI")
            return 0

    # skill_days = 2 * log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    #                      / all_skills_old_int * (milestone ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    #                                                                                                          levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11

    # skill_days += log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    #                   / all_skills_old_int * (3 ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    #                                                                                               levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11

    # skill_days += 4 * log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    #                       / all_skills_old_int * (2 ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    #                                                                                                   levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11
    # print(skill_days)
    print("haha loop1")
    min_rew, min_skill, em_rewinds, em_level_int, elixir_rew_int = funni_loop(10 ** 200, skills_int, em_level_int, elixir_rew_int,
                                                                              old_multi=old_multi)
    if min_skill > 10 ** 12:
        print("FABRICA DE BELELE")
        return 0

    if elixir_rew_int == 0:
        print("PETRECEREA I GATA MA")
        return 0
    print("haha loop1 ok")

    nice_em_level, em_level_suffix, nice_rewind_level, elixir_rew_suffix = nice_output(em_level_int, elixir_rew_int)

    print("haha loop2")
    if include_boss_slayer:
        min_rew2, min_skill2, em_rewinds2, em_level_int2, elixir_rew_int2 = funni_loop(10 ** 200, skills_int2, em_level_int,
                                                                                       elixir_rew_int, old_multi=1)
    else:
        min_rew2, min_skill2, em_rewinds2, em_level_int2, elixir_rew_int2 = funni_loop(10 ** 200, skills_int, em_level_int,
                                                                                       elixir_rew_int, old_multi=1)
    print("haha loop2 ok")
    nice_em_level2, em_level_suffix2, nice_rewind_level2, elixir_rew_suffix2 = nice_output(em_level_int2, elixir_rew_int2)

    print("???")

    print(f"min rewinds {min_rew} ({min_rew2 + em_rewinds}): em {em_rewinds} ({em_rewinds2 + em_rewinds}) "
          f"skill {min_skill} ({min_skill2}) em {format(nice_em_level, '.2f')}{em_level_suffix} "
          f"({format(nice_em_level2, '.2f')}{em_level_suffix2}) "
          f"elixir {format(nice_rewind_level, '.2f')}{elixir_rew_suffix} ({format(nice_rewind_level2, '.2f')}{elixir_rew_suffix2})")

    # print(f"Minimum rewinds required for {format(all_skills_old_int, '.2f')}{all_skills_old_suffix} - "
    #       f"{format(all_skills_new_int, '.2f')}{all_skills_new_suffix} skills (+{round(skill_days)} days)\n"
    #       f"----------------------------------\n"
    #       f"{format(original_em_level, '.2f')}{original_em_suffix} -> {format(nice_em_level, '.2f')}{em_level_suffix} ({format(nice_em_level2, '.2f')}{em_level_suffix2}) EM \n"
    #       f"{format(original_rewind_level, '.2f')}{original_rewind_suffix} -> {format(nice_rewind_level, '.2f')}{elixir_rew_suffix} "
    #       f"({format(nice_rewind_level2, '.2f')}{elixir_rew_suffix2}) Elixir\nx{nice_rewind_level / original_rewind_level} "
    #       f"(x{format(em_level_int2 / original_em_multi, '.2f')}) increase----------------------------------\n"
    #       f'{em_rewinds} ({em_rewinds2 + em_rewinds}) EM Rewinds\n'
    #       f'{max(1, round(min_skill))} ({max(1, round(min_skill2))}) Skill Rewinds\n----------------------------------\n'
    #       f'{max(1, round(em_rewinds + min_skill))} ({max(1, round(em_rewinds2 + em_rewinds + min_skill2))}) Total Rewinds')

    end = timer()
    print(f"time elapsed: {end - start} seconds")
    print(skills_int2)

    embed = discord.Embed(title="Optimal Rewind Calculator <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.add_field(name="Do you want to make a quick adjustment? Long tap/copy the command you just used!",
                    value=f'/calc optimal_rewind em_level: {em_level} elixir_per_rewind: {elixir_per_rewind} '
                          f'all_skills_old: {all_skills_old} all_skills_new: {all_skills_new} '
                          f'include_boss_slayer: {include_boss_slayer} invisible: {invisible}', inline=False)

    embed.add_field(
        name=f"Minimum rewinds required for {format(all_skills_old_int, '.2f')}{all_skills_old_suffix} - "
             f"{format(all_skills_new_int, '.2f')}{all_skills_new_suffix} "
             f"skills",
        value=f"----------------------------------\n"
              f"{format(original_em_level, '.2f')}{original_em_suffix} -> {format(nice_em_level2, '.2f')}{em_level_suffix2} EM \n"
              f"{format(original_rewind_level, '.2f')}{original_rewind_suffix} -> {format(nice_rewind_level2, '.2f')}{elixir_rew_suffix2} "
              f"Elixir\nx{format(em_level_int2 / original_em_multi, '.2f')} increase"
              f"\n----------------------------------\n"
              f'{em_rewinds2 + em_rewinds} EM Rewinds\n'
              f'{max(1, round(min_skill2))} Skill Rewinds\n----------------------------------\n'
              f'{max(1, round(em_rewinds2 + em_rewinds + min_skill2))} Total Rewinds', inline=False)
    embed.add_field(name='', value='*These calculations are using data from [Tom\'s Optimal Rewind Sheet]'
                                   '(https://docs.google.com/spreadsheets/d/1nN_oc4Pk4kFLbBDiL6gqwEpQJ5f4SrGaWAQpg-_WP5I/edit?usp=sharing)*')
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def best_spot(daya: int, day_range: int, express: bool, tj: bool, mode: int, titor: float, double_rewind: bool):
    kek = daya
    spots = []
    alta_matrice_babana = []
    start = startcopy = spot_range(daya, tj, express, 2, double_rewind)
    spots.append(start)

    while start - startcopy < day_range:
        start = spot_range(start + 1, tj, express, 2, double_rewind)
        spots.append(start)

    with open("ceva.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        lista_csv = list(csv_reader)

        for day in spots:
            lista = spot_score(day=day, titor=titor, express=express, tj=tj, double_rewind=double_rewind, mode=mode)
            alta_matrice_babana.append(lista)

    def minim():
        index_fishy = 1000000
        minim_dodo = 0
        day_minim = 0
        minim_fishy = 1000000
        skip = 0
        for i in range(0, len(alta_matrice_babana)):
            if minim_fishy > alta_matrice_babana[i][1]:
                minim_fishy = alta_matrice_babana[i][1]
                index_fishy = i
                minim_dodo = alta_matrice_babana[i][3]
                day_minim = alta_matrice_babana[i][0]
                skip = alta_matrice_babana[i][4]

        return index_fishy, minim_fishy, minim_dodo, day_minim, skip

    print(alta_matrice_babana)
    index_fishy1, minim_fishy, minim_dodo, day_minim, skip = minim()
    alta_matrice_babana[index_fishy1][1] = 1000000
    index_fishy2, minim_fishy2, minimdodo2, day2, skip2 = minim()
    alta_matrice_babana[index_fishy2][1] = 1000000
    index_fishy3, minim_fishy3, minimdodo3, day3, skip3 = minim()

    embed = discord.Embed(title="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    if mode == 1:
        embed.add_field(name='', value=f"**At Day {kek}, __Day {spot_range(day_minim, tj, express, 1, double_rewind)}__ ({skip} Days last portal) has the best rewind score of __{format(minim_fishy, '.2f')}__ "
                                       f"({round(minim_dodo)}) for the next "
                                       f"{day_range} days.\n\nThe next best 2 spots are __{spot_range(day2, tj, express, 1, double_rewind)}__ ({skip2} Days last portal) with a score of __{format(minim_fishy2, '.2f')}__"
                                       f" ({round(minimdodo2)}) and __{spot_range(day3, tj, express, 1, double_rewind)}__ ({skip3} Days last portal) with a score of __{format(minim_fishy3, '.2f')}__ ({round(minimdodo3)}). "
                                       f"The score inside brackets represents [Dodora's Rewind Sheet](https://bit.ly/Dodo_Rewind_Sheet) Cost.**", inline=False)
    else:
        embed.add_field(name='', value=f"**At Day {kek}, __Day {spot_range(day_minim, tj, express, 1, double_rewind)}__ ({skip} Days last portal) has the best rewind time of __{secunda(int(minim_fishy))}__ for the next "
                                       f"{day_range} days.\n\nThe next best 2 spots are __{spot_range(day2, tj, express, 1, double_rewind)}__ ({skip2} Days last portal) with a time of __{secunda(int(minim_fishy2))}__"
                                       f" and __{spot_range(day3, tj, express, 1, double_rewind)}__ ({skip3} Days last portal) with a time of __{secunda(int(minim_fishy3))}__.**\n\n***__Note: These times are approximations"
                                       f" and may not be 100% accurate.__***", inline=False)

    embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                   "(https://bit.ly/Fishy_Rewind_Sheet). If you want to use No TJ/No Express/Titor/Double rewind options, look at the optional parameters.*")
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def detailed_spot(daya: int, express: bool, tj: bool, double_rewind: bool, titor: float):
    with open("ceva.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        lista_csv = list(csv_reader)
        embed = discord.Embed(title="PORTAL --- DAY --- MOB --- BOSS\n--------------------------------", color=0x71368a)
        embed.add_field(name="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>\n------------------------"
                             "------------", value='', inline=False)
        score_fishy_list = spot_score(day=daya, titor=titor, express=express, tj=tj, double_rewind=double_rewind, mode=1)
        score_fishy = score_fishy_list[1]
        score_dodo = score_fishy_list[3]
        if daya > 1000:
            score_seconds = secunda(spot_score(day=daya, titor=titor, express=express, tj=tj, double_rewind=double_rewind, mode=2)[1])
            embed.add_field(name=f"This spot has a score of {score_fishy} ({score_dodo}) or {score_seconds} minutes, with a {score_fishy_list[4]} Day last portal.", value='', inline=False)
        else:
            embed.add_field(name=f"This spot has a score of {score_fishy} ({score_dodo}), with a {score_fishy_list[4]} Day last portal.", value='', inline=False)
        if express:
            portal = 10 if daya // 500 == 0 else (daya // 500) * 10
        else:
            portal = 5 if daya // 500 == 0 else (daya // 500) * 5
        portal_count = 1
        initial = daya
        if tj:
            if double_rewind:
                daya = int(spot_round(spot_round(daya * 0.75) * 0.75))
            else:
                daya = int(spot_round(daya * 0.75))
        else:
            if double_rewind:
                daya = int(spot_round(spot_round(daya * 0.5) * 0.5))
            else:
                daya = int(spot_round(daya * 0.5))
        i = 0
        if daya % 5 != 0:
            return 0
        ceva = "```\n"
        while daya < initial:
            if i < 9:
                ceva += f"{portal_count}:  " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                                  f"{boss[daya % 100 // 5].title()}\n"
            else:
                ceva += f"{portal_count}: " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                                 f"{boss[daya % 100 // 5].title()}\n"
            if i % 14 == 0 and i >= 14:
                ceva += "\n```"
                embed.add_field(name='', value=ceva, inline=False)
                ceva = "```\n"
                ceva += f"{portal_count}: " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                                 f"{boss[daya % 100 // 5].title()}\n"
            daya += portal
            portal_count += 1
            i += 1

    ceva += "\n```"
    embed.add_field(name='', value=ceva, inline=False)
    embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                   "(https://bit.ly/Fishy_Rewind_Sheet). The scores inside brackets represent [Dodora's Rewind Sheet]" \
                                   f"(https://bit.ly/Dodo_Rewind_Sheet) Costs. If you want to use No TJ/No Express/Titor/Double Rewind options, look at the optional parameters.*")
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
    return embed


def spots(daya: int, day_range: int, tj: bool, express: bool, mode: int, titor: float, double_rewind: bool):
    kek = daya
    spots = []
    matrice = []
    lista = []
    skip = 0
    start = startcopy = spot_range(daya, tj, express, 2, double_rewind)
    spots.append(start)

    while start - startcopy < day_range:
        start = spot_range(start + 1, tj, express, 2, double_rewind)
        spots.append(start)

    minim_fishy, minim_dodo = 100000000, 100000000
    day_minim = 0
    if mode == 1:
        embed = discord.Embed(title="DAY --- SCORE --- LAST BOSS --- LAST PORTAL SKIP\n--------------------------------", color=0x71368a)
    else:
        embed = discord.Embed(title="DAY --- TIME --- LAST BOSS --- LAST PORTAL SKIP\n--------------------------------", color=0x71368a)
    embed.add_field(name="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>\n------------------------"
                         "------------", value='', inline=False)
    for day in spots:
        lista = spot_score(day=day, titor=titor, express=express, tj=tj, double_rewind=double_rewind, mode=mode)
        initial = lista[0]
        score = lista[1]
        dodo_score = round(lista[3])
        if minim_fishy > score:
            day_minim = initial
            minim_fishy = score
            minim_dodo = dodo_score
            skip = lista[4]
        matrice.append(lista)

    print(matrice)
    if mode == 1:
        value = f"**At Day {kek}, __Day {spot_range(day_minim, tj, express, 1, double_rewind)}__ has the best rewind score of {format(minim_fishy, '.2f')} " \
                f"({round(minim_dodo)}) with a {skip} Day last portal skip for the next " \
                f"{day_range} days. The scores inside brackets represent [Dodora's Rewind Sheet]" \
                f"(https://bit.ly/Dodo_Rewind_Sheet) Costs.**"
    else:
        value = f"**At Day {kek}, __Day {spot_range(day_minim, tj, express, 1, double_rewind)}__ has the best time of __{secunda(int(minim_fishy))}__ with a " \
                f"{skip} day last portal skip for the next " \
                f"{day_range} days.**"
    embed.add_field(name='', value=value, inline=False)
    ceva = '```\n'
    counter = 0
    min_fishy = 1000000000
    min_dodo = 0
    min_day = 0
    prev = 0
    for lista in matrice:
        spots = spot_range(lista[0], tj, express, 1, double_rewind)
        if prev == spots:
            pass
        else:
            if counter < 10:
                if mode == 1:
                    ceva += f"{spot_range(lista[0], tj, express, 1, double_rewind)}" + " - " + f"{format(lista[1], '.2f')}" + f" ({lista[3]})" + " - " + f"{lista[2]} ({lista[4]} skip)\n"
                else:
                    ceva += f"{spot_range(lista[0], tj, express, 1, double_rewind)}" + " - " + f"{secunda(int(lista[1]))}" + " - " + f"{lista[2]} ({lista[4]} skip)\n"
                counter += 1
                if min_fishy > lista[1]:
                    min_day = lista[0]
                    min_fishy = lista[1]
                    min_dodo = lista[3]
            elif counter == 10:
                ceva += "\n```"
                counter = 0
                if mode == 1:
                    embed.add_field(name='-------------------------------------------\n'
                                         f"The best spot within this range is {spot_range(min_day, tj, express, 1, double_rewind)} with a {format(min_fishy, '.2f')} ({min_dodo}) score", value=ceva, inline=False)
                else:
                    embed.add_field(name='-------------------------------------------\n'
                                         f"The best spot within this range is {spot_range(min_day, tj, express, 1, double_rewind)} with a {secunda(int(min_fishy))} time", value=ceva, inline=False)
                ceva = '```\n'
                min_fishy = 1000000000
                if min_fishy > lista[1]:
                    min_day = lista[0]
                    min_fishy = lista[1]
                    min_dodo = lista[3]
                if mode == 1:
                    ceva += f"{spot_range(lista[0], tj, express, 1, double_rewind)}" + " - " + f"{format(lista[1], '.2f')}" + f" ({lista[3]})" + " - " + f"{lista[2]} ({lista[4]} skip)\n"
                else:
                    ceva += f"{spot_range(lista[0], tj, express, 1, double_rewind)}" + " - " + f"{secunda(int(lista[1]))}" + " - " + f"{lista[2]} ({lista[4]} skip)\n"
        prev = spots

    ceva += "\n```"
    if min_fishy > lista[1]:
        min_day = lista[0]
        min_fishy = lista[1]
        min_dodo = lista[3]

    if mode == 1:
        embed.add_field(name='-------------------------------------------\n'
                             f"The best spot within this range is {spot_range(min_day, tj, express, 1, double_rewind)} with a {format(min_fishy, '.2f')} ({min_dodo}) score",
                        value=ceva, inline=False)
        embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                       "(https://bit.ly/Fishy_Rewind_Sheet). If you want to use No TJ/No Express/Titor/Double Rewind options, look at the optional parameters.*")
    else:
        embed.add_field(name='-------------------------------------------\n'
                             f"The best spot within this range is {spot_range(min_day, tj, express, 1, double_rewind)} with a {secunda(int(min_fishy))} time",
                        value=ceva, inline=False)
        embed.add_field(name='', value="***__Note: These times are approximations and may not be 100% accurate.__***\n*These calculations are using data from [Fishy's Rewind Sheet]"
                                       "(https://bit.ly/Fishy_Rewind_Sheet). If you want to use No TJ/No Express/Titor/Double Rewind options, look at the optional parameters.*")
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def daytodamage(day: int):
    if 2000 <= day < 73919:
        index = matrice_babana[day // 1000] if day <= 37000 else None
        if index is None:
            day1 = 37000
            damage = 18
            litere = "mw"
        else:
            day1 = index[0]
            damage = index[1]
            litere = index[2]
        while day1 < day:
            day1 += 1
            damage *= 1.06599999998486
            if damage > 1000:
                if litere[1] != "z":
                    new_letters = letters[letters.index((litere[1])) + 1]
                    litere = litere[0] + new_letters
                elif litere == "zz":
                    return 0, 0
                else:
                    litere = letters[letters.index((litere[0])) + 1] + "a"
                damage /= 1000

        embed = discord.Embed(title="Day to Damage Calculator <a:kafkakurukuru:1118233531110412461>",
                              color=0x71368a)
        embed.add_field(name="",
                        value=f"The approximate one-shot damage required for **Day {day1}** is **{round(damage)}{litere}**! "
                              f"*(+/- 10 days).*",
                        inline=False)

        easy, easyseconds = exped_secunda(exped_time(damage, litere, day1, 160, 'k', 1.012874309))
        normal, normalseconds = exped_secunda(exped_time(damage, litere, day1, 8, 'm', 1.032497215))
        hard, hardseconds = exped_secunda(exped_time(damage, litere, day1, 1, 'b', 1.088930093))
        hell, hellseconds = exped_secunda(exped_time(damage, litere, day1, 20, 'ae', 1.239747763))
        nm, nmseconds = exped_secunda(int(((day1 - 1) / 10) * 3 - 201))

        times = f"```Easy   {easy}    Fates MS: {next_fates_milestone(easyseconds, 'easy')}\n" \
                f"Normal {normal}    Fates MS: {next_fates_milestone(normalseconds, 'normal')}\n" \
                f"Hard   {hard}    Fates MS: {next_fates_milestone(hardseconds, 'hard')}\n" \
                f"Hell   {hell}    Fates MS: {next_fates_milestone(hellseconds, 'hell')}\n" \
                f"NM     {nm}```"

        embed.add_field(name=f'Approximate Expedition Times for Day {day1}', value=times, inline=False)

        embed.add_field(name="", value=f"*These calculations are using data from [IINII's Pushing Sheet]"
                                       "(https://docs.google.com/spreadsheets/d/1-vl0Kwa9R1Bl36WHjihjItFfNVKi8LGRSEkqHy9tLuA/edit?usp=sharing)*",
                        inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

        return embed
    else:
        return 0


def damagetoday(damage: str, suffix: str, test_mode: bool):
    day_damage = 0
    day = 0
    litera_max = ''

    try:
        damage = float(damage)
    except ValueError:
        print("valoare eroare")
        return 0
    if len(suffix) != 2:
        print("len")
        return 0

    ok = False
    if levels.index(suffix) > levels.index("mz"):
        day = 37000
        day_damage = 18
        litera_max = "mw"

    elif len(suffix) == 2 and damage <= 1000:
        litera_max = ''
        for i in range(2, (len(matrice_babana) - 2)):
            if matrice_babana[i][2] == suffix:
                if damage < 9 and suffix == "ak":
                    print("2k")
                    return 0
                elif damage < matrice_babana[i][1]:
                    day = matrice_babana[i - 1][0]
                    day_damage = matrice_babana[i - 1][1]
                    litera_max = matrice_babana[i - 1][2]
                    ok = True
                    break
        if ok is False:
            for i in range(2, (len(matrice_babana) - 2)):
                if matrice_babana[i][2][0] == suffix[0]:
                    if letters.index(matrice_babana[i][2][1]) <= letters.index(suffix[1]) < \
                            letters.index(matrice_babana[i + 1][2][1]):
                        day = matrice_babana[i][0]
                        day_damage = matrice_babana[i][1]
                        litera_max = matrice_babana[i][2]
                        break

                    elif letters.index(suffix[1]) < letters.index(matrice_babana[i][2][1]):
                        day = matrice_babana[i - 1][0]
                        day_damage = matrice_babana[i - 1][1]
                        litera_max = matrice_babana[i - 1][2]
                        break

                    elif letters.index(matrice_babana[i + 2][2][0]) - letters.index(matrice_babana[i + 1][2][0]) == 1:
                        day = matrice_babana[i + 1][0]
                        day_damage = matrice_babana[i + 1][1]
                        litera_max = matrice_babana[i + 1][2]
                        break

                    elif letters.index(matrice_babana[i + 1][2][1]) < letters.index(suffix[1]) < \
                            letters.index(matrice_babana[i + 2][2][1]):
                        day = matrice_babana[i + 1][0]
                        day_damage = matrice_babana[i + 1][1]
                        litera_max = matrice_babana[i + 1][2]
                        break

                    elif letters.index(matrice_babana[i][2][1]) < letters.index(matrice_babana[i + 1][2][1]) < \
                            letters.index(suffix[1]):
                        day = matrice_babana[i + 2][0]
                        day_damage = matrice_babana[i + 2][1]
                        litera_max = matrice_babana[i + 2][2]
                        break

                    else:
                        day = matrice_babana[i - 1][0]
                        day_damage = matrice_babana[i - 1][1]
                        litera_max = matrice_babana[i - 1][2]

    if test_mode:
        if levels.index(suffix) < levels.index("ak"):
            if damage < 9:
                return 0
    print(litera_max, suffix, day, day_damage)
    try:
        while litera_max != suffix:
            day += 1
            day_damage *= 1.06599999998486
            if day_damage > 1000:
                if litera_max[1] != "z":
                    new_letters = letters[letters.index((litera_max[1])) + 1]
                    litera_max = litera_max[0] + new_letters
                elif litera_max == "zz":
                    print('zz fraiere')
                    return 0
                else:
                    litera_max = letters[letters.index((litera_max[0])) + 1] + "a"
                day_damage /= 1000
            if day > 73918:
                print('73k fraiere')
                return 0
    except:
        return 0

    while day_damage <= damage:
        day += 1
        day_damage *= 1.06599999998486

    embed = discord.Embed(title="Damage to Day Calculator <a:kafkakurukuru:1118233531110412461>",
                          color=0x71368a)
    embed.add_field(name="",
                    value=f"**{damage}{suffix.lower()}** damage will approximately put you to **Day {day}** with one-shots! "
                          f"*(+/- 10 days).*",
                    inline=False)

    try:
        easy, easyseconds = exped_secunda(exped_time(day_damage, litera_max, day, 160, 'k', 1.012874309))
        normal, normalseconds = exped_secunda(exped_time(day_damage, litera_max, day, 8, 'm', 1.032497215))
        hard, hardseconds = exped_secunda(exped_time(day_damage, litera_max, day, 1, 'b', 1.088930093))
        hell, hellseconds = exped_secunda(exped_time(day_damage, litera_max, day, 20, 'ae', 1.239747763))
        nm, nmseconds = exped_secunda(int(((day - 1) / 10) * 3 - 201))
    except IndexError:
        return 0

    times = f"```Easy   {easy}    Fates MS: {next_fates_milestone(easyseconds, 'easy')}\n" \
            f"Normal {normal}    Fates MS: {next_fates_milestone(normalseconds, 'normal')}\n" \
            f"Hard   {hard}    Fates MS: {next_fates_milestone(hardseconds, 'hard')}\n" \
            f"Hell   {hell}    Fates MS: {next_fates_milestone(hellseconds, 'hell')}\n" \
            f"NM     {nm}```"

    embed.add_field(name=f'Approximate Expedition Times for Day {day}', value=times, inline=False)

    embed.add_field(name="", value=f"*These calculations are using data from [IINII's Pushing Sheet]"
                                   "(https://docs.google.com/spreadsheets/d/1-vl0Kwa9R1Bl36WHjihjItFfNVKi8LGRSEkqHy9tLuA/edit?usp=sharing)*",
                    inline=False)
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def weapondamage(old_day: int, new_day: int):
    if new_day > old_day > 0 and new_day > 0:
        a = round(((new_day - old_day) / 78.3) * 11)
        return a
    else:
        return 0


class Formulas(commands.GroupCog, name="calc"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="weapondamage", description="Input the old & new day of your weapon to find out how many "
                                                           "days you gain")
    @app_commands.describe(old_day="Old Day/Level of your weapon")
    @app_commands.describe(new_day="New Day/Level of your weapon")
    @app_commands.user_install()
    @app_commands.allowed_installs(guilds=False, users=True)
    async def weapondamage_f(self, interaction: discord.Interaction, old_day: int, new_day: int, invisible: bool = True) -> None:
        print(f"Trying Weapon Damage with the following data: Old Day: {old_day} New Day: {new_day}")
        rezultat = weapondamage(old_day, new_day)
        embed = discord.Embed(title="Weapon Damage Calculator <a:kafkakurukuru:1118233531110412461>",
                              color=0x71368a)
        embed.add_field(name="",
                        value=f"A **{new_day - old_day}** Day increase on your weapon is worth **{rezultat}** Days!",
                        inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        if rezultat == 0:
            await interaction.response.send_message(f"Invalid data, please try again. Example: a level 10000 weapon "
                                                    f"compared to a level 11000 weapon is worth 140 days.", ephemeral=True)
        else:
            if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            elif invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Weapon Damage")

    @app_commands.command(name="daytodamage", description="Input a Day to receive the estimate one-shot damage "
                                                          "required to beat it")
    @app_commands.describe(day="Day you want to receive the approximate damage for")
    async def daytodamage_f(self, interaction: discord.Interaction, day: int, invisible: bool = True) -> None:
        print(f"Trying Damage to Day with the following data: Day: {day}")
        if day < 2000 or day > 73918:
            await interaction.response.defer(ephemeral=True)
        elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        embed = daytodamage(day)
        if embed == 0:
            await interaction.followup.send("Day must be between 2000 (9ak damage) and 73918 (999zz damage).")
        else:
            await interaction.followup.send(embed=embed)
        print("Done w/ Damage to Day")

    @app_commands.command(name="damagetoday", description="Input the damage number of your DPS Hero to get an estimate "
                                                          "of your one-shot pushing range")
    @app_commands.describe(damage="Damage number of your Main DPS Hero")
    @app_commands.describe(suffix="Suffix of the damage. Example: 'aa' is the suffix for '1aa' damage")
    async def damagetoday_f(self, interaction: discord.Interaction, damage: str, suffix: str, invisible: bool = True) -> None:
        print(f"Trying Damage to Day with the following data: Damage: {damage} Suffix {suffix}")
        test_value = damagetoday(damage, suffix.lower(), True)
        if test_value == 0:
            await interaction.response.defer(ephemeral=True)
        elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        embed = damagetoday(damage, suffix.lower(), False)
        if embed == 0:
            await interaction.followup.send("Day must be between 2000 (9ak damage) and 73918 (999zz damage).")
        else:
            await interaction.followup.send(embed=embed)
        print("Done w/ Damage to Day")

    @app_commands.command(name="multiplier", description="Input a damage multiplier to receive a Day equivalent")
    @app_commands.describe(multiplier="Multiplier value of the number you want to calculate. Example: A x50 multiplier is worth 62 days")
    async def multiplier(self, interaction: discord.Interaction, multiplier: int, invisible: bool = True) -> None:
        print(f"Trying Multiplier with the following data: Multiplier: {multiplier}")
        if multiplier < 0:
            await interaction.response.send_message("Invalid data, please try again. Example: a x50 damage increase is "
                                                    "equivalent to 62 days.", ephemeral=True)
        else:

            embed = discord.Embed(title="Multiplier to Day Calculator <a:kafkakurukuru:1118233531110412461>",
                                  color=0x71368a)
            embed.add_field(name='', value=f"A **x{multiplier}** Damage multiplier is worth **{round(math.log(multiplier, 2) * 11)}** Days! *This is also equal to "
                                           f"**{round(math.log(multiplier * multiplier, 2) * 11)}** Days for Crit Damage.*", inline=False)
            embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            elif invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Multiplier")

    @app_commands.command(name="rewindspots", description="Input a day & the days to look ahead to receive the Rewind "
                                                          "Scores for the said spots. Max 500.")
    @app_commands.describe(starting_day="Starting day for which you want to calculate spots for")
    @app_commands.describe(days_to_look_ahead="Days you want to look ahead the starting day, for all spots within that range")
    @app_commands.choices(mode=[
        discord.app_commands.Choice(name='Rewind scores', value=1),
        discord.app_commands.Choice(name='Seconds approximation (+/- 10s)', value=2)],
        titor=[
            discord.app_commands.Choice(name='No Titor', value=1.0),
            discord.app_commands.Choice(name='4*', value=1.08),
            discord.app_commands.Choice(name='7*', value=1.1),
            discord.app_commands.Choice(name='10*', value=1.14),
            discord.app_commands.Choice(name='13*', value=1.16),
            discord.app_commands.Choice(name='15*', value=1.2)],
    )
    async def spots_f(self, interaction: discord.Interaction, starting_day: int, days_to_look_ahead: int, mode: discord.app_commands.Choice[int],
                      titor: discord.app_commands.Choice[float] = 1.0, invisible: bool = True, tj: bool = True, express: bool = True, double_rewind: bool = False) -> None:
        print(f"Trying 'Rewind Spots' with the following data: Starting Day: {starting_day}, Days to look ahead: {days_to_look_ahead} titel {titor} double {double_rewind}")
        try:
            titor = titor.value
        except:
            titor = 1.0
        if 50 <= days_to_look_ahead <= 500 and (starting_day + days_to_look_ahead) <= max_day and starting_day >= 50:
            if double_rewind is True and starting_day < 10585:
                await interaction.response.send_message('Day 10585+ required to use the Doubles option', ephemeral=True)
                return
            else:
                embed = spots(starting_day, days_to_look_ahead, tj=tj, express=express, mode=mode.value, titor=titor, double_rewind=double_rewind)
                if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                    await interaction.response.send_message(embed=embed)
                elif invisible is True:
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(
                "Invalid data, please try again.\n- Max 500 spots a time.\n- Currently, "
                f"the mob data goes up to Day {max_day}.\n- Days to look ahead must "
                "be greater than 50.\n- Starting day must be above 50.\nSecond approximations not available below Day 1000."
                , ephemeral=True)
        print("Done w/ Rewind Spots")

    @app_commands.command(name="detailed_rewindspot", description="Input a day to receive detailed info on the spot ("
                                                                  "each Mob and Boss for each portal)")
    @app_commands.describe(day="Day of the Rewind spot you want the details for")
    @app_commands.choices(titor=[
        discord.app_commands.Choice(name='No Titor', value=1.0),
        discord.app_commands.Choice(name='4*', value=1.08),
        discord.app_commands.Choice(name='7*', value=1.1),
        discord.app_commands.Choice(name='10*', value=1.14),
        discord.app_commands.Choice(name='13*', value=1.16),
        discord.app_commands.Choice(name='15*', value=1.2)],
    )
    async def detailed_spots_f(self, interaction: discord.Interaction, day: int, invisible: bool = True, tj: bool = True, express: bool = True,
                               double_rewind: bool = False, titor: discord.app_commands.Choice[float] = 1.0) -> None:
        print(f"Trying 'Detailed Spot' with the following data: Day: {day} titel {titor} double {double_rewind} tj {tj} express {express}")
        try:
            titor = titor.value
        except:
            titor = 1.0

        if double_rewind is True and day < 10585:
            await interaction.response.send_message('Day 10585+ required to use the Doubles option', ephemeral=True)
            return
        else:
            # if day <= max_day:
                embed = detailed_spot(day, express=express, tj=tj, double_rewind=double_rewind, titor=titor)
            # else:
            #     embed = 0
        if embed == 0:
            await interaction.response.send_message("Invalid spot/data, please try again.", ephemeral=True)
        else:
            if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            elif invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Detailed Spot")

    @app_commands.command(name="best_rewindspot", description="Input a day & the days to look ahead to receive the day with the "
                                                              "best Rewind Score")
    @app_commands.describe(starting_day="Starting day for which you want to calculate spots for")
    @app_commands.describe(days_to_look_ahead="Days you want to look ahead the starting day, for the best spots within that range")
    @app_commands.choices(mode=[
        discord.app_commands.Choice(name='Rewind scores', value=1),
        discord.app_commands.Choice(name='Seconds approximation (+/- 10s)', value=2)],
        titor=[
            discord.app_commands.Choice(name='No Titor', value=1.0),
            discord.app_commands.Choice(name='4*', value=1.08),
            discord.app_commands.Choice(name='7*', value=1.1),
            discord.app_commands.Choice(name='10*', value=1.14),
            discord.app_commands.Choice(name='13*', value=1.16),
            discord.app_commands.Choice(name='15*', value=1.2)],
    )
    async def best_spots_f(self, interaction: discord.Interaction, starting_day: int, days_to_look_ahead: int, mode: discord.app_commands.Choice[int],
                           titor: discord.app_commands.Choice[float] = 1.0, invisible: bool = True,
                           tj: bool = True, express: bool = True, double_rewind: bool = False) -> None:
        print(f"Trying 'Best Spots' with the following data: Starting Day: {starting_day}, Days to look ahead: {days_to_look_ahead} titel {titor}")
        if 100 <= days_to_look_ahead <= 500 and (starting_day + days_to_look_ahead) <= max_day and starting_day >= 50:
            try:
                titor = titor.value
            except:
                titor = 1.0
            if double_rewind is True and starting_day < 10585:
                await interaction.response.send_message('Day 10585+ required to use the Doubles option', ephemeral=True)
                return
            else:
                if mode.value == 2 and starting_day < 1000:
                    await interaction.response.send_message(
                        "Invalid data, please try again.\n- Max 500 spots a time.\n- Currently, "
                        f"the mob data goes up to Day {max_day}.\n- Days to look ahead must "
                        "be greater than 50.\n- Starting day must be above 50.\nSecond approximations not available below Day 1000."
                        , ephemeral=True)
                else:
                    embed = best_spot(starting_day, days_to_look_ahead, express=express, tj=tj, mode=mode.value, titor=titor, double_rewind=double_rewind)
                    if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                        await interaction.response.send_message(embed=embed)
                    elif invisible is True:
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Invalid data, please try again.\n- Max 500 spots a time.\n- Currently, "
                                                    f"the mob data goes up to Day {max_day}.\n- Days to look ahead must "
                                                    "be greater than 100.\n- Starting day must be above 50.\nSecond approximations "
                                                    "not available below Day 1000.", ephemeral=True)
        print("Done w/ Best Spots")

    @app_commands.command(name="optimal_rewind",
                          description="Input your elixir data to receive the minimum amount of rewinds for your goal")
    @app_commands.describe(em_level="Level of your Elixir Mastery skill. Example: '15ag'")
    @app_commands.describe(elixir_per_rewind="Elixir per Max Day rewind. Example: '100aq'")
    @app_commands.describe(all_skills_old="Level of your current skills/starting point for the calculations (BS included). Example: '10M'")
    @app_commands.describe(all_skills_new="Level of the desired skill levels (BS included). Example: '20M'")
    @app_commands.describe(include_boss_slayer="Only change if you don't want BS included in your grind.")
    async def elixirsheet_f(self, interaction: discord.Interaction, em_level: str, elixir_per_rewind: str,
                            all_skills_old: str, all_skills_new: str, include_boss_slayer: bool = True, invisible: bool = True) -> None:
        print(f"Trying Elixir Calc with the following data: em {em_level} elixir {elixir_per_rewind} old {all_skills_old} "
              f"new {all_skills_new} bs {include_boss_slayer}")

        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        print("trandafiri")

        embed = elixirsheet(em_level=em_level, elixir_per_rewind=elixir_per_rewind, all_skills_old=all_skills_old,
                            all_skills_new=all_skills_new, include_boss_slayer=include_boss_slayer, invisible=invisible)
        print(embed)
        if embed != 0:
            print("fat frumos")
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="", color=0x71368a)
            embed.add_field(name=f"Invalid data or 30s have passed, please try again. Long tap/copy the command you just used if you want "
                                 "to make any adjustments!",
                            value=f'/calc optimal_rewind em_level: {em_level} elixir_per_rewind: {elixir_per_rewind} '
                                  f'all_skills_old: {all_skills_old} all_skills_new: {all_skills_new} '
                                  f'include_boss_slayer: {include_boss_slayer} invisible: {invisible}'
                            , inline=False)
            embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.followup.send(embed=embed, ephemeral=True)

        print("Done w/ Elixir calc")

    @app_commands.command(name="dungeon_gold",
                          description="Input your dungeon data to receive the best way to spend your keys")
    @app_commands.describe(crit_dmg_stat_level="Stat Menu -> Crit DMG Stat info button -> Blue number. NOT the percentage value, but the level")
    @app_commands.describe(gold_stat_level="Stat Menu -> Gold Stat info button -> Blue number. NOT the percentage value, but the level")
    @app_commands.describe(gold_from_dungeon_keys="Shop -> Dungeon -> Gold you get from your current keys. Example: '12bm'")
    @app_commands.describe(current_keys="Shop -> Dungeon -> Keys you currently have. Example: '12M'")
    @app_commands.describe(days_you_want_to_progress="The amount of days you'd like to expect from upgrading Crit DMG with Dungeon gold. Example: '70'")
    async def gold_sheet_f(self, interaction: discord.Interaction, crit_dmg_stat_level: str, gold_stat_level: str, gold_from_dungeon_keys: str, current_keys: str, days_you_want_to_progress: int, invisible: bool = True) -> None:
        print(f"Trying Gold Sheet with the following data: cdmg {crit_dmg_stat_level} gold {gold_from_dungeon_keys} keys {current_keys} target {days_you_want_to_progress}"
              f"gold lvl {gold_stat_level}")
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()
        if days_you_want_to_progress > 300:
            embed = 0
        else:
            embed = gold_sheet(cdmg=crit_dmg_stat_level, gold=gold_from_dungeon_keys, gold_level=gold_stat_level, keys=current_keys, target=days_you_want_to_progress, invisible=invisible)
        if embed == 0:
            embed = discord.Embed(title="", color=0x71368a)
            embed.add_field(name=f"Invalid data or days target exceeded 300, please try again. Long tap/copy the command you just used if you want "
                                 "to make any adjustments!",
                            value=f"/calc dungeon_gold crit_dmg_stat_level: {crit_dmg_stat_level} gold_stat_level: {gold_stat_level} gold_from_dungeon_keys: {gold_from_dungeon_keys} "
                                  f"current_keys: {current_keys} days_you_want_to_progress: {days_you_want_to_progress} invisible: {invisible}")
            embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.followup.send(embed=embed)
            elif invisible is True:
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(embed=embed)
        print("Done w/ Gold Sheet")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Formulas(bot))
