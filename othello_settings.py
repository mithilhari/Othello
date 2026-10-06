# Project 5: The Width of a Circle (Part 2)
# othello_settings.py
# By Mithil Hari 84147556
# Contains one Class that represents a Dialog Modal
# used in an Othello GUI application, to determine
# the game settings entered by the user.

import tkinter
import othello

SETTINGS_FONT = ('Charter', 10)

class Dialog:
    def __init__(self, root: tkinter.Tk):
        self._dialog_window = tkinter.Toplevel()
        self._dialog_window.title('Othello Settings | FULL')
        
        # Sets the parent of this window to
        # the initial window displaying the
        # Othelo game GUI.
        self._dialog_window.transient(root)

        # Modals are generally not resizeable.
        self._dialog_window.resizable(width= False, height= False,)

        # The next lines are used to display widgets
        # that allow the user to input information
        # for the game settings.
        # 5 Main Widgets: OptionMenus(2), Buttons(2) and RadioButtons(3)
        # The other widgets are Labels and there
        # a few Control Variables that represent information
        # in these widgets.
        
        row_label = tkinter.Label(
            master = self._dialog_window, text = 'Rows:',
            font = SETTINGS_FONT)
        row_label.grid(
            row = 0, column = 0,
            sticky= tkinter.W)
        
        self._row_var = tkinter.IntVar()
        self._row_var.set(4)
        self._rows_list = tkinter.OptionMenu(
            self._dialog_window,self._row_var,4,6,8,10,12,14,16)
        
        self._rows_list.grid(
            row = 0, column = 1,
            sticky = tkinter.E)

        column_label = tkinter.Label(
            master = self._dialog_window, text = 'Columns:',
            font = SETTINGS_FONT)
        column_label.grid(
            row = 1, column = 0,
            sticky= tkinter.W)

        self._col_var = tkinter.IntVar()
        self._col_var.set(4)
        self._columns_list = tkinter.OptionMenu(
            self._dialog_window,self._col_var,4,6,8,10,12,14,16)        
        self._columns_list.grid(
            row = 1, column = 1,
            sticky = tkinter.E)
        
        player_label = tkinter.Label(
            master = self._dialog_window, text = 'First Player:',
            font = SETTINGS_FONT)
        player_label.grid(
            row = 2, column = 0,
            sticky= tkinter.W)

        self._player_var= tkinter.IntVar()
        
        self._black_radiobutton = tkinter.Radiobutton(
            master = self._dialog_window, text = 'Black',
            variable = self._player_var, value = othello.BLACK)
        self._white_radiobutton = tkinter.Radiobutton(
            master = self._dialog_window, text = 'White',
            variable = self._player_var, value = othello.WHITE)
        
        self._black_radiobutton.grid( row = 2, column = 1,
                                       sticky = tkinter.E)
        self._white_radiobutton.grid( row = 2, column = 2,
                                       sticky = tkinter.E)
           
        arrangement_label = tkinter.Label(
            master = self._dialog_window,
            text = 'What color should the top left disc be? :',
            font = SETTINGS_FONT)
        arrangement_label.grid(
            row = 3, column = 0,
            sticky= tkinter.W)
        
        self._arrangement_var = tkinter.IntVar()
        
        self._black_radiobutton2 = tkinter.Radiobutton(
            master = self._dialog_window, text = 'Black',
            variable = self._arrangement_var, value = othello.BLACK)
        self._white_radiobutton2= tkinter.Radiobutton(
            master = self._dialog_window, text = 'White',
            variable = self._arrangement_var, value = othello.WHITE)
        
        self._black_radiobutton2.grid( row = 3, column = 1,
                                       sticky = tkinter.E)
        self._white_radiobutton2.grid( row = 3, column = 2,
                                       sticky = tkinter.E)       
        
        winner_label = tkinter.Label(
            master = self._dialog_window,
            text = 'How many discs should the winner have?:',
            font = SETTINGS_FONT)
        winner_label.grid(
            row = 4, column = 0,
            sticky= tkinter.W)

        self._win_var = tkinter.StringVar()
        self._win_var.set(' ')
        self._win_radiobutton1 = tkinter.Radiobutton(
            master = self._dialog_window, text = 'Most\nDiscs',
            variable = self._win_var, value = '>')
        self._win_radiobutton2= tkinter.Radiobutton(
            master = self._dialog_window, text = 'Least\nDiscs',
            variable = self._win_var, value = '<')
        
        self._win_radiobutton1.grid( row = 4, column = 1,
                                       sticky = tkinter.E)
        self._win_radiobutton2.grid( row = 4, column = 2,
                                       sticky = tkinter.E) 
        
        button_frame = tkinter.Frame(master = self._dialog_window)
        button_frame.grid(
            row = 5, column = 0, columnspan = 3,
            sticky = tkinter.E + tkinter.S)
        
        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = SETTINGS_FONT,
            command = self._on_ok_button)
        ok_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        quit_button = tkinter.Button(
            master = button_frame, text = 'QUIT', font = SETTINGS_FONT,
            command = self._on_quit_button,
            anchor = tkinter.E)
        quit_button.grid(row = 0, column = 2, padx = 10, pady = 10)

        self._ok_clicked = False
        self._rows = 4
        self._cols = 4
        self._first_player = 0
        self._topleft_disc = 0
        self._win_condition = ' '

        # Initializes game settings to an empty board.
        # This empty board will show in the background
        # before the user has entered their custom 
        # settings.
        
        self._state = othello.GameState([self._rows, self._cols],
                                        self._first_player,
                                        self._topleft_disc,
                                        self._win_condition)

    
    def show(self) -> None:
        '''Shows the game settings Dialog Modal'''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()
        

    def was_ok_clicked(self) -> bool:
        '''Returns True if the 'OK' button was clicked'''
        return self._ok_clicked


    def get_game(self) -> othello.GameState:
        '''Returns the Othello GameState created from the settings.'''
        return self._state   


    def _on_ok_button(self) -> None:
        '''
        When the 'OK' button is pressed, stores the information
        (if entered) and creates a game with the custom settings.
        '''
        self._rows = self._row_var.get()
        self._cols = self._col_var.get()
        self._first_player = self._player_var.get()
        self._topleft_disc = self._arrangement_var.get()
        self._win_condition = self._win_var.get()
    
        self._state = othello.GameState([self._rows, self._cols],
                                        self._first_player,
                                        self._topleft_disc,
                                        self._win_condition)
        
        settings = [self._rows, self._cols, self._first_player,
                   self._topleft_disc, self._win_condition]
        self._check_settings(settings)


    def _check_settings(self, settings: [int,str]) -> None:
        '''
        If the settings for the game entered by the user are no different
        from the default values, they have not entered valid input.
        '''

        if 0 in settings or ' ' in settings:
            tkinter.messagebox.showinfo(
                                'Othello | FULL', 'Invalid Input.')
            self._ok_clicked = False
        else:
            # If the settings are fine then the
            # window disappears
            self._ok_clicked = True
            self._dialog_window.destroy()


    def _on_quit_button(self) -> None:
        '''Quits the Dialog Modal if the 'QUIT' button is pressed.'''
        self._dialog_window.destroy()

