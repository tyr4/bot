import discord
from discord import app_commands
from discord.ext import commands
import asyncio

import csv
import math
from math import log, pow
from timeit import default_timer as timer

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
mobs = ["dino", "rex", "shade", "frosk", "blob", "gargoyle", "caps", "warmonger", "banshee"]
mob_scores = [1.93, 1.29, 1.94, 1.00, 1.92, 1.73, 1.92, 1.33, 1.65]

levels = ['', 'k', 'm', 'b', 't',
          'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj',
          'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at',
          'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd',
          'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn',
          'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx',
          'by', 'bz']


def gold_sheet(cdmg: str, gold:str, keys:str, target: float, invisible: bool):
    cdmg = cdmg.lower()
    gold = gold.lower()
    keys = keys.lower()

    stat_milestone, milestone = 0, 0
    milestone_suffix = ''

    def sn(p, b):  # ca sa nu uit, suma primilor p termeni si b e de unde incepe
        return int(p * ((2 * (b * 150 + 150) + ((p - 1) * 150)) / 2))

    def days(multi: float, stat_milestone: int):
        return math.log(multi ** 2, 2) * 11 + stat_milestone

    def nice_output(le_int):
        suffix = ''

        while le_int > 1000:
            le_int /= 1000
            suffix = levels[levels.index(suffix) + 1]
        le_int = le_int

        return le_int, suffix

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
    except ValueError:
        return 0

    key_gold_int = gold_int if keys_int <= 10 else int(gold_int / (keys_int // 10))
    key_copy = key_gold_int
    key_gold_int *= 1 if keys_int <= 10 else keys_int // 10
    gold_int = key_gold_int
    if key_gold_int == 0:
        return 0

    p = 1
    cdmg_copy = cdmg_int

    while (sn(p, cdmg_int)) <= gold_int and len(str(sn(p, cdmg_int))) < len(str(gold_int)):
        p *= 10
    p //= 10

    prev = 0
    num_length = len(str(p))

    while sn(p, cdmg_int) <= gold_int:
        p += 10 ** (num_length - 1)
        if sn(p, cdmg_int) == prev:
            break
        prev = sn(p, cdmg_int)
        if sn(p, cdmg_int) > gold_int:
            p -= 10 ** (num_length - 1)
            if num_length > 1:
                num_length -= 1

    p += cdmg_copy
    cdmg_copy_int, cdmg_copy_suffix = nice_output(cdmg_copy)
    cdmg_int, cdmg_suffix = nice_output(cdmg_int)

    if len(str(int(cdmg_int))) == 1:
        milestone = 10
        milestone_suffix = cdmg_suffix
    elif len(str(int(cdmg_int))) == 2:
        milestone = 100
        milestone_suffix = cdmg_suffix
    elif len(str(int(cdmg_int))) == 3:
        milestone = 1
        milestone_suffix = levels[levels.index(cdmg_suffix) + 1]

    if milestone_suffix == '':
        milestone = 10
        milestone_suffix = "k"

    milestone_gold_int = sn((milestone * (1000 ** (levels.index(milestone_suffix)))) - cdmg_copy, cdmg_copy)
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

    target_gold_int, target_gold_suffix = nice_output(sn((target_start * (1000 ** (levels.index(target_start_suffix))) - cdmg_copy), cdmg_copy))
    target_end, target_end_suffix = nice_output(target_start * (1000 ** (levels.index(target_start_suffix))))
    target_keys, target_keys_suffix = nice_output((sn((target_start * (1000 ** (levels.index(target_start_suffix))) - cdmg_copy), cdmg_copy) / key_copy) * 10)
    target_keys = 10 if target_keys_suffix == '' and target_keys < 10 else target_keys
    current_days = days(p / cdmg_copy, (len(str(int(p))) - len(str(int(cdmg_copy)))) * 22 if len(str(int(p))) >= 5 else 0)
    milestone_days = days((milestone * (1000 ** levels.index(milestone_suffix))) / cdmg_copy, 22)
    overshot = days((target_start * (1000 ** (levels.index(target_start_suffix) - levels.index(cdmg_copy_suffix)))) / cdmg_copy_int, stat_milestone) - target

    if target_keys_suffix in ["k", "m", "b", "t"]:
        target_keys_suffix = target_keys_suffix.upper()
    if target_gold_suffix in ["k", "m", "b", "t"]:
        target_gold_suffix = target_gold_suffix.upper()
    if target_end_suffix in ["k", "m", "b", "t"]:
        target_end_suffix = target_end_suffix.upper()
    if keys_req_suffix in ["k", "m", "b", "t"]:
        keys_req_suffix = keys_req_suffix.upper()
    if milestone_gold_suffix in ["k", "m", "b", "t"]:
        milestone_gold_suffix = milestone_gold_suffix.upper()
    if milestone_suffix in ["k", "m", "b", "t"]:
        milestone_suffix = milestone_suffix.upper()

    print(f"{format(current_days, '.2f')} days din current keys")
    print(f"{format(target_keys, '.2f')}{target_keys_suffix} keys pt target")
    print(f"{format(target_gold_int, '.2f')}{target_gold_suffix} gold pt target")
    print(f"{format(target_end, '.2f')}{target_end_suffix} pt target")
    print(f"{format(keys_req_int, '.2f')}{keys_req_suffix} milestone keys req")
    print(f"{milestone}{milestone_suffix} milestone")
    print(f"{format(milestone_days, '.2f')} days from milestone")
    print(f"{format(milestone_gold, '.2f')}{milestone_gold_suffix} gold pt milestone")
    embed = discord.Embed(title="Dungeon Gold Calculator <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.add_field(name="Do you want to make a quick adjustment? Long tap/copy the command you just used!",
                    value=f"/calc dungeon_gold crit_dmg_stat_level: {cdmg} gold_from_dungeon_keys: {gold} "
                          f"keys: {keys} target_days: {target} invisible: {invisible}", inline=False)
    embed.add_field(name="----------- Target days data -----------",
                    value=f"- {format(target_end, '.2f')}{target_end_suffix} Crit Dmg Level (overshot by {format(overshot, '.2f')} days)\n"
                          f"- {format(target_keys, '.2f')}{target_keys_suffix} Keys\n"
                          f"- {format(target_gold_int, '.2f')}{target_gold_suffix} Gold\n"
                          f"- {format(current_days, '.2f')} Days from current Keys", inline=False)
    embed.add_field(name="----------- Milestone data -----------",
                    value=f"- {milestone}{milestone_suffix} Crit Dmg Level\n"
                          f"- {format(keys_req_int, '.2f')}{keys_req_suffix} Keys\n"
                          f"- {format(milestone_gold, '.2f')}{milestone_gold_suffix} Gold\n"
                          f"- {format(milestone_days, '.2f')} Days", inline=False)
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def elixirsheet(em_level: str, elixir_per_rewind: str, all_skills_old: str, all_skills_new: str, invisible: bool, milestone: int = 2):
    timeout = 60
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

    skill_days = 2 * log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    / all_skills_old_int * (milestone ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11

    skill_days += log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    / all_skills_old_int * (3 ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11

    skill_days += 4 * log((all_skills_new_int * 1000 ** (levels.index(all_skills_new_suffix) - levels.index(all_skills_old_suffix)))
    / all_skills_old_int * (2 ** (round(math.log(all_skills_new_int * (1000 ** (levels.index(all_skills_new_suffix) -
    levels.index(all_skills_old_suffix))), 10)) - math.floor(math.log(all_skills_old_int, 10)))), 2) * 11
    print(skill_days)

    min_rew, min_skill, em_rewinds, em_level_int, elixir_rew_int = funni_loop(10 ** 200, skills_int, em_level_int, elixir_rew_int,
                                                                              old_multi=old_multi)
    if min_skill > 10 ** 12:
        print("FABRICA DE BELELE")
        return 0

    if elixir_rew_int == 0:
        print("PETRECEREA I GATA MA")
        return 0

    nice_em_level, em_level_suffix, nice_rewind_level, elixir_rew_suffix = nice_output(em_level_int, elixir_rew_int)

    min_rew2, min_skill2, em_rewinds2, em_level_int2, elixir_rew_int2 = funni_loop(10 ** 200, skills_int2, em_level_int,
                                                                                   elixir_rew_int, old_multi=1)

    nice_em_level2, em_level_suffix2, nice_rewind_level2, elixir_rew_suffix2 = nice_output(em_level_int2, elixir_rew_int2)

    print(f"min rewinds {min_rew} ({min_rew2 + em_rewinds}): em {em_rewinds} ({em_rewinds2 + em_rewinds}) "
          f"skill {min_skill} ({min_skill2}) em {format(nice_em_level, '.2f')}{em_level_suffix} "
          f"({format(nice_em_level2, '.2f')}{em_level_suffix2}) "
          f"elixir {format(nice_rewind_level, '.2f')}{elixir_rew_suffix} ({format(nice_rewind_level2, '.2f')}{elixir_rew_suffix2})")

    print(f"Minimum rewinds required for {format(all_skills_old_int, '.2f')}{all_skills_old_suffix} - "
                         f"{format(all_skills_new_int, '.2f')}{all_skills_new_suffix} skills (+{round(skill_days)} days)\n"
          f"----------------------------------\n"
          f"{format(original_em_level, '.2f')}{original_em_suffix} -> {format(nice_em_level, '.2f')}{em_level_suffix} ({format(nice_em_level2, '.2f')}{em_level_suffix2}) EM \n"
          f"{format(original_rewind_level, '.2f')}{original_rewind_suffix} -> {format(nice_rewind_level, '.2f')}{elixir_rew_suffix} "
          f"({format(nice_rewind_level2, '.2f')}{elixir_rew_suffix2}) Elixir\nx{nice_rewind_level / original_rewind_level} "
          f"(x{format(em_level_int2 / original_em_multi, '.2f')}) increase----------------------------------\n"
          f'{em_rewinds} ({em_rewinds2 + em_rewinds}) EM Rewinds\n'
          f'{max(1, round(min_skill))} ({max(1, round(min_skill2))}) Skill Rewinds\n----------------------------------\n'
          f'{max(1, round(em_rewinds + min_skill))} ({max(1, round(em_rewinds2 + em_rewinds + min_skill2))}) Total Rewinds')

    end = timer()
    print(f"time elapsed: {end - start} seconds")
    print(skills_int2)

    embed = discord.Embed(title="Optimal Rewind Calculator <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.add_field(name="Do you want to make a quick adjustment? Long tap/copy the command you just used!",
                    value=f'/calc optimal_rewind em_level: {em_level} elixir_per_rewind: {elixir_per_rewind} '
                          f'all_skills_old: {all_skills_old} all_skills_new: {all_skills_new} '
                          f'milestone: {milestone} invisible: {invisible}', inline=False)

    embed.add_field(
        name=f"Minimum rewinds required for {format(all_skills_old_int, '.2f')}{all_skills_old_suffix} - "
        f"{format(all_skills_new_int, '.2f')}{all_skills_new_suffix} "
        f"skills (+{round(skill_days)} days)",
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


def best_spot(daya: int, day_range: int):
    kek = daya
    spots = []
    alta_matrice_babana = []

    for i in range(daya, daya + day_range + 1):
        rez = math.floor(daya // 1.33333333333333333333333)
        if rez % 5 == 0:
            if daya % 100 in [1, 21, 41, 61, 81]:
                pass
            else:
                spots.append(daya)
        daya += 1

    with open("ceva.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        lista_csv = list(csv_reader)

        for day in spots:
            lista = []
            score = 0
            dodo_score = 0
            portal = 10 if day // 500 == 0 else (day // 500) * 10
            portal_count = 1
            initial = day
            day = math.floor(day * 0.75)
            froskScore = mob_scores[3]

            while day < initial:
                mobScore = mob_scores[mobs.index(lista_csv[(day // 5) - 1][1].lower())]
                bossScore = boss_scores[day % 100 // 5]
                speed = -12 * (day / initial) + 13
                score += (froskScore + (mobScore - froskScore) * (1 + (max(day - 10000, 0) / 20000)) + bossScore) / speed
                day += portal
                portal_count += 1

            dodo_score += score * 19.3191489361702
            lista.append(initial)
            lista.append(score)
            lista.append(dodo_score)
            alta_matrice_babana.append(lista)

    def minim():
        index_fishy = 1000
        minim_dodo = 0
        day_minim = 0
        minim_fishy = 1000
        for i in range(len(alta_matrice_babana) - 1):
            if minim_fishy > alta_matrice_babana[i][1]:
                minim_fishy = alta_matrice_babana[i][1]
                index_fishy = i
                minim_dodo = alta_matrice_babana[i][2]
                day_minim = alta_matrice_babana[i][0]

        return index_fishy, minim_fishy, minim_dodo, day_minim

    index_fishy1, minim_fishy, minim_dodo, day_minim = minim()
    alta_matrice_babana[index_fishy1][1] = 1000
    index_fishy2, minim_fishy2, minimdodo2, day2 = minim()
    alta_matrice_babana[index_fishy2][1] = 1000
    index_fishy3, minim_fishy3, minimdodo3, day3 = minim()

    embed = discord.Embed(title="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.add_field(name='', value=f"**At Day {kek}, Day {day_minim} has the best rewind score of {format(minim_fishy, '.2f')} "
                                   f"({round(minim_dodo)}) for the next "
                                   f"{day_range} days.\n\nThe next best 2 spots are {day2} with a score of {format(minim_fishy2, '.2f')}"
                                   f" ({round(minimdodo2)}) and {day3} with a score of {format(minim_fishy3, '.2f')} ({round(minimdodo3)}). "
                                   f"The score inside brackets represents [Dodora's Rewind Sheet](https://bit.ly/Dodo_Rewind_Sheet) Cost.**", inline=False)
    embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                       "(https://bit.ly/Fishy_Rewind_Sheet). Awakened TJ and Express pack are assumed.*")
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def detailed_spot(daya: int):
    if daya % 100 in [0, 1, 7, 14, 20, 21, 27, 34, 40, 41, 47, 54, 60, 61, 67, 74, 80, 81, 87, 94]:
        with open("ceva.csv") as csv_file:
            csv_reader = csv.reader(csv_file)
            lista_csv = list(csv_reader)
            embed = discord.Embed(title="PORTAL --- DAY --- MOB --- BOSS\n--------------------------------", color=0x71368a)
            embed.add_field(name="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>\n------------------------"
                                 "------------", value='', inline=False)
            portal = 10 if daya // 500 == 0 else (daya // 500) * 10
            portal_count = 1
            initial = daya
            daya = math.floor(daya * 0.75)
            i = 0
            ceva = "```\n"
            while daya < initial:
                if i < 13:
                    if i < 9:
                        ceva += f"{portal_count}:  " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                    f"{boss[daya % 100 // 5].title()}\n"
                    else:
                        ceva += f"{portal_count}: " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                                          f"{boss[daya % 100 // 5].title()}\n"
                    i += 1
                elif i == 13:
                    ceva += "\n```"
                    i = 0
                    embed.add_field(name='', value=ceva, inline=False)
                    ceva = "```\n"
                    ceva += f"{portal_count}: " f"{daya} " + f"M. {lista_csv[(daya // 5) - 1][1]}" + f" B. " \
                                                                                    f"{boss[daya % 100 // 5].title()}\n"
                daya += portal
                portal_count += 1

        ceva += "\n```"
        embed.add_field(name='', value=ceva, inline=False)
        embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                       "(https://bit.ly/Fishy_Rewind_Sheet). Awakened TJ and Express pack are assumed.*")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        return embed

    return 0


def spots(daya: int, day_range: int):
    kek = daya
    spots = []
    matrice = []

    for i in range(daya, daya + day_range + 1):
        rez = math.floor(daya // 1.33333333333333333333333)
        if rez % 5 == 0:
            if daya % 100 in [1, 21, 41, 61, 81]:
                pass
            else:
                spots.append(daya)
        daya += 1

    with open("ceva.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        lista_csv = list(csv_reader)
        minim_fishy = 100
        day_minim = 0
        average = 0
        average_num = 0
        embed = discord.Embed(title="DAY -------- SCORE -------- LAST BOSS\n--------------------------------", color=0x71368a)
        embed.add_field(name="Rewind Spot Calculator <a:kafkakurukuru:1118233531110412461>\n------------------------"
                             "------------", value='', inline=False)
        for day in spots:
            lista = []
            score = 0
            dodo_score = 0
            portal = 10 if day // 500 == 0 else (day // 500) * 10
            portal_count = 1
            initial = day
            day = math.floor(day * 0.75)
            froskScore = mob_scores[3]

            while day < initial:
                mobScore = mob_scores[mobs.index(lista_csv[(day // 5) - 1][1].lower())]
                currentDay = day if day - 10000 > 0 else 0
                bossScore = boss_scores[day % 100 // 5]
                speed = -12 * (day / initial) + 13
                score += (froskScore + (mobScore - froskScore) * (1 + (max(day - 10000, 0) / 20000)) + bossScore) / speed
                day += portal
                portal_count += 1

            dodo_score += score * 19.3191489361702
            if minim_fishy > score:
                day_minim = initial
                minim_fishy = score
                minim_dodo = dodo_score

            dodo_score = round(dodo_score)
            average += float(score)
            average_num += 1
            lista.append(initial)
            lista.append(score)
            lista.append(boss[(day - portal) % 100 // 5].title())
            lista.append(dodo_score)
            matrice.append(lista)

            # print(f"{initial}   |    {score}")

    embed.add_field(name='', value=f"**At Day {kek}, Day {day_minim} has the best rewind score of {format(minim_fishy, '.2f')} "
                                   f"({round(minim_dodo)}) for the next "
                                   f"{day_range} days. The scores inside brackets represent [Dodora's Rewind Sheet]"
                                   f"(https://bit.ly/Dodo_Rewind_Sheet) Costs.**", inline=False)
    ceva = '```\n'
    counter = 0
    min_fishy = 1000
    min_dodo = 0
    min_day = 0
    for lista in matrice:
        if counter < 10:
            ceva += f"{str(lista[0])}" + " -- " + f"{format(lista[1], '.2f')}" + f" ({lista[3]})" + " -- " + f"{lista[2]}\n"
            counter += 1
            if min_fishy > lista[1]:
                min_day = lista[0]
                min_fishy = lista[1]
                min_dodo = lista[3]
        elif counter == 10:
            ceva += "\n```"
            counter = 1
            embed.add_field(name='-------------------------------------------\n'
                                 f"The best spot within this range is {min_day} with a {format(min_fishy, '.2f')} ({min_dodo}) score", value=ceva, inline=False)
            ceva = '```\n'
            min_fishy = 1000
            ceva += f"{str(lista[0])}" + " -- " + f"{format(lista[1], '.2f')}" + f" ({lista[3]})" + " -- " + f"{lista[2]}\n"

    ceva += "\n```"
    if min_fishy > lista[1]:
        min_day = lista[0]
        min_fishy = lista[1]
        min_dodo = lista[3]
    embed.add_field(name='-------------------------------------------\n'
                         f"The best spot within this range is {min_day} with a {format(min_fishy, '.2f')} ({min_dodo}) score.",
                    value=ceva, inline=False)
    embed.add_field(name='', value="*These calculations are using data from [Fishy's Rewind Sheet]"
                                       "(https://bit.ly/Fishy_Rewind_Sheet). Awakened TJ and Express pack are assumed.*")
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed


def daytodamage(day: int):
    if 2000 < day <= matrice_babana[-1][0]:
        index = matrice_babana[day // 1000]
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
                else:
                    litere = letters[letters.index((litere[0])) + 1] + "a"
                damage /= 1000
        return damage, litere
    else:
        return 0, 0


def damagetoday(damage: int, suffix: str):
    day_damage = 0
    day = 0
    ok = False
    if len(suffix) == 2 and damage <= 1000:
        litera_max = ''
        for i in range(2, (len(matrice_babana) - 2)):
            if matrice_babana[i][2] == suffix:
                if damage < 9 and suffix == "ak":
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

        while litera_max != suffix:
            day += 1
            day_damage *= 1.06599999998486
            if day_damage > 1000:
                if litera_max[1] != "z":
                    new_letters = letters[letters.index((litera_max[1])) + 1]
                    litera_max = litera_max[0] + new_letters
                else:
                    litera_max = letters[letters.index((litera_max[0])) + 1] + "a"
                day_damage /= 1000
            if day >= 100000:
                return 0

        while day_damage <= damage:
            day += 1
            day_damage *= 1.06599999998486

        return day
    else:
        return 0


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
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Weapon Damage")

    @app_commands.command(name="daytodamage", description="Input a Day to receive the estimate one-shot damage "
                                                          "required to beat it")
    async def daytodamage_f(self, interaction: discord.Interaction, day: int, invisible: bool = True) -> None:
        print(f"Trying Damage to Day with the following data: Day: {day}")
        damage, litere = daytodamage(day)
        embed = discord.Embed(title="Day to Damage Calculator <a:kafkakurukuru:1118233531110412461>",
                              color=0x71368a)
        embed.add_field(name="",
                        value=f"The approximate one-shot damage required for **Day {day}** is **{round(damage)}{litere}**! "
                              f"*(+/- 10 days).*",
                        inline=False)
        embed.add_field(name="", value=f"*These calculations are using data from [IINII's Pushing Sheet]"
                                       "(https://docs.google.com/spreadsheets/d/1-vl0Kwa9R1Bl36WHjihjItFfNVKi8LGRSEkqHy9tLuA/edit?usp=sharing)*",
                        inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        if damage == 0:
            await interaction.response.send_message(f"Day must be between 2000 and 37000", ephemeral=True)
        else:
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Damage to Day")

    @app_commands.command(name="damagetoday", description="Input the damage number of your DPS Hero to get an estimate "
                                                          "of your one-shot pushing range")
    async def damagetoday_f(self, interaction: discord.Interaction, damage: int, suffix: str, invisible: bool = True) -> None:
        print(f"Trying Damage to Day with the following data: Damage: {damage} Suffix {suffix}")
        day = damagetoday(damage, suffix.lower())
        embed = discord.Embed(title="Damage to Day Calculator <a:kafkakurukuru:1118233531110412461>",
                              color=0x71368a)
        embed.add_field(name="",
                        value=f"**{damage}{suffix.lower()}** damage will approximately put you to **Day {day}** with one-shots! "
                              f"*(+/- 10 days).*",
                        inline=False)
        embed.add_field(name="", value=f"*These calculations are using data from [IINII's Pushing Sheet]"
                                       f"(https://docs.google.com/spreadsheets/d/1-vl0Kwa9R1Bl36WHjihjItFfNVKi8LGRSEkqHy9tLuA/edit?usp=sharing)*",
                        inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        if day == 0:
            await interaction.response.send_message(f"Invalid data, please try again. Example: 123hi damage translates "
                                                    f"to Day 21467.", ephemeral=True)
        else:
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Damage to Day")

    @app_commands.command(name="multiplier", description="Input a damage multiplier to receive a Day equivalent")
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
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Multiplier")

    @app_commands.command(name="rewindspots", description="Input a day & the days to look ahead to receive the Rewind "
                                                          "Scores for the said spots. Max 500.")
    async def spots_f(self, interaction: discord.Interaction, starting_day: int, days_to_look_ahead: int, invisible: bool = True) -> None:
        print(f"Trying 'Rewind Spots' with the following data: Starting Day: {starting_day}, Days to look ahead: {days_to_look_ahead}")
        if 50 <= days_to_look_ahead <= 500 and (starting_day + days_to_look_ahead) <= 37500 and starting_day > 50:
            embed = spots(starting_day, days_to_look_ahead)
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "Invalid data, please try again.\n- Max 500 spots a time.\n- Currently, "
                "the mob data goes up to Day 37500.\n- Days to look ahead must "
                "be greater than 50.\n- Starting day must be above 50.", ephemeral=True)
        print("Done w/ Rewind Spots")

    @app_commands.command(name="detailed_rewindspot", description="Input a day to receive detailed info on the spot ("
                                                                  "each Mob and Boss for each portal)")
    async def detailed_spots_f(self, interaction: discord.Interaction, day: int, invisible: bool = True) -> None:
        print(f"Trying 'Detailed Spot' with the following data: Day: {day}")
        embed = detailed_spot(day)
        if embed == 0:
            await interaction.response.send_message("Invalid spot/data, please try again.", ephemeral=True)
        else:
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Detailed Spot")

    @app_commands.command(name="best_rewindspot", description="Input a day & the days to look ahead to receive the day with the "
                                                        "best Rewind Score")
    async def best_spots_f(self, interaction: discord.Interaction, starting_day: int, days_to_look_ahead: int, invisible: bool = False) -> None:
        print(f"Trying 'Best Spots' with the following data: Starting Day: {starting_day}, Days to look ahead: {days_to_look_ahead}")
        if 100 <= days_to_look_ahead <= 500 and (starting_day + days_to_look_ahead) <= 37500 and starting_day > 50:
            embed = best_spot(starting_day, days_to_look_ahead)
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Invalid data, please try again.\n- Max 500 spots a time.\n- Currently, "
                                                    "the mob data goes up to Day 37500.\n- Days to look ahead must "
                                                    "be greater than 100.\n- Starting day must be above 50.", ephemeral=True)
        print("Done w/ Best Spots")

    @app_commands.command(name="optimal_rewind",
                          description="Input your elixir data to receive the minimum amount of rewinds for your goal")
    async def elixirsheet_f(self, interaction: discord.Interaction, em_level: str, elixir_per_rewind: str,
                           all_skills_old: str, all_skills_new: str, milestone: int = 2, invisible: bool = True) -> None:
        print(f"Trying Elixir Calc with the following data: em {em_level} elixir {elixir_per_rewind} old {all_skills_old} "
              f"new {all_skills_new} milestone {milestone}")

        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        print("trandafiri")

        embed = elixirsheet(em_level=em_level, elixir_per_rewind=elixir_per_rewind, all_skills_old=all_skills_old,
                            all_skills_new=all_skills_new, milestone=milestone, invisible=invisible)
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
                                  f'milestone: {milestone} invisible: {invisible}'
                            , inline=False)
            embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.followup.send(embed=embed, ephemeral=True)

        print("Done w/ Elixir calc")

    @app_commands.command(name="dungeon_goldd",
                          description="Input your dungeon data to receive the best way to spend your keys")
    async def gold_sheet_f(self, interaction: discord.Interaction, crit_dmg_stat_level: str, gold_from_dungeon_keys :str, keys:str, target_days: int, invisible: bool = True) -> None:
        print(f"Trying Gold Sheet with the following data: cdmg {crit_dmg_stat_level} gold {gold_from_dungeon_keys} keys {keys} target {target_days}")
        embed = gold_sheet(cdmg=crit_dmg_stat_level, gold=gold_from_dungeon_keys, keys=keys, target=target_days, invisible=invisible)
        if embed == 0:
            embed = discord.Embed(title="", color=0x71368a)
            embed.add_field(name=f"Invalid data, please try again. Long tap/copy the command you just used if you want "
                                 "to make any adjustments!",
                            value=f"/calc dungeon_gold crit_dmg_stat_level: {crit_dmg_stat_level} gold_from_dungeon_keys: {gold_from_dungeon_keys} "
                                  f"keys: {keys} target_days: {target_days} invisible: {invisible}")
            embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        print("Done w/ Gold Sheet")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Formulas(bot))
