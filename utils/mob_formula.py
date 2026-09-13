M = ["Dino", "Rex", "Caps", "Gargoyle", "Blob", "Shade", "Frosk", "Warmonger", "Banshee"]

def get_mob(day: int) -> str:
    if day < 1:
        return "Invalid day"

    forced = {1: "Dino", 4: "Caps", 21: "Blob", 35: "Shade", 51: "Frosk", 301: "Warmonger"}
    if day in forced:
        return forced[day]

    if day <= 3: n = 2
    elif day <= 10: n = 3
    elif day <= 20: n = 4
    elif day <= 34: n = 5
    elif day <= 50: n = 6
    elif day <= 300: n = 7
    elif day <= 3000: n = 8
    else: n = 9

    x = day & 0xFFFFFFFF
    y = (1812433253 * x + 1) & 0xFFFFFFFF
    z = (1812433253 * y + 1) & 0xFFFFFFFF
    w = (1812433253 * z + 1) & 0xFFFFFFFF
    t = (x ^ (x << 11)) & 0xFFFFFFFF
    w = (w ^ (w >> 19) ^ t ^ (t >> 8)) & 0xFFFFFFFF

    return M[w % n]

def get_mob_range(starting_day: int, how_many: int) -> list[str]:
    result = []

    for day in range(starting_day, starting_day + how_many + 1):
        result.append(get_mob(day))

    return result

def get_mob_range_with_days(starting_day: int, how_many: int) -> list[list[int | str]]:
    result = []

    for day in range(starting_day, starting_day + how_many + 1):
        temp = []

        temp.append(day)
        temp.append(get_mob(day))
        result.append(temp)

    return result

mob = get_mob(49090)
print(mob)