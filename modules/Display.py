

# ============================================================================================================= #
# THE MAIN PURPOSE OF THIS CLASS IS TO UPDATE THE CHARACTER SHEET WITH ALL THE CHARACTER INFORMATION
class Display:

    _menus = {}

    # ============================================================================================================= #
    # CLASS CONSTRUCTOR
    def __init__(self):
        pass

    # ============================================================================================================= #
    # DRAW THE COMBAT CHARACTER SHEET
    @staticmethod
    def draw_combat_sheet(ch1, ch2, combat):

        # LOAD THE CHARACTER SHEET TEMPLATE FROM FILE, FORMAT IT WITH INFO FROM HEROES
        with open("resources/character_sheet_template.txt", "r", encoding='UTF-8') as file:
            c = file.read()

            c = c.format(
                ch1.role.center(12),                                                    # HERO 1 ROLE
                ch1.get_status_icons().ljust(20),                                       # HERO 1 STATUS ICONS
                ch2.get_status_icons().rjust(20),                                       # HERO 2 STATUS ICONS
                ch2.role.center(12),                                                    # HERO 2 ROLE
                ch1.name.ljust(39),                                                     # HERO 1 NAME
                ch2.name.rjust(39),                                                     # HERO 2 NAME
                Display.get_hpmp_bar(ch1.stats["HP_MAX"], ch1.stats["HP"], 36, '▓'),   # HERO 1 HP BAR
                Display.get_hpmp_bar(ch2.stats["HP_MAX"], ch2.stats["HP"], 36, '▓'),   # HERO 2 HP BAR
                Display.get_hpmp_bar(ch1.stats["MP_MAX"], ch1.stats["MP"], 36, '▓'),   # HERO 1 MP BAR
                Display.get_hpmp_bar(ch2.stats["MP_MAX"], ch2.stats["MP"], 36, '▓'),   # HERO 2 MP BAR
                str(ch1.stats["STR"]).ljust(2),                                         # HERO 1 STR
                str(ch1.stats["DEX"]).ljust(2),                                         # HERO 1 DEX
                str(ch1.stats["STA"]).ljust(2),                                         # HERO 2 STR
                str(ch1.stats["INT"]).ljust(2),                                         # HERO 2 DEX
                str(ch1.stats["WIS"]).ljust(2),                                         # HERO 1 STA
                str(ch2.stats["STR"]).ljust(2),                                         # HERO 1 INT
                str(ch2.stats["DEX"]).ljust(2),                                         # HERO 2 STA
                str(ch2.stats["STA"]).ljust(2),                                         # HERO 2 INT
                str(ch2.stats["INT"]).ljust(2),                                         # HERO 1 WIS
                str(ch2.stats["WIS"]).ljust(2),                                         # HERO 2 WIS
                ch1.weapon.name.ljust(39),                                              # HERO 1 WEAPON
                ch2.weapon.name.ljust(39),                                              # HERO 2 WEAPON
                combat.get_attacking(ch1).center(41, "▒"),                             # HERO 1 TURN BAR
                combat.get_attacking(ch2).center(41, "▒"),                             # HERO 1 TURN BAR
                combat.log[4].ljust(83),                                                # COMBAT LOG
                combat.log[3].ljust(83),                                                # COMBAT LOG
                combat.log[2].ljust(83),                                                # COMBAT LOG
                combat.log[1].ljust(83),                                                # COMBAT LOG
                combat.log[0].ljust(83),                                                # COMBAT LOG
            )

            return c

    # ============================================================================================================= #
    # DRAW THE CHARACTER SHEET DISPLAYED AFTER CHARACTER CREATION
    @staticmethod
    def draw_character_sheet(character):

        # LOAD CHARACTER SHEET TEMPLATE FROM FILE AND FORMAT IT WITH HERO INFORMATION
        with open("resources/character_sheet_template_single.txt", "r", encoding='UTF-8') as file:
            c = file.read()

            c = c.format(
                character.name.ljust(46),                    # HERO NAME
                character.role.ljust(46),                    # HERO ROLE
                str(character.stats["STR"]).ljust(2),        # HERO STR
                str(character.stats["DEX"]).ljust(33),       # HERO DEX
                str(character.stats["STA"]).ljust(2),        # HERO STA
                str(character.stats["INT"]).ljust(33),       # HERO INT
                str(character.stats["WIS"]).ljust(41),       # HERO WIS
                str(character.stats["HP"]).ljust(28),        # HERO HP
                str(character.stats["MP"]).ljust(28),        # HERO MP
                character.weapon.name.ljust(45)              # HERO WEAPON
            )

        return c.center(100, ' ')

    # ============================================================================================================= #
    # DRAWS THE TITLE SCREEN AT THE START OF THE GAME
    @staticmethod
    def draw_title_screen():

        with open('resources/Title2.txt', 'r', encoding='UTF-8') as f:
            title = f.read() + '\n'

        return title

    # ============================================================================================================= #
    # DRAW THE HP AND MP BARS AND CALCULATES THEIR SIZE AND POSITION
    @staticmethod
    def get_hpmp_bar(max_hp, cur_hp, bar_length, bar_char):

        if cur_hp > max_hp:
            return None

        if max_hp == 0:
            return ''.ljust(bar_length)

        try:
            percentage = cur_hp / max_hp
        except ZeroDivisionError:
            return None

        addon = '[{}/{}]'.format(int(cur_hp), int(max_hp))

        actual_length = bar_length * percentage
        bar_string = bar_char * int(actual_length)

        if (actual_length+len(addon)) <= bar_length:
            bar_string += addon

        full_string = bar_string.ljust(bar_length)
        return full_string


if __name__ == '__main__':
    pass
