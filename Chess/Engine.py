"""
Stores all the info about the current game state.
Determines valid moves at that state.
Logs moves.
"""

class GameState():
    def __init__(self):
        # consider numpy arrays for increased AI speed
        # 8x8 2D list
        # each element has two characters
        # w is white, b is black, 2nd char is the piece type:
        # P Pawn, N Knight, B Bishop, R Rook, Q Queen, K King, -- empty 
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]

        # white always moves first
        self.whiteToMove = True

        # track moves
        self.moveLog = []

        