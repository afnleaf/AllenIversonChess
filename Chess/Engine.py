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

        # keep track of king's location for efficiency
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)

        # game end state
        self.checkMake = False
        self.staleMate = False

        # for castling
        self.currCastlingRights = CastlingRights(True, True, True, True)
        # copying the values to a new object
        self.castlingRightsLog = [CastlingRights(self.currCastlingRights.wks, 
                                                 self.currCastlingRights.bks, 
                                                 self.currCastlingRights.wqs, 
                                                 self.currCastlingRights.bqs)]
        
    

    # take a move and execute it
    # castling and pawn promotion not implemented, could also add en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # log the move to undo it later
        self.moveLog.append(move)
        # switch turns
        self.whiteToMove = not self.whiteToMove
        # update king's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        # defaulting to just queen for now
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # castling
        # move rook into new square
        # remove from old square
        if move.isCastleMove:
            #print("CASTLEMOVE")
            #print(self.board[move.endRow][move.endCol])
            # kingside
            if move.endCol - move.startCol == 2:
                #print("ks")
                #print(self.board[move.endRow][move.endCol-1])
                #print(self.board[move.endRow][move.endCol+1])
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            # queenside
            else:
                #print("qs")
                #print(self.board[move.endRow][move.endCol+1])
                #print(self.board[move.endRow][move.endCol-2])
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        # update castling rights, rook/king move
        self.updateCastlingRights(move)
        self.castlingRightsLog.append(CastlingRights(self.currCastlingRights.wks, 
                                                     self.currCastlingRights.bks, 
                                                     self.currCastlingRights.wqs, 
                                                     self.currCastlingRights.bqs))

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
            # undo the update to king's location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo castling rights, remove last
            self.castlingRightsLog.pop()
            newRights = self.castlingRightsLog[-1]
            self.currCastlingRights = CastlingRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            # undo the castle
            # remove from new location, put back into old location
            if move.isCastleMove:
                # kingside
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                # queenside
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'


    def updateCastlingRights(self, move):
        # king moves
        if move.pieceMoved == 'wK':
            self.currCastlingRights.wks = False
            self.currCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currCastlingRights.bks = False
            self.currCastlingRights.bqs = False
        # for rook, check if its left or right
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                # left rook
                if move.startCol == 0:
                    self.currCastlingRights.wqs = False
                # right rook
                elif move.startCol == 7:
                    self.currCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                # left rook
                if move.startCol == 0:
                    self.currCastlingRights.bqs = False
                # right rook
                elif move.startCol == 7:
                    self.currCastlingRights.bks = False



    # print the move log to console
    def printMoveLog(self):
        print("Move log:")
        i = 1
        for move in self.moveLog:
            print(str(i) + ". " + move.getChessNotation())
            i += 1


    # all moves considering checks
    # ex pawn cant move if the pawn is pinned to a check by an opposing piece
    # player cant put themselves in check
    def getValidMoves(self):
        #for log in self.castlingRightsLog:
        #    print(log.wks, log.wqs, log.bks, log.bqs, end = ", ")
        #print()

        # temp castling rights to avoid all the possible changes
        tempCastlingRights = CastlingRights(self.currCastlingRights.wks,
                                            self.currCastlingRights.bks,
                                            self.currCastlingRights.wqs,
                                            self.currCastlingRights.bqs)
        
        # generate all possible moves whether they are valid or not
        moves = self.getAllPossibleMoves()
        # get the castling movess
        if self.whiteToMove:
            self.getCastlingMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastlingMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        
        # make each move
        # move through the list backwards
        for i in range(len(moves)-1, -1 , -1):
            self.makeMove(moves[i])
            # we need to switch back after we do makeMove()
            self.whiteToMove = not self.whiteToMove
            # gen all opp's moves, see if they attack your king
            if self.inCheck():
                # if the move puts us in check, we need to remove that move from the list of valid moves
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        # checking for checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.currCastlingRights = tempCastlingRights

        return moves
    
    # determine if current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    # determine if they enemy can attack the square at row, col
    def squareUnderAttack(self, row, col):
        # switch to opp turn
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        # switch back
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:        
                return True
        return False


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
            endRow, endCol = row + offset[0], col + offset[1]
            if 0 <= endRow < n and 0 <= endCol < n:
                piece = self.board[endRow][endCol]
                if piece == '--' or piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (endRow, endCol), self.board))


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
        #self.getCastlingMoves(row, col, moves, color)


    # generate the valid castling moves for the respective king
    def getCastlingMoves(self, row, col, moves):
        # cannot castle while in check
        if self.squareUnderAttack(row, col):
            return
        # check if squares are clear to whichever side you want to castle
        if (self.whiteToMove and self.currCastlingRights.wks) or (not self.whiteToMove and self.currCastlingRights.bks):
            self.getKingSideCastlingMoves(row, col, moves)
        if (self.whiteToMove and self.currCastlingRights.wqs) or (not self.whiteToMove and self.currCastlingRights.bqs):
            self.getQueenSideCastlingMoves(row, col, moves)

    
    def getKingSideCastlingMoves(self, row, col, moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.squareUnderAttack(row, col+1) and not self.squareUnderAttack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))


    def getQueenSideCastlingMoves(self, row, col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--':
            if not self.squareUnderAttack(row, col-1) and not self.squareUnderAttack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastleMove=True))
        

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
    def __init__(self, start, end, board, isCastleMove=False):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        # track pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True

        # track castling
        self.isCastleMove = isCastleMove

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

        