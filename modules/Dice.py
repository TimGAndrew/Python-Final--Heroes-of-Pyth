import random

# THIS FILE IS IN CHARGE OF ANYTHING TO DO WITH ROLLING THE RANDOM DICE USED IN THE GAME

# ============================================================================================================= #
# ROLLS A RANDOM DICE, FORMAT IS 'XdY', WHERE x IS THE AMOUNT OF DIE TO ROLL, AND Y IS THE TYPE OF DIE TO ROLL
# EX. '3d6' = ROLL THREE SIX SIDED DICE ; '2d8' = ROLL TWO EIGHT SIDED DIE
def roll(what):

    amount, type_die = what.split('d')

    if type_die == '4':
        return d4(int(amount))
    elif type_die == '6':
        return d6(int(amount))
    elif type_die == '8':
        return d8(int(amount))
    elif type_die == '10':
        return d10(int(amount))
    elif type_die == '12':
        return d12(int(amount))
    elif type_die == '20':
        return d20(int(amount))
    elif type_die == '100':
        return d100(int(amount))


# ============================================================================================================= #
# ROLLS X AMOUNT OF 4 SIDED DIE, RETURNS RESULTS AS A LIST
def d4(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 4))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 6 SIDED DIE, RETURNS RESULTS AS A LIST
def d6(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 6))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 8 SIDED DIE, RETURNS RESULTS AS A LIST
def d8(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 8))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 10 SIDED DIE, RETURNS RESULTS AS A LIST
def d10(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 10))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 12 SIDED DIE, RETURNS RESULTS AS A LIST
def d12(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 12))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 20 SIDED DIE, RETURNS RESULTS AS A LIST
def d20(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 20))
        counter += 1
    return rolls


# ============================================================================================================= #
# ROLLS X AMOUNT OF 100 SIDED DIE, RETURNS RESULTS AS A LIST
def d100(x):
    rolls = []
    counter = 1
    while counter <= x:
        rolls.append(random.randint(1, 100))
        counter += 1
    return rolls
