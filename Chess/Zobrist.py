import random

# hashing functions to create a unique key for the transposition table
# source: https://en.wikipedia.org/wiki/Zobrist_hashing
class ZobristHash:

    def __init__(self):
        self.piece_keys = {}
        self.side_key = 0
        # same board state can actually be different based on castling rights
        self.castling_keys = {}
        self.init_keys()

    # generating randomness
    def init_keys(self):
        for piece_type in ['P', 'N', 'B', 'R', 'Q', 'K']:
            for i in range(64):
                self.piece_keys[(piece_type, i)] = random.randint(0, 2**64-1)
        
        self.side_key = random.randint(0, 2**64-1)
        
        for i in range(16):
            self.castling_keys[i] = random.randint(0, 2**64-1)
        
    # return a hash value that considers the current state of the board
    def hash(self, board, white_to_move, curr_castling_rights):
        hash_value = 0
        
        # to track what square we are on
        i = 0
        for row, row_squares in enumerate(board):
            for col, square in enumerate(row_squares):
                piece_type = board[row][col][1]
                if piece_type != '-':
                    hash_value ^= self.piece_keys[(piece_type, i)]
                i += 1

        if not white_to_move:
            hash_value ^= self.side_key

        if curr_castling_rights.wqs:
            hash_value ^= self.castling_keys[0]
        if curr_castling_rights.wks:
            hash_value ^= self.castling_keys[1]
        if curr_castling_rights.bqs:
            hash_value ^= self.castling_keys[2]
        if curr_castling_rights.bks:
            hash_value ^= self.castling_keys[3]
        
        return hash_value