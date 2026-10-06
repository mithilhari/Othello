# Project 5: The Width of a Circle (Part 2)
# othello_gui.py
# By Mithil Hari 84147556
# This module implements game logic from Othello in a tkinter based
# GUI Othello Application.
# The application begins with an empty 4x4 Othello gameboard.
# Clicking on the canvas causes an attempted  move on this gameboard
# A black or white disc will be drawn on the canvas in its respective
# grid cell, or a message will be displayed telling the player information
# about their move. When the canvas is resized, the gameboard displayed
# adjusts accordingly.

import tkinter
import othello
import othello_settings

SIZE = 50
DEFAULT_FONT = ('Comic Sans', 24)
BUTTON_FONT = ('Comic Sans', 18)

class OthelloApplication:
    def __init__(self):
        '''Initiailizes a new Othello Application'''
        self._root = tkinter.Tk()
        self._root.title('Othello | FULL')

        # Stores an object of the Dialog Modal for game settings
        self._dialog = othello_settings.Dialog(self._root)

        # The following lines contain information required
        # to display an updating scoreboard.
        self._score_text = tkinter.StringVar()
        self._score_text.set('Black: {}  White: {}'.format(0,0))
                            
        self._score_label = tkinter.Label(
            master = self._root, textvariable = self._score_text,
            anchor = tkinter.CENTER, font = BUTTON_FONT)
        self._score_label.grid(
            row = 0, column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        # The following lines contain information required
        # to display the current player.
        # (when the game ends this label displays the winner)
        self._turn_text = tkinter.StringVar()
        self._turn_text.set('Turn:')
        
        self._turn_label = tkinter.Label(
            master = self._root, textvariable = self._turn_text,
            anchor = tkinter.CENTER, font = BUTTON_FONT)
        self._turn_label.grid(
            row = 2, column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                        
        self._canvas = tkinter.Canvas(master = self._root, background = 'green',
                                      relief = tkinter.RAISED, bd = 5,
                                      bg = 'green', height = 300, width = 200)
        self._canvas.grid(row = 1, column = 0,

                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<ButtonRelease-1>', self._on_click_release)
        
        # Determines the proportions for resizing
        # the Canvas Widget in the root window.
        self._root.rowconfigure(1, weight = 1)
        self._root.columnconfigure(0, weight = 1)
        
        
    def run(self) -> None:
        '''
        Shows the settings Dialog Modal and runs the mainloop,
        after storing information entered in the Modal.
        '''    
        self._dialog.show()
        if self._dialog.was_ok_clicked():
            state = self._dialog.get_game()

            # Initial size of the canvas.
            # Height = Rows * 50 pixels * 1.5
            # Width  = Columns * 50 pixels * 1.5
            # Multiplied by 1.5 to adjust
            # for the row and column configure 1:1 ratio
            self._canvas.configure(height= state.get_num_rows() * SIZE,
                                   width = state.get_num_cols() * SIZE)

            self._update_turn_label(state)
            self._redraw_gameboard(state)
            self._root.mainloop()
        else:
            self._root.destroy()

    
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Redraws the gameboard if the canvas is changed.'''
        self._redraw_gameboard(self._dialog.get_game())


    def _redraw_gameboard(self, state: othello.GameState) -> None:
        '''
        Redraws each grid cell and the respective disc (if)
        contained in the cell. Every disc and cell stores
        a tag reprsenting the row and column number they
        are located in on the Othello GameState board.
        This information will be used to identify what
        the user has clicked later.
        '''
        self._canvas.delete(tkinter.ALL)
        # A dictionary for each disc's (fill, outline)
        disc_color= {othello.BLACK: ('black','white'),
                     othello.WHITE:('white','black')}

        rows = state.get_num_rows()
        cols = state.get_num_cols()
        
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        # Sets cell width and cell height to be drawn
        cell_width = canvas_width / cols
        cell_height = canvas_height / rows
        board = state.get_board()

        # For every cell in the board, draws a rectangle
        # representing the grid cell and an oval
        # representing the cell's disc if any
        for row in range(rows):
            for col in range(cols):
                self._canvas.create_rectangle(
                    col * (cell_width), row * (cell_height),
                    (col + 1)*(cell_width), (row + 1)*(cell_height),
                    fill = "green", width = 2,
                    tags = (row,col))
                cell = board[row][col]
                # If the cell has a disc, fills it in.
                if cell != othello.NONE:

                    # Creates an oval that fills up 0.9
                    # or 90% of the cell drawn
                    self._canvas.create_oval(
                            (col + 0.1) * (cell_width),
                            (row + 0.1) * (cell_height),
                            (col + 0.9) * (cell_width),
                            (row + 0.9) * (cell_height),
                            fill = disc_color[cell][0],
                            outline = disc_color[cell][1],
                            width = 2, tags = (row,col))


    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''
        When the canvas is clicked, this method will locate where
        the it was clicked and attempt to make a move there.
        '''

        state = self._dialog.get_game()

        # Gets the closest item in the Canvas Widget
        # which is either a grid cell or a disc
        item = self._canvas.find_closest(event.x, event.y)

        # Stores the item's tag value as a row and column index
        tags = self._canvas.gettags(item)
        row, column = tags[0:2]
        try:
            state.move(int(row), int(column))
            self._redraw_gameboard(state)
            self._update_score_label(state)
            self._update_turn_label(state)
        except othello.GameOverError:
            winner = state.winner()
            self._show_winner(winner)
        except othello.InvalidMoveError:
            tkinter.messagebox.showinfo(
                'Othello | FULL', 'Invalid Move. Please try again.')

                            
    def _on_click_release(self, event: tkinter.Event) -> None:
        '''
        When the Left Button is released this method will
        call methods required to handle the end of the turn,
        by either ending the game or passing the turn(s).
        '''
        

        state = self._dialog.get_game()
        try:
            state.require_game_not_over()
            state.require_available_moves()
        except othello.GameOverError:
                winner = state.winner()
                self._show_winner(winner)
        except othello.NoAvailableMovesError:
            self._update_turn_label(state)
            tkinter.messagebox.showinfo(
                'Othello | FULL', '{} passes their turn.'.format(self._turn))
            state.opposite_turn()
            self._update_turn_label(state)

            # Handles the case where a turn is passed,
            # but the next player can not make a move.
            # The message box is used here in order
            # to make it easier for the player to understand.
            # Calls a method to show the winner at the end.
            try:
                state.require_available_moves()
            except othello.NoAvailableMovesError:
                tkinter.messagebox.showinfo(
                    'Othello | FULL', '{} passes their turn.'.format(self._turn))
                winner = state.winner()
                self._show_winner(winner)
            
            

    def _update_score_label(self, state: othello.GameState) -> None:
        '''
        Updates the control variable for the score label to the current score.
        '''
        self._score_text.set('Black: {}  White: {}'.format(
                    state.get_num_black_discs(),
                    state.get_num_white_discs()))

    
    def _update_turn_label(self, state: othello.GameState) -> None:
        '''
        Updates the control variable for the turn label to the current turn.
        '''
        if state.turn() == othello.BLACK:
            self._turn = 'Black'
        else:
            self._turn = 'White'
        self._turn_text.set("Turn: {}'s Turn".format(self._turn))


    def _show_winner(self, winner: int) -> None:
        '''
        Shows the winner of the game by setting a control variable's value
        to the winner.
        '''
        if winner == othello.BLACK:
            self._turn_text.set('Black Wins!')
        elif winner == othello.WHITE:
            self._turn_text.set('White Wins!')
        else:
            self._turn_text.set('Tie game -_-')
    

if __name__ == '__main__':
    OthelloApplication().run()
