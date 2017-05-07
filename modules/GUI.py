from tkinter import *
import random


# ============================================================================================================= #
# THIS IS THE MAIN GUI CLASS FROM WHICH THE MAIN GAME CLASS IS DERIVED
class GUI(Tk):

    # ============================================================================================================= #
    # CLASS CONSTRUCTOR
    def __init__(self):
        Tk.__init__(self)

        self.title("Heroes of Pyth")
        self.geometry('800x358')
        self.resizable(0, 0)

        # BINDINGS
        self.bind("<Key>", self.keypress)
        self.bind("<Left>", self.on_left)
        self.bind("<Up>", self.on_up)
        self.bind("<Right>", self.on_right)
        self.bind("<Down>", self.on_down)
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_esc)

        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1)

        # TEXT BOX
        self.display = Text(self.main_frame)
        self.display.pack(fill=BOTH, expand=1)
        self.display.configure(state="disabled")

    # ============================================================================================================= #
    # THIS WILL UPDATE THE MAIN TEXT WIDGET WITH ALL THE INFORMATION THAT WE WANT TO SHOW ON THE SCREEN
    def wprint(self, string):
        self.display.configure(state="normal")

        # RESIZE TEXT BOX ACCORDINGLY
        h = string.count('\n')
        if h <= 20:
            h = 20

        self.display.configure(height=h + 1)

        # UPDATE THE TEXT BOX WITH NEW CONTENT
        self.display.delete('1.0', END)
        self.display.insert('1.0', string)
        self.display.configure(state="disabled")


    def keypress(self, event):
        pass

    def on_up(self, event):
        pass

    def on_down(self, event):
        pass

    def on_left(self, event):
        pass

    def on_right(self, event):
        pass

    def on_return(self, event):
        pass

    def on_esc(self, event):
        pass

    def hero_create_on_ok(self):
        pass

    def hero_create_on_cancel(self):
        pass


# ============================================================================================================= #
# THIS FRAME CONTAINS FORMS USED TO CREATE A HERO FROM SCRATCH,
# IT INCLUDES FIELDS FOR HERO NAME AND HERO SEED
class HeroCreateFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self)

        self.parent = parent
        self.configure(padx=275, bg='white')

        # CAPTION WIDGET
        self.caption = Label(self, text='TYPE NAME AND SEED\nPress <ENTER> to continue', bg='white', font=('Courier', 9))
        self.caption.pack(fill=X, pady=(100,0))

        # LABEL WIDGET
        self.label1 = Label(self, text='Name', bg='white', width=6, padx=4, justify=RIGHT, font=('Courier', 9))
        self.label1.pack(fill=X)

        # NAME ENTRY WIDGET
        self.name_entry = Entry(self, relief=SOLID, font=('Courier', 9))
        self.name_entry.pack(fill=X, pady=(0, 4))

        # RANDOM NAME BUTTON WIDGET
        self.random_name = Button(self, text='Random Name',
                                  command=self.get_random_name,
                                  relief=SOLID, bg='white',
                                  borderwidth=1, height=0,
                                  width=12, font=('Courier', 9))

        self.random_name.pack()

        # LABEL WIDGET
        self.label2 = Label(self, text='Seed', bg='white', width=6, padx=4, justify=RIGHT, font=('Courier', 9))
        self.label2.pack(fill=X)

        # SEED ENTRY WIDGET
        self.seed_entry = Entry(self, relief=SOLID, font=('Courier', 9))
        self.seed_entry.pack(fill=X)

    # ============================================================================================================= #
    # GET RANDOM NAME FROM FILES AND INSERT IT IN THE NAME ENTRY WIDGET
    def get_random_name(self):

        name_list = []
        hero_name = ''

        # MAIN HERO NAME
        with open('resources/dictionary.names.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                name_list.append(line.strip())

        hero_name += name_list[random.randrange(0, len(name_list))]

        # HERO TITLE
        with open('resources/dictionary.titles.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                name_list.append(line.strip())

        hero_name += " " + name_list[random.randrange(0, len(name_list))]

        self.name_entry.delete(0, END)
        self.name_entry.insert(0, hero_name)


if __name__ == '__main__':
    root = GUI()
    root.mainloop()
