from modules.Dice import *
from modules.Hero import *
import modules.GameRules as gr
import modules.Spells as Spell
import math


# ============================================================================================================= #
# THE PURPOSE OF THIS MODULE IS TO DEAL WITH COMBAT, COMBAT RESOLUTION, AND ANYTHING COMBAT RELATED
class Combat:

    # ============================================================================================================= #
    # CLASS CONSTRUCTOR
    def __init__(self, p1, p2):
        self.log = ['', '', '', '', '']                             # DECLARE EMPTY COMBAT LOG LIST
        self.p1 = p1                                                # PLAYER ONE
        self.p2 = p2                                                # PLAYER TWO
        self.combat_order = self.determine_initiative()
        self.winner = None

    # ============================================================================================================= #
    # DETERMINES COMBAT INITIATIVE
    def determine_initiative(self):

        # ROLL FOR INITIATIVE
        roll = d100(1)

        if roll[0] <= 50:
            return self.p1, self.p2     # PLAYER 1 GOES FIST
        else:
            return self.p2, self.p1     # PLAYER 2 GOES FIRST

    # ============================================================================================================= #
    # USED ON THE COMBAT SCREEN TO DISPLAY WHOSE TURN IT IS
    def get_attacking(self, player):

        if player == self.get_attacker():
            return " YOUR TURN "

        return ''

    # ============================================================================================================= #
    # RETURNS THE NAME OF THE HERO WHO'S CURRENTLY ATTACKING
    def get_attacker_name(self):
        return self.combat_order[0].name

    # ============================================================================================================= #
    # RETURNS THE HERO OBJECT THAT'S CURRENTLY ATTACKING
    def get_attacker(self):
        return self.combat_order[0]

    # ============================================================================================================= #
    # THIS FUNCTION RESOLVES ALL THE COMBAT
    def resolve_combat(self, option):

        # ESTABLISH WHO'S ATTACKING, AND WHO'S DEFENDING
        attacker = self.combat_order[0]
        defender = self.combat_order[1]

        # ATTACKER DECIDES TO ATTACK
        if attacker.moves[option] == Moves.ATTACK:

            log = '{} attempts to attack {}..'.format(attacker.name, defender.name)
            self.add_combat_log(log)

            # TRY TO HIT HERE
            if self.try_hit(defender, attacker):

                # CALCULATE DAMAGE
                damage = self.calc_damage(attacker, defender)

                # OPPONENT TAKES DAMAGE
                defender.stats["HP"] -= damage

                log = "{} hits, causing {} damage".format(attacker.name, damage)
                self.add_combat_log(log)

        # ATTACKER DECIDES TO EVADE
        elif attacker.moves[option] == Moves.EVADE:

            self.add_combat_log('{} decides to EVADE'.format(attacker.name))
            effect = gr.Buff.EVADE.copy()                                       # GIVE ATTACKER EVADE BUFF
            attacker.status_effects.append(effect)

        # ATTACKER DECIDES TO GUARD
        elif attacker.moves[option] == Moves.GUARD:

            self.add_combat_log('{} prepares to GUARD'.format(attacker.name))
            effect = gr.Buff.GUARD.copy()                                       # GIVE ATTACKER GUARD BUFF
            attacker.status_effects.append(effect)

        # ATTACKER DECIDES TO PARRY
        elif attacker.moves[option] == Moves.PARRY:

            self.add_combat_log('{} prepares to PARRY'.format(attacker.name))
            effect = gr.Buff.PARRY.copy()                                       # GIVE ATTACKER PARRY BUFF
            attacker.status_effects.append(effect)

        # ATTACKER IS CASTING A SPELL...
        elif attacker.moves[option] == Moves.CAST:

            spell = attacker.spells[0]

            # IF PRIEST, SPELL IS HEAL
            if attacker.spells[0] == Spell.HEAL:

                # HEAL ATTACKER
                # attacker.try_cast() MAKES SURE HERO HAS ENOUGH MP TO CAST THE SPELL
                if attacker.try_cast(spell.mp):
                    heal_amt = sum(roll(spell.damage)) + (attacker.stats["INT"] * attacker.modifiers["MAGIC"])

                    # MAKE SURE HP DOESN'T GO OVER MAX
                    if heal_amt + attacker.stats['HP'] > attacker.stats['HP_MAX']:
                        attacker.stats['HP'] = attacker.stats['HP_MAX']
                    else:
                        attacker.stats['HP'] += heal_amt

                        self.add_combat_log('{} casts heal, healing {} HP'.format(attacker.name, heal_amt))

                # NOT ENOUGH MP!
                else:
                    self.add_combat_log('{} can\'t cast {} without enough MP!'.format(attacker.name,
                                                                                      spell.name))

                    # SINCE SPELL COULDN'T BE CAST, RETURN FALSE TO MAKE PLAYER CHOOSE ANOTHER OPTION
                    return False

            # MAGES CAST FIREBALL
            elif attacker.spells[0] == Spell.FIREBALL:

                # CAST FIREBALL
                # attacker.try_cast() MAKES SURE HERO HAS ENOUGH MP TO CAST THE SPELL
                if attacker.try_cast(spell.mp):
                    self.add_combat_log('{} casts {}...'.format(attacker.name, spell.name))

                    # CHECK IF SPELL HIT
                    if self.try_hit_spell(defender, attacker, spell):
                        # SPELL HIT

                        # CALCULATE DAMAGE FOR SPELL
                        damage = self.calc_spell_damage(attacker, defender, spell)

                        # OPPONENT TAKES DAMAGE
                        defender.stats['HP'] -= damage

                        self.add_combat_log('{} hits {} with {} for {}'.format(attacker.name,
                                                                               defender.name,
                                                                               spell.name,
                                                                               damage))

                else:
                    # NOT ENOUGH MP!
                    self.add_combat_log('{} can\'t cast {} without enough MP!'.format(attacker.name,
                                                                                      spell.name))

                    # SINCE SPELL COULDN'T BE CAST, RETURN FALSE TO MAKE PLAYER CHOOSE ANOTHER OPTION
                    return False

        # HANDLE MP REGENERATION...

        # MAKE SURE IT DOESN'T GO OVER THE MAX MP
        if attacker.stats['MP'] < attacker.stats['MP_MAX']:
            regen_amt = math.ceil(attacker.stats['WIS'] * attacker.modifiers['MAGICREGEN'])

            if attacker.stats['MP'] + regen_amt > attacker.stats['MP_MAX']:
                attacker.stats['MP'] = attacker.stats['MP_MAX']
            else:
                attacker.stats['MP'] += regen_amt

        # CHECK IF OPPONENT IS DEAD AND IF SO, END THE MATCH
        if defender.stats["HP"] < 1:
            self.add_combat_log("{} is dead!!".format(defender.name))

            # STORE THE WINNER HERE FOR LATER USE
            self.winner = attacker

            return True

        # HANDLE BUFF COUNTDOWN FOR BOTH PLAYERS
        attacker.status_effect_countdown()
        defender.status_effect_countdown()

        # SWITCH PLAYER ORDER FOR NEXT TURN
        self.combat_order = [defender, attacker]

        return False

    # ============================================================================================================= #
    # ATTEMPT TO HIT THE OPPONENT AND RETURN THE RESULTS
    def try_hit(self, defender, attacker):

        # BASE CHANCE TO HIT
        chance = 90

        # CALCULATE DODGE CHANCE
        dodge = math.ceil(defender.stats["DEX"] * defender.modifiers["DODGE"])

        # DOES DEFENDER HAVE EVADE BUFF?
        for effect in defender.status_effects:
            if effect['Name'] == 'Evade':
                dodge += effect['Effect']

        # GET NATURAL PARRY CHANCE FOR THE OPPONENT
        parry_chance = math.ceil(defender.stats["DEX"] * defender.modifiers["PARRY"])

        # PARRY ROLL
        parry_roll = d100(1)[0]

        # DID OPPONENT PREPARE TO PARRY THE PREVIOUS TURN?
        for effect in defender.status_effects:
            if effect['Name'] == 'Parry':
                parry_chance += effect['Effect']

                # OPPONENT HAS PARRY BUFF..CHECK TO SEE IF PARRIED
                if parry_roll < parry_chance:

                    # IF PARRY SUCCESSFUL ATTACKER TAKES DAMAGE
                    parry_damage = self.calc_damage(defender, attacker)
                    self.add_combat_log('{} parried, and hit {} for {} damage'.format(defender.name,
                                                                                      attacker.name,
                                                                                      parry_damage))
                    attacker.stats['HP'] -= parry_damage
                    return False

                else:

                    # OPPONENT FAILED PARRY ROLL, HE TAKES EXTRA DAMAGE NEXT ROUND
                    attacker.status_effects.append(gr.Buff.PARRY_DAMAGE_BONUS)
                    self.add_combat_log('{} attempted to parry, but failed'.format(defender.name))

        # NATURAL PARRY CHANCE
        if parry_roll < parry_chance:
            self.add_combat_log('{} parried {}\'s attack'.format(defender.name, attacker.name))
            return False

        # BASE HIT CHANCE
        chance -= dodge

        # ROLL TO HIT
        roll = d100(1)
        if roll[0] <= chance:

            # ATTACKER HIT
            return True

        # ATTACKER MISSED
        self.add_combat_log("{} misses!".format(attacker.name))
        return False

    # ============================================================================================================= #
    # CALCULATE DAMAGE ON HIT
    def calc_damage(self, attacker, defender):

        # CALCULATE BASE DAMAGE RESISTANCE
        resist = math.ceil(defender.stats['STA'] * defender.modifiers['DEFENSE'])

        # CALCULATE DAMAGE, TAKE INTO ACCOUNT ATTACKER'S WEAPON
        weapon_dmg = roll(attacker.weapon.damage)
        dmg_bonus = attacker.stats["STR"] * attacker.modifiers["DAMAGE"]
        damage = sum(weapon_dmg) + dmg_bonus

        # DID OPPONENT CHOOSE TO GUARD ON THE PREVIOUS TURN?
        for effect in defender.status_effects:
            if effect['Name'] == 'Guard':
                resist += effect['Effect']

                # OPPONENT HAS GUARD BUFF, RESIST DAMAGE
                damage -= (damage * (resist / 100))

        # APPLY DAMAGE BONUS IF OPPONENT FAILED TO PARRY THE PREVIOUS ROUND
        for effect in attacker.status_effects:
            if effect['Name'] == 'ParryDamageBonus':
                damage += (damage * effect['Effect'])

        return math.floor(damage)

    # ============================================================================================================= #
    # CALCULATE DAMAGE WITH SPELL
    def calc_spell_damage(self, attacker, defender, spell):

        # CALCULATE SPELL DAMAGE, INCLUDE SPELL DAMAGE MODIFIERS
        damage = sum(roll(spell.damage)) + (attacker.stats['INT'] * attacker.modifiers['MAGIC'])

        return math.floor(damage)

    # ============================================================================================================= #
    # ATTEMPT TO HIT THE OPPONENT WITH SPELL
    def try_hit_spell(self, defender, attacker, spell):

        # BASE CHANCE TO HIT
        chance = 90

        # CALCULATE DODGE CHANCE
        dodge = math.ceil(defender.stats["DEX"] * defender.modifiers["DODGE"])

        # DOES DEFENDER HAVE EVADE
        for effect in defender.status_effects:
            if effect['Name'] == 'Evade':
                dodge += effect['Effect']

        # CALC TOTAL HIT CHANCE
        chance -= dodge

        # DO HIT ROLL
        roll = d100(1)

        if roll[0] <= chance:
            return True

        self.add_combat_log('{}\'s {} misses'.format(attacker.name, spell.name))
        return False

    # ============================================================================================================= #
    # ADD TO COMBAT LOG
    def add_combat_log(self, message):

        self.log[4] = self.log[3]
        self.log[3] = self.log[2]
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]

        self.log[0] = message
