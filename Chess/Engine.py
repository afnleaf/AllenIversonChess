"""
Stores all the info about the current game state.
Determines valid moves at that state.
Logs moves.
"""
import numpy as np


class GameState():

    def __init__(self):
        # consider numpy arrays for increased AI speed
        # 8x8 2D list
        # each element has two characters
        # w is white, b is black, 2nd char is the piece type:
        # P Pawn, N Knight, B Bishop, R Rook, Q Queen, K King, -- empty 
        self.board = np.array([
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ])

        # dictionary that works kind of like a switch statement
        self.move_functions = {
            'P': self.get_pawn_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'R': self.get_rook_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }

        # game state variables and flags
        self.turn_counter = 1
        self.num_pieces_left = 32
        # white always moves first
        self.white_to_move = True
        self.move_log = []
        # keep track of king's location for efficiency
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        # game end state
        self.checkmate = False
        self.stalemate = False
        # for castling
        self.curr_castling_rights = CastlingRights(True, True, True, True)
        # copying the values to a new object
        self.castling_rights_log = [CastlingRights(self.curr_castling_rights.wks, 
                                                 self.curr_castling_rights.bks, 
                                                 self.curr_castling_rights.wqs, 
                                                 self.curr_castling_rights.bqs)]
        
    
    # take a move and execute it
    def make_move(self, move):
        # moves the piece, leaving empty square behind
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = '--'
        
        # remove piece from the board
        if move.piece_captured[0] == 'b' or move.piece_captured[0] == 'w':
            self.num_pieces_left -= 1

        # update king's location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        # defaulting to just queen for now
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
        # TODO: add piece choice pawn promotion

        # castling
        # move rook into new square
        # remove from old square
        if move.is_castle_move:
            # kingside
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = '--'
            # queenside
            else:
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = '--'

        # update castling rights, rook/king move
        self.update_castling_rights(move)
        self.castling_rights_log.append(CastlingRights(
            self.curr_castling_rights.wks, 
            self.curr_castling_rights.bks, 
            self.curr_castling_rights.wqs, 
            self.curr_castling_rights.bqs
        ))

        # log the move to undo it later
        self.move_log.append(move)
        # update turn counter
        self.turn_counter += 1
        # switch turns
        self.white_to_move = not self.white_to_move
        

    # undo last move made
    def undo_move(self):
        # check if at least 1 move has been made
        if len(self.move_log) != 0:
            # remove last element in list
            move = self.move_log.pop()

            # remove piece from the board
            if move.piece_captured[0] == 'b' or move.piece_captured[0] == 'w':
                self.num_pieces_left += 1

            # return piece
            self.board[move.start_row][move.start_col] = move.piece_moved
            # return captured piece
            self.board[move.end_row][move.end_col] = move.piece_captured
            
            # undo the update to king's location
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

            # undo castling rights, remove last
            self.castling_rights_log.pop()
            newRights = self.castling_rights_log[-1]
            self.curr_castling_rights = CastlingRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo the castle
            # remove from new location, put back into old location
            if move.is_castle_move:
                # kingside
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                # queenside
                else:
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'
           
            # for ai
            self.checkmate = False
            self.stalemate = False
            # update turn counter
            self.turn_counter -= 1
            # switch turns
            self.white_to_move = not self.white_to_move


    def update_castling_rights(self, move):
        # Update castling rights based on the move
        piece = move.piece_moved
        captured_piece = move.piece_captured
        start_row, start_col = move.start_row, move.start_col
        end_row, end_col = move.end_row, move.end_col

        if piece == 'wK':
            self.curr_castling_rights.wks = False
            self.curr_castling_rights.wqs = False
        elif piece == 'bK':
            self.curr_castling_rights.bks = False
            self.curr_castling_rights.bqs = False
        # for rook, check if its left or right
        elif piece == 'wR':
            if start_row == 7:
                if start_col == 0:
                    self.curr_castling_rights.wqs = False
                elif start_col == 7:
                    self.curr_castling_rights.wks = False
        elif piece == 'bR':
            if start_row == 0:
                if start_col == 0:
                    self.curr_castling_rights.bqs = False
                elif start_col == 7:
                    self.curr_castling_rights.bks = False
        
        # check if the rook was captured
        if captured_piece == 'wR':
            if end_row == 7:
                if end_col == 0:
                    self.curr_castling_rights.wqs = False
                elif end_col == 7:
                    self.curr_castling_rights.wks = False
        elif captured_piece == 'bR':
            if end_row == 0:
                if end_col == 0:
                    self.curr_castling_rights.bqs = False
                elif end_col == 7:
                    self.curr_castling_rights.bks = False




    # print the move log to console
    def print_move_log(self):
        print("Move log:")
        i = 1
        for move in self.move_log:
            print(str(i) + ". " + move.get_chess_notation())
            i += 1


    # all moves considering checks
    # ex pawn cant move if the pawn is pinned to a check by an opposing piece
    # player cant put themselves in check
    def get_valid_moves(self):
        # temp castling rights to avoid all the possible changes
        temp_castling_rights = CastlingRights(self.curr_castling_rights.wks,
                                            self.curr_castling_rights.bks,
                                            self.curr_castling_rights.wqs,
                                            self.curr_castling_rights.bqs)
        
        # generate all possible moves whether they are valid or not
        moves = self.get_all_possible_moves()
        # get the castling movess
        if self.white_to_move:
            self.get_castling_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castling_moves(self.black_king_location[0], self.black_king_location[1], moves)
        
        # make each move
        # move through the list backwards
        for i in range(len(moves)-1, -1 , -1):
            self.make_move(moves[i])
            # we need to switch back after we do make_move()
            self.white_to_move = not self.white_to_move
            # gen all opp's moves, see if they attack your king
            if self.in_check():
                # if the move puts us in check, we need to remove that move from the list of valid moves
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        
        # checking for checkmate or stalemate
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.curr_castling_rights = temp_castling_rights

        return moves
    
    # determine if current player is in check
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])


    # determine if they enemy can attack the square at row, col
    def square_under_attack(self, row, col):
        # switch to the opposite turn
        self.white_to_move = not self.white_to_move
        # get all possible moves for the opposite side
        opp_moves = self.get_all_possible_moves()
        # switch back to the current turn
        self.white_to_move = not self.white_to_move
        # check if any of the opposite side's moves attack the square
        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False


    # all moves without considering checks
    # consider all moves that are possible based on how a piece is legally allowed to move
    """
    def get_all_possible_moves(self):
        # moves = [Move((6,4), (4,4), self.board)]
        moves = []
        # check all pieces on our board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # find the colour of the piece
                turn = self.board[row][col][0]
                if(turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    # get the piece type
                    piece = self.board[row][col][1]
                    # calls the appropriate move function based on the piece type
                    self.move_functions[piece](row, col, moves)
        return moves
    """

    def get_all_possible_moves(self):
        moves = []
        for row, row_squares in enumerate(self.board):
            for col, square in enumerate(row_squares):
                if self.is_valid_piece(square):
                    self.add_moves_for_piece(row, col, moves)
        return moves

    def is_valid_piece(self, square):
        return bool(square) and (square[0] == 'w') == self.white_to_move

    def add_moves_for_piece(self, row, col, moves):
        piece_type = self.board[row][col][1]
        if piece_type != '-':
            self.move_functions[piece_type](row, col, moves)


    # chatGPT
    #The refactored code simplifies the white/black pawn move logic into a single set of conditionals by setting the direction, enemy, start_row, and end_row variables based on the self.white_to_move boolean value. The code also combines the diagonal capture checks into a single if statement, making it more concise. Finally, the code includes a TODO comment to remind the reader that pawn promotion and en-passant need to be implemented.
    def get_pawn_moves(self, row, col, moves):
        n = len(self.board)
        # so that we can swap what direction the pawn is facing
        direction = -1 if self.white_to_move else 1
        # for two move forward
        start_row = 6 if self.white_to_move else 1
        # for pawn promotion
        end_row = 0 if self.white_to_move else 7
        
        # forward one square
        if self.board[row+direction][col] == '--':
            moves.append(Move((row, col), (row+direction, col), self.board))
            # forward two squares
            if row == start_row and self.board[row+2*direction][col] == '--':
                moves.append(Move((row, col), (row+2*direction, col), self.board))
        
        enemy = 'b' if self.white_to_move else 'w'
        # diagonal left
        if col-1 >= 0 and self.board[row+direction][col-1][0] == enemy:
            moves.append(Move((row, col), (row+direction, col-1), self.board))
        # diagonal right
        if col+1 < n and self.board[row+direction][col+1][0] == enemy:
            moves.append(Move((row, col), (row+direction, col+1), self.board))

    # refactored chatGPT Code
    # Instead of using if statements to check each possible move, we can create a list of tuples representing all possible moves for the knight. Then, we iterate over each offset and check if the corresponding square is a valid move for the knight. If it is, we append the move to the list of moves.
    #Additionally, we can check if the destination square contains an enemy piece by comparing its color with the color of the knight's piece. We can simplify the logic by checking if the first character of the piece at the destination square is not the same as the knight's piece.
    def get_knight_moves(self, row, col, moves):
        n = len(self.board)
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for offset in offsets:
            end_row, end_col = row + offset[0], col + offset[1]
            if 0 <= end_row < n and 0 <= end_col < n:
                piece = self.board[end_row][end_col]
                if piece == '--' or piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (end_row, end_col), self.board))


    # get all diagonal moves for the Bishop at board[row][col]
    # add moves to list
    def get_bishop_moves(self, row, col, moves):
        self.get_diagonal(row, col, moves)


    # get all horizontal and vertical moves for the Rook at board[row][col]
    # add moves to list
    def get_rook_moves(self, row, col, moves):
        self.get_horizontal(row, col, moves)
        self.get_vertical(row, col, moves)


    # get all diagonal, horizontal and vertical moves for the Queen at board[row][col]
    # add moves to list
    def get_queen_moves(self, row, col, moves):
        self.get_diagonal(row, col, moves)
        self.get_horizontal(row, col, moves)
        self.get_vertical(row, col, moves)


    # refactored by ChatGPT
    # This code replaces the original 8 if-statements with a nested loop that checks all the squares around the king. It also uses the variable color to avoid duplicating the if-statements for the white and black kings. Finally, it skips the current square (i.e., the king's position) to avoid adding a move to the same square.
    def get_king_moves(self, row, col, moves):
        n = len(self.board)
        color = 'w' if self.white_to_move else 'b'
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if r == row and c == col:  # ignore the current square
                    continue
                if 0 <= r < n and 0 <= c < n and self.board[r][c][0] != color:
                    moves.append(Move((row, col), (r, c), self.board))
        #self.get_castling_moves(row, col, moves, color)


    # generate the valid castling moves for the respective king
    def get_castling_moves(self, row, col, moves):
        # cannot castle while in check
        if self.square_under_attack(row, col):
            return
        # check if squares are clear to whichever side you want to castle
        if (self.white_to_move and self.curr_castling_rights.wks) or (not self.white_to_move and self.curr_castling_rights.bks):
            self.get_king_side_castling_moves(row, col, moves)
        if (self.white_to_move and self.curr_castling_rights.wqs) or (not self.white_to_move and self.curr_castling_rights.bqs):
            self.get_queen_side_castling_moves(row, col, moves)

    
    def get_king_side_castling_moves(self, row, col, moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move=True))


    def get_queen_side_castling_moves(self, row, col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--':
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move=True))
        

    # ChatGPT
    # This version uses a loop that iterates over all four diagonals, and then another loop inside each diagonal that generates moves in that diagonal. The loop ends when it hits the edge of the board or a piece. If the piece is an enemy piece, the function appends the move and stops the loop.
    def get_diagonal(self, row, col, moves):
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                piece = self.board[r][c]
                if piece == '--':
                    moves.append(Move((row, col), (r, c), self.board))
                elif (self.white_to_move and piece[0] == 'b') or (not self.white_to_move and piece[0] == 'w'):
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
                r += dr
                c += dc

    
    # ChatGPT
    # The code has been refactored to use fewer repeated blocks of code and to make use of the range function to loop over the columns to the left and right of the starting position. The enemy color is now determined once and used throughout the method. Additionally, the comments have been removed as they did not add any value to the code.
    def get_horizontal(self, row, col, moves):
        n = len(self.board)
        # get the range of columns to check
        #left_range = range(col - 1, -1, -1)
        #right_range = range(col + 1, n)
        # define the enemy color
        enemy = 'b' if self.white_to_move else 'w'
        # check moves to the right
        #for i in right_range:
        for i in range(col + 1, n):
            piece = self.board[row][i]
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == enemy:
                moves.append(Move((row, col), (row, i), self.board))
                break
            else:
                break
        # check moves to the left
        #for i in left_range:
        for i in range(col - 1, -1, -1):
            piece = self.board[row][i]
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == enemy:
                moves.append(Move((row, col), (row, i), self.board))
                break
            else:
                break


    # chatGPT
    #This refactored version uses a loop to iterate over the two possible directions (up and down), and for each direction, it uses another loop to explore all the possible squares along that direction. The inner loop keeps track of the current position using the variables r and c, which are initialized to the position immediately above or below the starting square, depending on the direction. The loop continues as long as the current position is within the board boundaries, and updates the position by adding the direction vector to (r, c) at each iteration.
    #Inside the inner loop, the function checks the piece at the current position and appends a new Move object to the moves list if the square is empty or occupied by an opponent's piece. If the square is occupied by a piece of the same color, the loop is broken to avoid exploring squares beyond that piece.
    def get_vertical(self, row, col, moves):
        n = len(self.board)
        directions = [(1, 0), (-1, 0)]
        if self.white_to_move:
            directions = list(reversed(directions))
        for direction in directions:
            r, c = row + direction[0], col + direction[1]
            while 0 <= r < n and 0 <= c < n:
                piece = self.board[r][c]
                if piece == '--':
                    moves.append(Move((row, col), (r, c), self.board))
                elif piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
                r += direction[0]
                c += direction[1]


# white and black have castling rights on either the king or queen side
# track which are possible still
class CastlingRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


# for moves
class Move():
    # maps keys to values
    # key : value
    ranks_to_rows = { 
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
    }
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}

    files_to_cols = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    # start square, end square, board state
    def __init__(self, start, end, board, is_castle_move=False):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        # track pawn promotion
        self.is_pawn_promotion = False
        if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
            self.is_pawn_promotion = True

        # track castling
        self.is_castle_move = is_castle_move

        # gen unique move id between 0000 and 7777
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        #print(self.move_id)
        

    # override equals method
    # compare one object to (other) object
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

        