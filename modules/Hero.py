import random
import pickle
import modules.Spells as Spell
import modules.Inventory as Inventory

# THIS CLASS' PURPOSE IS TO HANDLE ANY ROUTINES AND DATA HAVING TO DO WITH THE
# CHARACTERS IN THE GAME


# MOVES ENUMERATION
class Moves:
    ATTACK = 'Attack'
    EVADE = 'Evade'
    GUARD = 'Guard'
    PARRY = 'Parry'
    CAST = 'Cast'
    #VANISH = 'Vanish'


# ============================================================================================================= #
# HERO CLASS
class Hero:

    # ============================================================================================================= #
    # CLASS ATTRIBUTES

    # LIST OF ROLES/CLASSES
    _roles = [
        "Warrior",
        "Rogue",
        "Priest",
        "Mage"
    ]

    # STAT BONUSES BASED ON CHARACTER ROLE
    _class_bonuses = {
        "Warrior": {"STR": 10, "DEX": 0, "STA": 0, "INT": -5, "WIS": 0},
        "Rogue": {"STR": 5, "DEX": 5, "STA": 0, "INT": -5, "WIS": 0},
        "Priest": {"STR": -5, "DEX": 0, "STA": 0, "INT": 5, "WIS": 5},
        "Mage": {"STR": -5, "DEX": 0, "STA": 0, "INT": 8, "WIS": 2}
    }

    # MODIFIER TYPES (AND THE STATS THEY DEPEND ON):
    #   ATTACK:    (DEX)      CHANCE TO HIT
    #   DEFENSE:   (STA)      CHANCE TO MITIGATE DAMAGE
    #   DAMAGE:    (STR)      DAMAGE BONUS
    #   DODGE:     (DEX)      CHANCE TO DODGE ATTACK
    #   PARRY:     (DEX)      CHANCE TO PARRY ATTACK
    #   MAGIC      (INT)      MAGIC SPELL BONUS
    #   MAGICREGEN (WIS)      MAGIC REGENERATION

    _modifiers = {
        "Warrior": {
            "DAMAGE": 0.3,
            "DEFENSE": 0.25,
            "DODGE": 0.05,
            "PARRY": 0.2,
            "MAGIC": 0,
            "MAGICREGEN": 0
        },

        "Rogue": {
            "DAMAGE": 0.25,
            "DEFENSE": 0.20,
            "DODGE": 0.5,
            "PARRY": 0.2,
            "MAGIC": 0,
            "MAGICREGEN": 0
        },

        "Priest": {
            "DAMAGE": 0.1,
            "DEFENSE": 0.15,
            "DODGE": 0.1,
            "PARRY": 0.1,
            "MAGIC": 0.3,
            "MAGICREGEN": 0.2
        },

        "Mage": {
            "DAMAGE": 0.1,
            "DEFENSE": 0.15,
            "DODGE": 0.1,
            "PARRY": 0.1,
            "MAGIC": 0.4,
            "MAGICREGEN": 0.1
        }
    }

    # MOVES AVAILABLE PER ROLE
    _moves = {
        'Warrior': [Moves.ATTACK, Moves.GUARD, Moves.PARRY],
        'Rogue': [Moves.ATTACK, Moves.EVADE, Moves.PARRY],
        'Priest': [Moves.ATTACK, Moves.EVADE, Moves.CAST],
        'Mage': [Moves.ATTACK, Moves.EVADE, Moves.CAST]
    }

    # SPELLS AVAILABLE PER ROLE
    _spells = {
        'Warrior' : [],
        'Rogue' : [],
        'Mage' : [Spell.FIREBALL],
        'Priest' : [Spell.HEAL],
    }

    # WEAPONS AVAILABLE PER ROLE
    _weapons = {
        'Warrior': [Inventory.ONE_HANDED_SWORD,
                     Inventory.AXE,
                     Inventory.BATTLE_AXE,
                     Inventory.TWO_HANDED_SWORD],

        'Rogue': [Inventory.DAGGER,
                   Inventory.AXE,
                   Inventory.ONE_HANDED_SWORD,
                   Inventory.KATAR],

        'Priest': [Inventory.DAGGER,
                    Inventory.STAFF,
                    Inventory.WAND,
                    Inventory.MACE],

        'Mage': [Inventory.DAGGER,
                    Inventory.STAFF,
                    Inventory.WAND,
                    Inventory.ONE_HANDED_SWORD]
    }

    # ============================================================================================================= #
    # MAIN CONSTRUCTOR (USED WHEN CREATING A NEW CHARACTER)
    def __init__(self, name, seed=None, role=None, stats=None, modifiers=None):

        self.status_effects = []     # STATUS EFFECTS THE CHARACTER HAS ACTIVE
        self.stats = {}              # DICTIONARY OF CHARACTER STATS
        self.role = ""               # CHARACTER'S ROLE
        self.modifiers = {}          # DICTIONARY OF CHARACTER MODIFIERS
        self.spells = []             # LIST OF SPELLS (IF ANY)
        self.weapon = None           # CHARACTER WEAPONS

        # IF NO SEED IS PROVIDED, CREATE CHARACTER FROM DATA (MOSTLY USED FOR TESTING PURPOSES)
        # ALL OPTIONAL ARGUMENTS MUST BE PROVIDED
        if seed is None:

            self.name = name
            self.role = role
            self.stats = stats
            self.modifiers = modifiers
            self.moves = None

        else:  # OTHERWISE GENERATE RANDOMLY

            self.name = name
            self.seed = seed
            self.generate_stats(self.seed)
            self.apply_bonuses()
            self.modifiers = self._modifiers[self.role]
            self.move_list = self._moves[self.role]

    # ============================================================================================================= #
    # GENERATES NEW CHARACTER FROM SEED PROVIDED
    def generate_stats(self, seed):

        random.seed(seed)

        # ROLL FOR STATS
        self.stats = {
            "STR": random.randrange(3, 18),
            "DEX": random.randrange(3, 18),
            "INT": random.randrange(3, 18),
            "WIS": random.randrange(3, 18),
            "STA": random.randrange(3, 18),
            "HP": 0,
            "HP_MAX": 0,
            "MP": 0,
            "MP_MAX": 0,
        }

        # DETERMINE HERO'S ROLE
        self.role = self._roles[random.randrange(0, len(self._roles))]

        # GET MOVES
        self.moves = self._moves[self.role]

        # GET SPELLS
        self.spells = self._spells[self.role]

        # WEAPONS
        self.weapon = self._weapons[self.role][random.randrange(len(self._weapons[self.role]))]

        # RESET RANDOM SEED TO SYSTEM TIME
        random.seed()

    # ============================================================================================================= #
    # APPLIES BONUSES TO THIS CHARACTER BASED ON ROLE
    def apply_bonuses(self):

        for b in self._class_bonuses:
            if b == self.role:
                bonuses = self._class_bonuses[b]

                # APPLY BONUSES, BUT MAKE SURE STATS ARE NOT LOWER THAN 3
                self.stats["STR"] = max([self.stats["STR"] + bonuses["STR"], 3])
                self.stats["DEX"] = max([self.stats["DEX"] + bonuses["DEX"], 3])
                self.stats["STA"] = max([self.stats["STA"] + bonuses["STA"], 3])
                self.stats["WIS"] = max([self.stats["WIS"] + bonuses["WIS"], 3])
                self.stats["INT"] = max([self.stats["INT"] + bonuses["INT"], 3])

        # DETERMINE HP
        self.stats["HP"] = self.stats["STA"] * 2
        self.stats["HP_MAX"] = self.stats["HP"]

        # DETERMINE MP
        self.stats['MP'] = self.stats['INT'] * 2
        self.stats['MP_MAX'] = self.stats['MP']

    # ============================================================================================================= #
    # COUNTDOWN THE DURATION OF ANY BUFFS THIS HERO HAS
    def status_effect_countdown(self):

        for effect in self.status_effects:
            effect['Duration'] -= 1

        for i in reversed(range(len(self.status_effects))):
            if self.status_effects[i]['Duration'] <= 0:
                self.status_effects.remove(self.status_effects[i])

    # ============================================================================================================= #
    # CHECK TO SEE IF HERO HAS ENOUGH MP TO CAST SPELL, AND IF SO, SUBTRACT THE AMOUNT
    def try_cast(self, mp):

        if self.stats['MP'] - mp < 0:
            return False

        self.stats['MP'] -= mp
        return True

    # ============================================================================================================= #
    # GET STATUS EFFECT ICONS
    def get_status_icons(self):

        icons = ''

        for effect in self.status_effects:
            icons += effect['Icon']

        return icons

    # ============================================================================================================= #
    # SAVE CHARACTER TO FILE USING SERIALIZATION
    @staticmethod
    def save(character, path):

        with open(path, 'wb') as f:
            pickle.dump(character, f, pickle.HIGHEST_PROTOCOL)

    # ============================================================================================================= #
    # LOADS CHARACTER FROM FILE USING SERIALIZATION
    @staticmethod
    def load(path):

        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except pickle.UnpicklingError:
            print("Error loading file: File corrupted")
            return None
        except FileNotFoundError:
            print("Error loading file: File not found")
        except:
            print("Oops! Something happened")

if __name__ == '__main__':
    pass

