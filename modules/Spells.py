

# CLASS USED TO CREATE SPELL TEMPLATES
class Spell:

    # CLASS CONSTRUCTOR
    def __init__(self, name, damage, mp):
        self.name = name
        self.damage = damage
        self.mp = mp

# PREMADE SPELLS
FIREBALL = Spell('Fireball', '2d6', 10)
HEAL = Spell('Heal', '2d4', 8)