# Project 5: The Width of a Circle (Part 2)
# othello.py
# By Mithil Hari 84147556
# Contains a class representing the GameState of an
# Othello Game. Also contains 3 Class Exceptions,
# that are relevant to the game rules of Othello.

NONE = 0
BLACK = 1
WHITE = 2

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass


class NoAvailableMovesError(Exception):
    '''Raised whenever a player has no available moves to make'''
    pass


class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass

class GameState:
    def __init__(self, dimensions: [int], first_player: int, topleft_disc: int, win_rule: str):
        self._rows, self._columns = dimensions
        self._turn = first_player
        self._topleft_disc = topleft_disc
        # win_rule is a parameter that determines how the game is won
        # It's values are either '<' or '>'
        self._win_rule = win_rule 
        
        self._board = self._new_game_board()
        self._arrange_center_cells()
        self._black_counter = 2 
        self._white_counter = 2
        # Stores the number of times a turn has been passed
        self._turns_passed = 0

          
    def get_board(self) -> [[int]]:
        '''Returns the game board'''
        return self._board


    def get_num_rows(self) -> int:
        ''' Returns the number of rows of a board'''
        return self._rows


    def get_num_cols(self) -> int:
        '''Returns the number of columns of a board'''
        return self._columns

    
    def turn(self) -> int:
        '''Returns whose turn it is'''    
        return self._turn


    def opposite_turn(self) -> None:
        '''Updates the turn to the next player'''
        if self._turn == WHITE:
            self._turn = BLACK
        else:
            self._turn = WHITE

    
    def winner(self) -> int:
        '''
        Determines the winning player in the given GameState, if any.
        '''
        winner = -1

        if self._win_rule == '>':
            if self._black_counter > self._white_counter:
                winner = BLACK
            elif self._white_counter > self._black_counter:
                winner = WHITE
            else:
                winner = NONE
                    
        else:
            if self._black_counter < self._white_counter:
                winner = BLACK
            elif self._white_counter < self._black_counter:
                winner = WHITE
            else:
                winner = NONE
            
        return winner



    def get_num_black_discs(self) -> int:
        '''Returns the number of black discs on a board'''
        return self._black_counter


    def get_num_white_discs(self) -> int:
        '''Returns the number of white discs on a board'''
        return self._white_counter

    
    def disc_at(self, row_number: int, column_number: int) -> int:
        '''Returns the disc found at the given indices, if any.'''
        if self._is_valid_row_number(row_number) and \
           self._is_valid_column_number(column_number) and \
           self._board[row_number][column_number] != NONE:
            return self._board[row_number][column_number]

        # Return -1 if the disc found is not BLACK or WHITE

        return -1

    
    def require_game_not_over(self) -> None:
        '''
        Raises a GameOverError if the given game state represents a situation
        where the game is over.
        '''
        if self._board_is_full() or self._no_moves_left():
            raise GameOverError()


    def require_available_moves(self) -> None:
        '''
        Given a GameState, checks if there are any legal moves availabe to make on the board.
        If there are no legal moves available to make, the turn is passed onto the next player.
        '''
        available_moves = []
        
        for row in range(self._rows):
            for col in range(self._columns):
                board_cell = self._board[row][col]
                if board_cell == NONE:
                    available_moves.extend(
                        self._find_discs(
                            self._get_interesting_directions(row, col),
                            row, col))
    
        if len(available_moves) == 0:
            self._turns_passed+= 1
            raise NoAvailableMovesError()

 
    def move(self, row_number: int, column_number: int) -> None:
        '''
        Given a row and column to place a disc in, attempts to
        make the move it is valid and if the game is not over yet.
        Raises an InvalidMoveError if it is not.
        '''
        self.require_game_not_over()
        self._require_valid_row_number(row_number)
        self._require_valid_column_number(column_number)
        self._require_empty_cell(row_number, column_number)
        
        interesting_directions = self._get_interesting_directions(
            row_number, column_number)
        discs_to_flip = self._find_discs(interesting_directions,
                                         row_number, column_number)

        # If no discs can be flipped this means that
        # the move is invalid.
        
        if len(discs_to_flip) >  0:

            # Adds a disc for the current player
            # in the location of the desired move.
            
            self._board[row_number][column_number] = self._turn

            # Flips the color of the discs affected
            # by the move.
            
            self._flip_discs(discs_to_flip)
            self._reset_number_of_turns_passed()
            self.opposite_turn()
            self._calc_num_discs()
            
        else:
            raise InvalidMoveError() 


    def _calc_num_discs(self) -> None:
        '''Calculates the number of white and black discs on a board'''
        black_counter = 0
        white_counter = 0
        
        for row in range(self._rows):
            for col in range(self._columns):
                if self._board[row][col] != NONE:
                    if self._board[row][col] == BLACK:
                        black_counter+= 1
                    else:
                        white_counter+= 1
                        

        self._black_counter = black_counter
        self._white_counter = white_counter
        

    def _reset_number_of_turns_passed(self) -> None:
        '''
        Resets the number of turns passed to zero.
        '''
        self._turns_passed = 0

        
    def _flip_discs(self, discs_to_flip: [[int]]) -> None:
        '''
        Changes the color of the discs that can be flipped by the players move.
        '''
        for disc in discs_to_flip:
                row, col = disc
                self._board[row][col] = self._turn


    def _get_interesting_directions(self, initial_row: int, initial_column: int) -> [[int]]:
        '''
        An interesting direction, is one that contains an opponents disc in a cell
        adjacent to the current cell. Returns a list of such directions.
        '''
        interesting_directions = []
        all_directions = [[-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1]]

        for direction in all_directions:
            rdelta, cdelta = direction
            adjacent_row = initial_row + rdelta
            adjacent_column = initial_column + cdelta

            # Get's the value of the disc at the adajcent
            # row and adjacent column. 
            adjacent_cell = self.disc_at(adjacent_row, adjacent_column)

            # If the adjacent cell is equal to the opposite player, consider
            # this direction interesting
            if adjacent_cell != -1 and adjacent_cell != self._turn:
                interesting_directions.append(direction)
    
        return interesting_directions


    def _find_discs(self, directions: [[int]], row_number: int, column_number: int) -> [[int]]:
        '''
        Given the initial disc position and a list of the directions in which
        the other player was found, finds all discs that can be flipped
        by a legal move.
        '''
        discs_to_flip = []
        
        for direction in directions:
            rdelta, cdelta = direction
            next_row = row_number + rdelta 
            next_column = column_number + cdelta
            next_disc = self.disc_at(next_row, next_column)
            potential_discs_to_flip = []
            
            end_of_sequence = False

            # Searches for discs of the opposite color
            # until a disc of the same color is found
            # or if the end of the board is reached
            # in that direction.
            # The end of the sequence has been reached if
            # the next disc looked at is actually an empty
            # cell or if it is not the opponents disc.
            
            while not(end_of_sequence) and next_disc != -1:

                if next_disc != self._turn: 
                    potential_discs_to_flip.append([next_row, next_column])
                else:
                    end_of_sequence = True
                    
                last_disc = self.disc_at(next_row, next_column)
                next_row += rdelta
                next_column += cdelta
                next_disc = self.disc_at(next_row, next_column)
                
            # Only stores the discs found, if the last disc
            # color is equal to the current player.
            # If the move is = B and the sequence found
            # is W->W->(Empty/Off the board), no discs
            # will be flipped. However if the sequence
            # is something like B->W->W->B then the discs found
            # in the sequence will be flipped.
            
            if last_disc == self._turn:
                discs_to_flip.extend(potential_discs_to_flip)
                
        return discs_to_flip


    def _new_game_board(self) -> [[int]]:
        '''
        Creates a new game board. Initially, a game board has the size
        self._rows x self._columns and is comprised of integers with the
        value NONE everywhere except the center of the board. The center
        of the board contains four discs, two white and two black, that
        are arranged according to the specified Othello rule.
        '''
        board = []

        for row in range(self._rows):
            board.append([])
            for col in range(self._columns):
                board[-1].append(NONE)

        return board


    def _arrange_center_cells(self) -> None:
        '''
        Given a game board adds a disc, BLACK or WHITE, to each of
        the four center cells according to the specified arrangement.
        '''
        toprow = int(self._rows/2 - 1)
        botrow = int(self._rows/2)
        leftcol = int(self._columns/2 - 1)
        rightcol = int(self._columns/2)

        if self._topleft_disc != NONE:
            if self._topleft_disc == BLACK:
                self._board[toprow][leftcol] = BLACK
                self._board[toprow][rightcol] = WHITE
                self._board[botrow][leftcol] = WHITE
                self._board[botrow][rightcol] = BLACK
            else:
                self._board[toprow][leftcol] = WHITE
                self._board[toprow][rightcol] = BLACK
                self._board[botrow][leftcol] = BLACK
                self._board[botrow][rightcol] = WHITE


    def _board_is_full(self) -> bool:
        '''Returns True if the board has no empty cells.'''
        for row in self._board:
            if NONE in row:
                return False
            
        return True

            
    def _no_moves_left(self) -> bool:
        '''
        Returns True if both players passed their turn, meaning that
        there are no moves left.
        '''
        return self._turns_passed == 2

                
    def _require_valid_row_number(self, row_number: int) -> None:
        '''Raises an InvalidMoveError if its parameter is not a valid row number'''
        if not(self._is_valid_row_number(row_number)):
            raise InvalidMoveError()
    

    def _require_valid_column_number(self, column_number: int) -> None:
        '''Raises an InvalidMoveError if its parameter is not a valid column number'''
        if not(self._is_valid_column_number(column_number)):
            raise InvalidMoveError()


    def _require_empty_cell(self, row_number: int, column_number: int) -> None:
        '''Raises an InvalidMoveError if its parameter is not an empty cell in the board'''
        if self._board[row_number][column_number] != NONE:
            raise InvalidMoveError()

        
    def _is_valid_row_number(self, row_number: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise'''
        return 0 <= row_number < self._rows


    def _is_valid_column_number(self, column_number: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column_number < self._columns
