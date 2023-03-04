import chess
import random

class ZobristHash:
    def __init__(self):
        self.piece_keys = {}
        self.side_key = 0
        self.castling_keys = {}
        #self.en_passant_keys = {}

        self.init_keys()

    def init_keys(self):
        for piece_type in ['P', 'N', 'B', 'R', 'Q', 'K']:
            for i in range(64):
                self.piece_keys[(piece_type, i)] = random.randint(0, 2**64-1)
        
        self.side_key = random.randint(0, 2**64-1)
        
        for i in range(16):
            self.castling_keys[i] = random.randint(0, 2**64-1)
        
        #for i in range(64):
        #    self.en_passant_keys[i] = random.randint(0, 2**64-1)

    def hash(self, board, white_to_move, curr_castling_rights):
        hash_value = 0
        '''
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                piece_type = piece.symbol().upper()
                hash_value ^= self.piece_keys[(piece_type, i)]
        '''
        # to track what square we are on
        i = 0
        for row, row_squares in enumerate(board):
            for col, square in enumerate(row_squares):
                piece_type = board[row][col][1]
                if piece_type != '-':
                    #self.move_functions[piece_type](row, col, moves)
                    hash_value ^= self.piece_keys[(piece_type, i)]
                i += 1

        '''
        if board.turn == chess.BLACK:
            hash_value ^= self.side_key
        '''
        if not white_to_move:
            hash_value ^= self.side_key
        '''
        if board.has_kingside_castling_rights(chess.WHITE):
            hash_value ^= self.castling_keys[0]
        if board.has_queenside_castling_rights(chess.WHITE):
            hash_value ^= self.castling_keys[1]
        if board.has_kingside_castling_rights(chess.BLACK):
            hash_value ^= self.castling_keys[2]
        if board.has_queenside_castling_rights(chess.BLACK):
            hash_value ^= self.castling_keys[3]
        '''
        if curr_castling_rights.wqs:
            hash_value ^= self.castling_keys[0]
        if curr_castling_rights.wks:
            hash_value ^= self.castling_keys[1]
        if curr_castling_rights.bqs:
            hash_value ^= self.castling_keys[2]
        if curr_castling_rights.bks:
            hash_value ^= self.castling_keys[3]
        
        return hash_value

'''
# create a chess board
board = chess.Board()

print(board)

# create a ZobristHash object
zobrist = ZobristHash()

# get the Zobrist hash of the board
hash_value = zobrist.hash(board)
print(hash_value)
hash_value = zobrist.hash(board)
print(hash_value)
'''