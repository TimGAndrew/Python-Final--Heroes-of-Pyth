

# WEAPON CLASS
class Weapon:

    # CLASS CONSTRUCTOR
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

# PREMADE WEAPONS USED IN THE GAME
DAGGER = Weapon('Dagger', '1d4')
ONE_HANDED_SWORD = Weapon ('1H-Sword', '1d6')
TWO_HANDED_SWORD = Weapon ('2H-Sword', '1d8')
AXE = Weapon('Axe', '1d4')
BATTLE_AXE = Weapon('Battle-Axe', '1d8')
WAND = Weapon('Wand', '1d4')
STAFF = Weapon('Staff', '1d6')
MACE = Weapon('Mace', '1d6')
KATAR = Weapon('Katar', '1d6')