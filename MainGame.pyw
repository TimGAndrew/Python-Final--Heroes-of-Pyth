from modules.Hero import *
from modules.Combat import *
from modules.Display import Display
from modules.GameMenu import *
from modules.GUI import *
import tkinter.messagebox
import tkinter.filedialog as fd
import os

GAME_PATH = os.path.dirname(__file__)


# PLAYER ENUMERATION
class Player:
    ONE = 1
    TWO = 2


# ============================================================================================================= #
# MainGame CLASS
class MainGame (GUI):

    # EMPTY VARIABLES FOR LATER USE
    player1 = None                          # PLAYER ONE
    player2 = None                          # PLAYER TWO
    hero_create_frame = None                # PLACEHOLDER FOR HERO CREATE FRAME
    previous_state = None                   # SAVE PREVIOUS STATE BEFORE SHOWING QUIT MENU
    previous_menu = None                    # SAVE PREVIOUS MENU BEFORE SHOWING QUIT MENU
    combat = None

    # CLASS CONSTRUCTOR
    def __init__(self):
        GUI.__init__(self)

        self.state = 'game_start'                       # STATE HANDLES THE FLOW OF THE GAME
        self.current_menu = MAIN_MENU                   # THE CURRENT MENU BEING DISPLAYED ON THE SCREEN


        # START GAME...
        self.handle_state()

    # ============================================================================================================= #
    # LEFT ARROW PRESSED
    def on_left(self, event):

        # SELECT PREVIOUS MENU OPTION (IF HORIZONTAL MENU)
        if self.current_menu.hmenu:
            self.current_menu.select_previous()
            self.handle_state()

    # ============================================================================================================= #
    # RIGHT ARROW PRESSED
    def on_right(self, event):

        # SELECT NEXT MENU OPTION (IF HORIZONTAL MENU)
        if self.current_menu.hmenu:
            self.current_menu.select_next()
            self.handle_state()

    # ============================================================================================================= #
    # UP ARROW PRESSED
    def on_up(self, event):

        # SELECT PREVIOUS MENU OPTION (IF VERTICAL MENU)
        if self.current_menu.hmenu is False:
            self.current_menu.select_previous()
            self.handle_state()

    # ============================================================================================================= #
    # DOWN ARROW PRESSED
    def on_down(self, event):

        # SELECT NEXT MENU OPTION (IF VERTICAL MENU)
        if self.current_menu.hmenu is False:
            self.current_menu.select_next()
            self.handle_state()

    # ============================================================================================================= #
    # ESCAPE PRESSED
    def on_esc(self, event):

        # SHOW QUIT MENU...

        # IF ALREADY ON QUIT MENU, IGNORE
        if self.current_menu == QUIT_MENU:
            return

        self.previous_state = self.state
        self.previous_menu = self.current_menu
        self.state = 'quit_menu'
        self.current_menu = QUIT_MENU

        if self.hero_create_frame is not None:
            self.hero_create_frame.pack_forget()
            self.main_frame.pack(fill=BOTH, expand=1)

        self.handle_state()

    # ============================================================================================================= #
    # RETURN KEY (ENTER) HAS BEEN PRESSED
    # MANAGES RESPONSES TO THE ENTER KEY BEING PRESSED BASED ON MENU CONTEXT
    def on_return(self, event):

        # PLAYER PRESSED ENTER AT THE START SCREEN
        if self.state == 'game_start':

            if self.current_menu.selected_index == 0:
                self.state = 'match_type_select'
                self.current_menu = MATCH_TYPE_MENU
                self.handle_state()

            elif self.current_menu.selected_index == 1:
                self.state = 'credit_screen'
                self.current_menu = CREDITS
                self.handle_state()

            elif self.current_menu.selected_index == 2:
                self.quit()

        # ---------------------------------------------

        # PLAYER PRESSED ENTER AT THE CREDIT SCREEN
        elif self.state == 'credit_screen':
            self.state = 'game_start'
            self.current_menu = MAIN_MENU
            self.handle_state()

        # PLAYER PRESSED ENTER DURING QUIT MENU
        elif self.state == 'quit_menu':
            self.quit_menu()

        # ---------------------------------------------

        # PLAYER PRESSED ENTER DURING MATCH TYPE SELECTION
        elif self.state == 'match_type_select':
            if self.current_menu.selected_index == 0:     # LOCAL MATCH
                self.state = 'player1_hero_select'
                self.current_menu = PLAYER1_HERO_MENU
                self.handle_state()
            else:                                           # ONLINE MATCH (NOT WORKING ATM)
                pass
        # ---------------------------------------------

        # PLAYER 1 PRESSED ENTER DURING PLAYER 1 HERO SELECTION SCREEN
        elif self.state == 'player1_hero_select':
            self.player_hero_select(Player.ONE)

        # ---------------------------------------------

        # PLAYER 1 PRESSED ENTER DURING PLAYER 1 HERO CONFIRMATION SCREEN
        elif self.state == 'player1_confirm_hero_selection':
            self.confirm_hero_selection(Player.ONE)
        # ---------------------------------------------

        # PLAYER 2 PRESSED ENTER DURING PLAYER 2 HERO SELECTION SCREEN
        elif self.state == 'player2_hero_select':
            self.player_hero_select(Player.TWO)
        # ---------------------------------------------

        # PLAYER 2 PRESSED ENTER DURING PLAYER 2 HERO CONFIRMATION SCREEN
        elif self.state == 'player2_confirm_hero_selection':
            self.confirm_hero_selection(Player.TWO)
        # ---------------------------------------------

        # PLAYER PRESSED ENTER DURING PRE MATCH SCREEN
        elif self.state == 'pre_match':
            self.state = 'combat'
            self.combat = Combat(self.player1, self.player2)
            self.current_menu = GameMenu(self.combat.get_attacker().moves, hmenu=True)
            self.handle_state()

        # PLAYER PRESSES ENTER DURING COMBAT
        elif self.state == 'combat':
            self.handle_combat_options(self.current_menu.selected_index)

        # PLAYER PRESSES ENTER DURING POST MATCH SCREEN
        elif self.state == 'match_over':
            self.state = 'post_match_screen'
            self.current_menu = POST_COMBAT_MENU
            self.current_menu.caption = 'Congratulations {}! You\'re the Winner!'.format(self.combat.winner.name)
            self.handle_state()

        elif self.state == 'post_match_screen':
            self.state = 'character_save_prompt'
            self.current_menu = SAVE_CHARACTER_PROMPT
            self.handle_state()

        # PLAYER PRESSES ENTER DURING CHARACTER SAVE PROMPT
        elif self.state == 'character_save_prompt':

            # PLAYER CHOOSES TO SAVE CHARACTER
            if self.current_menu.selected_index == 0:
                self.handle_character_save()
                self.reset()

            else:
                # PLAYER CHOOSES NOT TO SAVE, RESET EVERYTHING AND GO BACK TO MAIN MENU
                self.reset()

    # ============================================================================================================= #
    # PROMPTS THE PLAYER TO SELECT A METHOD FOR HERO CREATION
    def player_hero_select(self, player):

        # CREATE A CHARACTER USING THE CREATE DIALOG
        if self.current_menu.selected_index == 0:

            # DISPLAY HERO SELECTION FRAME IF NONE EXIST
            if self.hero_create_frame is None:
                self.main_frame.pack_forget()
                self.hero_create_frame = HeroCreateFrame(self)
                self.hero_create_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
                self.hero_create_frame.name_entry.focus()

            # IF ON HERO SELECTION FRAME ACCEPT SELECTION AND GET VALUES FROM THE TEXT INPUT
            else:
                name = self.hero_create_frame.name_entry.get()
                seed = self.hero_create_frame.seed_entry.get()

                if name == '':
                    tkinter.messagebox.showwarning('No name entered', 'You need to enter a name!')
                    pass
                elif seed == '':
                    tkinter.messagebox.showwarning('No seed entered', 'You need to enter a seed!')
                    pass
                else:

                    hero = Hero(name, seed)
                    if player == Player.ONE:
                        self.player1 = hero
                        self.state = 'player1_confirm_hero_selection'
                        self.current_menu = PLAYER1_CONFIRM_HERO_MENU
                        self.current_menu.caption = 'Confirm selection for seed: {}'.format(self.player1.seed)

                    else:

                        self.player2 = hero
                        self.state = 'player2_confirm_hero_selection'
                        self.current_menu = PLAYER2_CONFIRM_HERO_MENU
                        self.current_menu.caption = 'Confirm selection for seed: {}'.format(self.player2.seed)

                    self.hero_create_frame.destroy()
                    self.main_frame.pack(fill=BOTH, expand=1)
                    self.hero_create_frame = None
                    self.handle_state()

        # LOAD CHARACTER FROM FILE
        else:

            # SHOW OPEN FILE DIALOG
            file_name = fd.askopenfilename(filetypes=(('Hero File', '*.hero'),))

            # MAKE SURE FILE NAME IS NOT BLANK
            if file_name is not '':

                # LOAD FILE FOR PLAYER ONE
                if player == Player.ONE:

                    self.player1 = Hero.load(file_name)
                    if self.player1 is None:
                        tkinter.messagebox.showwarning('Error loading file', 'The file is corrupt.')
                        return

                    self.state = 'player1_confirm_hero_selection'
                    self.current_menu = PLAYER1_CONFIRM_HERO_MENU

                # LOAD FILE FOR PLAYER TWO
                else:

                    self.player2 = Hero.load(file_name)
                    if self.player2 is None:
                        tkinter.messagebox.showwarning('Error loading file', 'The file is corrupt.')
                        return

                    self.state = 'player2_confirm_hero_selection'
                    self.current_menu = PLAYER2_CONFIRM_HERO_MENU

                self.handle_state()

    # ============================================================================================================= #
    # PROMPTS THE PLAYER TO CONFIRM HERO SELECTION
    def confirm_hero_selection(self, player):

        # SELECTION CONFIRMED
        if self.current_menu.selected_index == 0:

            # NEXT PLAYER'S TURN
            if player == Player.ONE:
                self.state = 'player2_hero_select'
                self.current_menu = PLAYER2_HERO_MENU
                self.handle_state()

            # PLAYER 2 ALREADY CHOSE SO BEGIN MATCH
            else:
                self.state = 'pre_match'
                self.current_menu = PRE_COMBAT_MENU
                self.handle_state()

        # SELECTION DENIED
        elif self.current_menu.selected_index == 1:

            # RESET SOME STUFF AND PRESENT PLAYER WITH SELECTION SCREEN ONCE AGAIN
            # ...FOR PLAYER 1
            if player == Player.ONE:
                self.player1 = None
                self.state = 'player1_hero_select'
                self.current_menu = PLAYER1_HERO_MENU
                self.handle_state()

            # ...PLAYER 2
            else:
                self.player1 = None
                self.state = 'player2_hero_select'
                self.current_menu = PLAYER2_HERO_MENU
                self.handle_state()

    # ============================================================================================================= #
    # PROMPTS PLAYER TO CHOOSE AN OPTION FROM THE QUIT MENU
    def quit_menu(self):

        # QUIT THE GAME
        if self.current_menu.selected_index == 0:
            self.quit()

        # DO NOT QUIT
        elif self.current_menu.selected_index == 1:
            self.state = self.previous_state
            self.current_menu = self.previous_menu

            if self.hero_create_frame is not None:
                self.main_frame.pack_forget()
                self.hero_create_frame.pack(fill=BOTH, expand=1)

            self.handle_state()

        # QUIT TO MAIN MENU
        elif self.current_menu.selected_index == 2:  # QUIT TO MAIN MENU
            self.reset()

    # ============================================================================================================= #
    # HANDLES CURRENT STATE, AND DISPLAYS THE APPROPRIATE MENU BASED ON THE CURRENT STATE
    def handle_state(self):

        if self.state == 'game_start':
            self.wprint(Display.draw_title_screen() + self.current_menu.get_menu())

        elif self.state == 'credit_screen':
            self.wprint(self.current_menu.get_frame())

        elif self.state == 'quit_menu':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'match_type_select':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'player1_hero_select':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'player1_confirm_hero_selection':
            self.wprint(Display.draw_character_sheet(self.player1) + self.current_menu.get_menu())

        elif self.state == 'player2_hero_select':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'player2_confirm_hero_selection':
            self.wprint(Display.draw_character_sheet(self.player2) + self.current_menu.get_menu())

        elif self.state == 'pre_match':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'combat':
            self.handle_combat()

        elif self.state == 'post_match_screen':
            self.wprint(self.current_menu.get_menu())

        elif self.state == 'character_save_prompt':
            self.wprint(self.current_menu.get_menu())

    # ============================================================================================================= #
    # HANDLES THE COMBAT SCREEN AND DISPLAYS THE CHARACTER SHEETS ON THE SCREEN AS WELL AS THE COMBAT OPTIONS
    # FOR EACH HERO
    def handle_combat(self):
        combat_screen = Display.draw_combat_sheet(self.player1, self.player2, self.combat) + '\n'
        self.wprint(combat_screen + self.current_menu.get_menu())

    # ============================================================================================================= #
    # HANDLE CURRENT STATE
    def handle_combat_options(self, option):

        # CHECKS TO SEE IF MATCH IS OVER (OTHER PLAYER DIED)...

        # MATCH ISN'T OVER SO GET THE COMBAT OPTIONS FOR THE NEXT PLAYER
        if self.combat.resolve_combat(option) is False:
            self.current_menu = GameMenu(self.combat.get_attacker().moves, hmenu=True)
            self.handle_combat()

        # MATCH OVER, CHANGE STATE AND DISPLAY POST-MATCH SCREEN
        else:
            self.state = 'match_over'
            combat_screen = Display.draw_combat_sheet(self.player1, self.player2, self.combat) + '\n'
            self.current_menu = GameMenu(['Match over, press <ENTER> to continue...'], hmenu=True)
            self.wprint(combat_screen + self.current_menu.get_menu())

    # ============================================================================================================= #
    # HANDLE CHARACTER SAVING IF THE PLAYER WISHES TO DO SO AT THE END OF THE MATCH
    def handle_character_save(self):

        # RESET HERO's HP AND MP BEFORE SAVING
        self.combat.winner.stats['HP'] = self.combat.winner.stats['HP_MAX']
        self.combat.winner.stats['MP'] = self.combat.winner.stats['MP_MAX']

        # SHOW SAVE FILE DIALOG
        file_name = fd.asksaveasfilename(initialfile=self.combat.winner.name,
                                         defaultextension=".hero",
                                         filetypes=(('Hero File', '*.hero'),))

        # SAVE HERO TO FILE
        Hero.save(self.combat.winner, file_name)

    # ============================================================================================================= #
    # RESET THE GAME TO ORIGINAL STATE AND DISPLAY THE MAIN MENU
    def reset(self):
        # RESET SOME STUFF
        self.hero_create_frame = None
        self.player1 = None
        self.player2 = None
        self.state = 'game_start'
        self.current_menu = MAIN_MENU
        self.combat = None
        self.handle_state()

if __name__ == '__main__':
    game = MainGame()
    game.mainloop()
