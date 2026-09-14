def calculate_elo(ra, rb, matches_a, matches_b):
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    eb = 1 / (1 + 10 ** ((ra - rb) / 400))

    ka = 40 if matches_a < 20 else (16 if ra > 2000 else 24)
    kb = 40 if matches_b < 20 else (16 if rb > 2000 else 24)

    new_a = round(ra + ka * (1 - ea))
    new_b = round(rb + kb * (0 - eb))

    return new_a, new_b