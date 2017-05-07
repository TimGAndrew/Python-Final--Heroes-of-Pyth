
# ENUMERATIONS FOR THE BUFFS USED IN THE GAME
class Buff:
    GUARD = {
        'Name': 'Guard',
        'Description': 'Increased defense for one turn.',
        'Icon': '◊',
        'Duration': 2,
        'Effect': 50
        }

    EVADE = {
        'Name': 'Evade',
        'Description': 'Increased chance to dodge for one turn.',
        'Icon': '→',
        'Duration': 2,
        'Effect': 50
        }

    PARRY = {
        'Name': 'Parry',
        'Description': 'Increased chance to parry for one turn.',
        'Icon': '≠',
        'Duration': 2,
        'Effect': 50
        }

    PARRY_DAMAGE_BONUS = {
        'Name': 'ParryDamageBonus',
        'Description': 'Adds damage bonus after failed parry.',
        'Icon': '',
        'Duration': 2,
        'Effect': 1.5
        }