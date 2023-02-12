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
        moves = [Move((6,4), (4,4), self.board)]
        # check all pieces on our board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # find the colour of the piece
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    # get the piece type
                    piece = self.board[row][col][1]
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
        return moves


    # get all pawn moves for the Pawn at board[row][col]
    # add moves to list
    def getPawnMoves(row, col, moves):
        pass


    # get all pawn moves for the Knight at board[row][col]
    # add moves to list
    def getKnightMoves(row, col, moves):
        pass

    # get all pawn moves for the Bishop at board[row][col]
    # add moves to list
    def getBishopMoves(row, col, moves):
        pass

    # get all pawn moves for the Rook at board[row][col]
    # add moves to list
    def getRookMoves(row, col, moves):
        pass

    # get all pawn moves for the Queen at board[row][col]
    # add moves to list
    def getQueenMoves(row, col, moves):
        pass

    # get all pawn moves for the King at board[row][col]
    # add moves to list
    def getKingMoves(row, col, moves):
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

        