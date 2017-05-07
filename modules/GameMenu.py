import math

# =============================================================================================================== #
# THIS CLASS IS IN CHARGE OF DISPLAYING A MESSAGE FRAME, SIMILAR TO A MENU, BUT WITH NO OPTIONS
class GameMessageFrame:
    def __init__(self, lines, padt=0, padb=0):
        self.lines = lines
        self.padt = padt
        self.padb = padb

    # =============================================================================================================== #
    # DRAWS A MESSAGE FRAME
    def get_frame(self):

        if len(self.lines) == 0:
            return

        frame = ""

        # TOP BORDER
        frame += "╔{:=^97}╗\n".format('')

        # TOP PADDING
        if self.padt > 0:
            for i in range(0, self.padt):
                frame += "║{:^97}║\n".format('')

        for line in self.lines:
            frame += "║{:^97}║\n".format(line)

        # BOTTOM PADDING
        if self.padb > 0:
            for i in range(0, self.padb):
                frame += "║{:^97}║\n".format('')

        # BOTTOM BORDER
        frame += "╚{:=^97}╝".format("")

        return frame


# =============================================================================================================== #
# THIS CLASS IS IN CHARGE OF DRAWING THE MENUS ON THE GAME
class GameMenu:

    # CLASS CONSTRUCTOR
    def __init__(self, options, enum=False, caption=None, padt=0, padb=0, hmenu=False, loop=False):

        self.options = options                      # OPTIONS THAT WILL APPEAR ON THE MENU
        self.enum = enum                            # ENUMERATE OPTIONS
        self.caption = caption                      # CAPTION FOR THE MENU
        self.padt = padt                            # TOP PADDING (IN LINES)
        self.padb = padb                            # BOTTOM PADDING (IN LINES)
        self.hmenu = hmenu                          # SET IF MENU IS HORIZONTAL
        self.loop = loop                            # LOOPING MENU

        self.selected_index = 0                     # INDEX OF CURRENTLY SELECTED ITEM ON THE MENU

    # =============================================================================================================== #
    # DRAWS A FRAMED MENU FROM THE LIST OF OPTIONS PROVIDED
    def get_menu(self):

        menu = ""

        # TOP BORDER
        menu += "╔{:=^97}╗\n".format('')

        # TOP PADDING
        if self.padt > 0:
            for i in range(0, self.padt):
                menu += "║{:^97}║\n".format('')

        # CAPTION
        if self.caption is not None:
            menu += "║{:^97}║\n".format(self.caption)
            menu += "║{:^97}║\n".format('')

        # VERTICAL MENU?
        if not self.hmenu:
            for i in range(len(self.options)):

                # ENUMERATED
                if self.enum:
                    if i == self.selected_index:
                        menu += '║' + str('>> {}. {} <<'.format(i+1, self.options[i])).center(97) + '║\n'
                    else:
                        menu += '║' + str('{}. {}'.format(i+1, self.options[i])).center(97) + '║\n'

                # NOT ENUMERATED
                else:
                    if i == self.selected_index:
                        menu += '║' + str('>> {} <<'.format(self.options[i])).center(97) + '║\n'
                    else:
                        menu += '║' + str('{}'.format(self.options[i])).center(97) + '║\n'
        # END VERTICAL

        # HORIZONTAL MENU
        else:

            col_len = 0
            h_options = ''

            if len(self.options) > 0:
                col_len = int(math.floor(97 / len(self.options)))

            for i in range(len(self.options)):

                # ENUMERATED
                if self.enum:
                    if i == self.selected_index:
                        h_options += str('>> {}. {} <<'.format(i+1, self.options[i])).center(col_len)
                    else:
                        h_options += str('{}. {}'.format(i+1, self.options[i])).center(col_len)

                # NON ENUMERATED
                else:
                    if i == self.selected_index:
                        h_options += str('>> {} <<'.format(self.options[i])).center(col_len)
                    else:
                        h_options += str('{}'.format(self.options[i])).center(col_len)

            menu += '║' + h_options.center(97) + '║\n'
        # END HORIZONTAL MENU

        # BOTTOM PADDING
        if self.padb > 0:
            for i in range(0, self.padb):
                menu += "║{:^97}║\n".format('')

        # BOTTOM BORDER
        menu += "╚{:=^97}╝".format("")

        return menu

    # =============================================================================================================== #
    # SELECT THE NEXT OPTION ON THE MENU
    def select_next(self):

        # MAKE SURE WE DON'T GO OUT OF RANGE
        if self.loop:
            if self.selected_index + 1 > len(self.options) - 1:
                self.selected_index = 0
            else:
                self.selected_index += 1
        else:
            if self.selected_index + 1 > len(self.options) - 1:
                pass
            else:
                self.selected_index += 1

        return self.get_menu()

    # =============================================================================================================== #
    # SELECT THE PREVIOUS OPTION ON THE MENU
    def select_previous(self):

        # MAKE SURE WE DON'T GO OUT OF RANGE
        if self.loop:
            if self.selected_index - 1 < 0:
                self.selected_index = len(self.options) - 1
            else:
                self.selected_index -= 1
        else:
            if self.selected_index - 1 < 0:
                pass
            else:
                self.selected_index -= 1

        return self.get_menu()


# CONSTANTS WITH PREMADE MENUS USED IN THE GAME
QUIT_MENU = GameMenu(['Yes', 'No', 'Quit to Main Menu'], hmenu=True, padt=8, padb=9, caption='Really Quit?')
MAIN_MENU = GameMenu(['Start', 'Credits', 'Quit'], hmenu=True)
MATCH_TYPE_MENU = GameMenu(['Local Match', 'Online Match'], padt=8, padb=8, caption='Select Match Type')
PLAYER1_HERO_MENU = GameMenu(['New Character', 'Load Character'], padt=8, padb=8, caption='Player 1, select your hero')
PLAYER2_HERO_MENU = GameMenu(['New Character', 'Load Character'], padt=8, padb=8, caption='Player 2, select your hero')
PLAYER1_CONFIRM_HERO_MENU = GameMenu(['Yes', 'No'], hmenu=True, caption='Confirm selection')
PLAYER2_CONFIRM_HERO_MENU = GameMenu(['Yes', 'No'], hmenu=True, caption='Confirm selection')
PRE_COMBAT_MENU = GameMenu(['PRESS <ENTER> TO BEGIN MATCH'], padt=8, padb=9, caption='The Heroes are Ready')
POST_COMBAT_MENU = GameMenu(['PRESS <ENTER> TO CONTINUE'],padt=8, padb=9)
SAVE_CHARACTER_PROMPT = GameMenu(['Yes', 'No'], hmenu=True, padt=8, padb=9, caption='Do you wish to save your character?')
CREDITS = GameMessageFrame(['TEAM Awesome is:','','Omar Silva', 'Mike Sturdy', 'Tim Andrew'], padt=8, padb=7)

if __name__ == '__main__':
    pass
