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
        self.moveFunctions = {
            'P': self.getPawnMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'R': self.getRookMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }

        # white always moves first
        self.whiteToMove = True

        # track moves
        self.moveLog = []
    
    # take a move and execute it
    # castling and pawn promotion not implemented, could also add en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # log the move to undo it later
        self.moveLog.append(move)
        # switch turns
        self.whiteToMove = not self.whiteToMove


    # undo last move made
    def undoMove(self):
        # check if at least 1 move has been made
        if len(self.moveLog) != 0:
            # remove last element in list
            move = self.moveLog.pop()
            # return piece
            self.board[move.startRow][move.startCol] = move.pieceMoved
            # return captured piece
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # switch turns
            self.whiteToMove = not self.whiteToMove


    # all moves considering checks
    # ex pawn cant move if the pawn is pinned to a check by an opposing piece
    # player cant put themselves in check
    def getValidMoves(self):
        # not checking for checks rn
        return self.getAllPossibleMoves()


    # all moves without considering checks
    # consider all moves that are possible based on how a piece is legally allowed to move
    def getAllPossibleMoves(self):
        # moves = [Move((6,4), (4,4), self.board)]
        moves = []
        # check all pieces on our board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # find the colour of the piece
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    # get the piece type
                    piece = self.board[row][col][1]
                    # calls the appropriate move function based on the piece type
                    self.moveFunctions[piece](row, col, moves)
                    
                    '''
                    if piece == 'P':
                        self.getPawnMoves(row, col, moves)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, moves)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, moves)
                    elif piece == 'R':
                        self.getRookMoves(row, col, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, moves)
                    elif piece == 'K':
                        self.getKingMoves(row, col, moves)
                    '''
        return moves

    # chatGPT
    #The refactored code simplifies the white/black pawn move logic into a single set of conditionals by setting the direction, enemy, start_row, and end_row variables based on the self.whiteToMove boolean value. The code also combines the diagonal capture checks into a single if statement, making it more concise. Finally, the code includes a TODO comment to remind the reader that pawn promotion and en-passant need to be implemented.
    def getPawnMoves(self, row, col, moves):
        n = len(self.board)
        # so that we can swap what direction the pawn is facing
        direction = -1 if self.whiteToMove else 1
        # for two move forward
        start_row = 6 if self.whiteToMove else 1
        # for pawn promotion
        end_row = 0 if self.whiteToMove else 7
        
        # forward one square
        if self.board[row+direction][col] == '--':
            moves.append(Move((row, col), (row+direction, col), self.board))
            # forward two squares
            if row == start_row and self.board[row+2*direction][col] == '--':
                moves.append(Move((row, col), (row+2*direction, col), self.board))
        
        enemy = 'b' if self.whiteToMove else 'w'
        # diagonal left
        if col-1 >= 0 and self.board[row+direction][col-1][0] == enemy:
            moves.append(Move((row, col), (row+direction, col-1), self.board))
        # diagonal right
        if col+1 < n and self.board[row+direction][col+1][0] == enemy:
            moves.append(Move((row, col), (row+direction, col+1), self.board))
            
        # TODO: pawn promotion, en-passant not allowed

    # refactored chatGPT Code
    # Instead of using if statements to check each possible move, we can create a list of tuples representing all possible moves for the knight. Then, we iterate over each offset and check if the corresponding square is a valid move for the knight. If it is, we append the move to the list of moves.
    #Additionally, we can check if the destination square contains an enemy piece by comparing its color with the color of the knight's piece. We can simplify the logic by checking if the first character of the piece at the destination square is not the same as the knight's piece.
    def getKnightMoves(self, row, col, moves):
        n = len(self.board)
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for offset in offsets:
            x, y = row + offset[0], col + offset[1]
            if 0 <= x < n and 0 <= y < n:
                piece = self.board[x][y]
                if piece == '--' or piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (x, y), self.board))

    # get all diagonal moves for the Bishop at board[row][col]
    # add moves to list
    def getBishopMoves(self, row, col, moves):
        self.getDiagonal(row, col, moves)

    # get all horizontal and vertical moves for the Rook at board[row][col]
    # add moves to list
    def getRookMoves(self, row, col, moves):
        self.getHorizontal(row, col, moves)
        self.getVertical(row, col, moves)
                
    # get all diagonal, horizontal and vertical moves for the Queen at board[row][col]
    # add moves to list
    def getQueenMoves(self, row, col, moves):
        self.getDiagonal(row, col, moves)
        self.getHorizontal(row, col, moves)
        self.getVertical(row, col, moves)


    # refactored by ChatGPT
    # This code replaces the original 8 if-statements with a nested loop that checks all the squares around the king. It also uses the variable color to avoid duplicating the if-statements for the white and black kings. Finally, it skips the current square (i.e., the king's position) to avoid adding a move to the same square.
    def getKingMoves(self, row, col, moves):
        n = len(self.board)
        color = 'w' if self.whiteToMove else 'b'
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if r == row and c == col:  # ignore the current square
                    continue
                if 0 <= r < n and 0 <= c < n and self.board[r][c][0] != color:
                    moves.append(Move((row, col), (r, c), self.board))

    # ChatGPT
    # This version uses a loop that iterates over all four diagonals, and then another loop inside each diagonal that generates moves in that diagonal. The loop ends when it hits the edge of the board or a piece. If the piece is an enemy piece, the function appends the move and stops the loop.
    def getDiagonal(self, row, col, moves):
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                piece = self.board[r][c]
                if piece == '--':
                    moves.append(Move((row, col), (r, c), self.board))
                elif (self.whiteToMove and piece[0] == 'b') or (not self.whiteToMove and piece[0] == 'w'):
                    moves.append(Move((row, col), (r, c), self.board))
                    break
                else:
                    break
                r += dr
                c += dc

    
    # ChatGPT
    # The code has been refactored to use fewer repeated blocks of code and to make use of the range function to loop over the columns to the left and right of the starting position. The enemy color is now determined once and used throughout the method. Additionally, the comments have been removed as they did not add any value to the code.
    def getHorizontal(self, row, col, moves):
        n = len(self.board)
        # get the range of columns to check
        #left_range = range(col - 1, -1, -1)
        #right_range = range(col + 1, n)
        # define the enemy color
        enemy = 'b' if self.whiteToMove else 'w'
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
    def getVertical(self, row, col, moves):
        n = len(self.board)
        directions = [(1, 0), (-1, 0)]
        if self.whiteToMove:
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


# for moves
class Move():

    # maps keys to values
    # key : value
    ranksToRows = { 
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
    }
    rowsToRanks = {value: key for key, value in ranksToRows.items()}

    filesToCols = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }
    colsToFiles = {value: key for key, value in filesToCols.items()}

    # start square, end square, board state
    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # gen unique move id between 0000 and 7777
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)


    # override equals method
    # compare one object to (other) object
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

        