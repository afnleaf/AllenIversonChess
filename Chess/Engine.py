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


    # get all pawn moves for the Pawn at board[row][col]
    # add moves to list
    # todo: pawn promotion, en-passant?
    def getPawnMoves(self, row, col, moves):
        n = len(self.board)
        # white pawn moves
        if self.whiteToMove:
            # 1 square pawn advance
            if self.board[row-1][col] == '--':
                moves.append(Move((row, col), (row-1, col), self.board))
                # 2 square pawn advance
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row, col), (row-2, col), self.board))
            # diagonal capture left
            if col-1 >= 0:
                # check for enemy piece
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            # diagonal capture right
            if col+1 < n:
                # check for enemy piece
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        # black pawn moves
        else:
            # 1 square pawn advance
            if self.board[row+1][col] == '--':
                moves.append(Move((row, col), (row+1, col), self.board))
                # 2 square pawn advance
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row, col), (row+2, col), self.board))
            # diagonal capture right
            if col-1 >= 0:
                # check for enemy piece
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            # diagonal capture right
            if col+1 < n:
                # check for enemy piece
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))


    # get all pawn moves for the Knight at board[row][col]
    # add moves to list
    # to:do refactor
    def getKnightMoves(self, row, col, moves):
        n = len(self.board)
        # white knight moves
        if self.whiteToMove:
            # check up
            if row-2 >= 0:
                if col+1 < n and (self.board[row-2][col+1] == '--' or self.board[row-2][col+1][0] == 'b'):
                    moves.append(Move((row, col), (row-2, col+1), self.board))
                if col-1 >= 0 and (self.board[row-2][col-1] == '--' or self.board[row-2][col-1][0] == 'b' ):
                    moves.append(Move((row, col), (row-2, col-1), self.board))
            # check down
            if row+2 < n:
                if col+1 < n and (self.board[row+2][col+1] == '--' or self.board[row+2][col+1][0] == 'b'):
                    moves.append(Move((row, col), (row+2, col+1), self.board))
                if col-1 >= 0 and (self.board[row+2][col-1] == '--' or self.board[row+2][col-1][0] == 'b'):
                    moves.append(Move((row, col), (row+2, col-1), self.board))
            # check right
            if col-2 >= 0:
                if row-1 >= 0 and (self.board[row-1][col-2] == '--' or self.board[row-1][col-2][0] == 'b'):
                    moves.append(Move((row, col), (row-1, col-2), self.board))
                if row+1 < n and (self.board[row+1][col-2] == '--' or self.board[row+1][col-2][0] == 'b'):
                    moves.append(Move((row, col), (row+1, col-2), self.board))
            # check left
            if col+2 < n:
                if row-1 >= 0 and (self.board[row-1][col+2] == '--' or self.board[row-1][col+2][0] == 'b'):
                    moves.append(Move((row, col), (row-1, col+2), self.board))
                if row+1 < n and (self.board[row+1][col+2] == '--' or self.board[row+1][col+2][0] == 'b'):
                    moves.append(Move((row, col), (row+1, col+2), self.board))
        # black knight moves
        else:
            # check up
            if row-2 >= 0:
                if col+1 < n and (self.board[row-2][col+1] == '--' or self.board[row-2][col+1][0] == 'w'):
                    moves.append(Move((row, col), (row-2, col+1), self.board))
                if col-1 >= 0 and (self.board[row-2][col-1] == '--' or self.board[row-2][col-1][0] == 'w' ):
                    moves.append(Move((row, col), (row-2, col-1), self.board))
            # check down
            if row+2 < n:
                if col+1 < n and (self.board[row+2][col+1] == '--' or self.board[row+2][col+1][0] == 'w'):
                    moves.append(Move((row, col), (row+2, col+1), self.board))
                if col-1 >= 0 and (self.board[row+2][col-1] == '--' or self.board[row+2][col-1][0] == 'w'):
                    moves.append(Move((row, col), (row+2, col-1), self.board))
            # check right
            if col-2 >= 0:
                if row-1 >= 0 and (self.board[row-1][col-2] == '--' or self.board[row-1][col-2][0] == 'w'):
                    moves.append(Move((row, col), (row-1, col-2), self.board))
                if row+1 < n and (self.board[row+1][col-2] == '--' or self.board[row+1][col-2][0] == 'w'):
                    moves.append(Move((row, col), (row+1, col-2), self.board))
            # check left
            if col+2 < n:
                if row-1 >= 0 and (self.board[row-1][col+2] == '--' or self.board[row-1][col+2][0] == 'w'):
                    moves.append(Move((row, col), (row-1, col+2), self.board))
                if row+1 < n and (self.board[row+1][col+2] == '--' or self.board[row+1][col+2][0] == 'w'):
                    moves.append(Move((row, col), (row+1, col+2), self.board))

    # get all pawn moves for the Bishop at board[row][col]
    # add moves to list
    # to:do refactor
    def getBishopMoves(self, row, col, moves):
        n = len(self.board)
        # white bishop moves
        if self.whiteToMove:
            # check up and right
            rminu = row - 1
            cplus = col + 1
            while rminu >= 0 and cplus < n:
                piece = self.board[rminu][cplus]
                if piece == '--':
                    moves.append(Move((row, col), (rminu, cplus), self.board))
                elif piece[0] == 'b':
                    moves.append(Move((row, col), (rminu, cplus), self.board))
                    break
                elif piece[0] == 'w':
                    break
                rminu -= 1
                cplus += 1

            # check up and left
            rminu = row - 1
            cminu = col - 1
            while rminu >= 0 and cminu < n:
                piece = self.board[rminu][cminu]
                if piece == '--':
                    moves.append(Move((row, col), (rminu, cminu), self.board))
                elif piece[0] == 'b':
                    moves.append(Move((row, col), (rminu, cminu), self.board))
                    break
                elif piece[0] == 'w':
                    break
                rminu -= 1
                cminu -= 1

            # check down and right
            rplus = row + 1
            cplus = col + 1
            while rplus < n and cplus < n:
                piece = self.board[rplus][cplus]
                if piece == '--':
                    moves.append(Move((row, col), (rplus, cplus), self.board))
                elif piece[0] == 'b':
                    moves.append(Move((row, col), (rplus, cplus), self.board))
                    break
                elif piece[0] == 'w':
                    break
                rplus += 1
                cplus += 1

            # check down and left
            rplus = row + 1
            cminu = col - 1
            while rplus < n and cminu >= 0:
                piece = self.board[rplus][cminu]
                if piece == '--':
                    moves.append(Move((row, col), (rplus, cminu), self.board))
                elif piece[0] == 'b':
                    moves.append(Move((row, col), (rplus, cminu), self.board))
                    break
                elif piece[0] == 'w':
                    break
                rplus += 1
                cminu -= 1

        # black bishop moves
        else:
            # check up and right
            rminu = row - 1
            cplus = col + 1
            while rminu >= 0 and cplus < n:
                piece = self.board[rminu][cplus]
                if piece == '--':
                    moves.append(Move((row, col), (rminu, cplus), self.board))
                elif piece[0] == 'w':
                    moves.append(Move((row, col), (rminu, cplus), self.board))
                    break
                elif piece[0] == 'b':
                    break
                rminu -= 1
                cplus += 1

            # check up and left
            rminu = row - 1
            cminu = col - 1
            while rminu >= 0 and cminu < n:
                piece = self.board[rminu][cminu]
                if piece == '--':
                    moves.append(Move((row, col), (rminu, cminu), self.board))
                elif piece[0] == 'w':
                    moves.append(Move((row, col), (rminu, cminu), self.board))
                    break
                elif piece[0] == 'b':
                    break
                rminu -= 1
                cminu -= 1

            # check down and right
            rplus = row + 1
            cplus = col + 1
            while rplus < n and cplus < n:
                piece = self.board[rplus][cplus]
                if piece == '--':
                    moves.append(Move((row, col), (rplus, cplus), self.board))
                elif piece[0] == 'w':
                    moves.append(Move((row, col), (rplus, cplus), self.board))
                    break
                elif piece[0] == 'b':
                    break
                rplus += 1
                cplus += 1

            # check down and left
            rplus = row + 1
            cminu = col - 1
            while rplus < n and cminu >= 0:
                piece = self.board[rplus][cminu]
                if piece == '--':
                    moves.append(Move((row, col), (rplus, cminu), self.board))
                elif piece[0] == 'w':
                    moves.append(Move((row, col), (rplus, cminu), self.board))
                    break
                elif piece[0] == 'b':
                    break
                rplus += 1
                cminu -= 1


    # get all pawn moves for the Rook at board[row][col]
    # add moves to list
    def getRookMoves(self, row, col, moves):
        pass


    # get all pawn moves for the Queen at board[row][col]
    # add moves to list
    def getQueenMoves(self, row, col, moves):
        pass


    # get all pawn moves for the King at board[row][col]
    # add moves to list
    def getKingMoves(self, row, col, moves):
        pass
    


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

        