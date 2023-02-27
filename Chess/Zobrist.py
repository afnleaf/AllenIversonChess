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

    def hash(self, board):
        h = 0
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                piece_type = piece.symbol().upper()
                h ^= self.piece_keys[(piece_type, i)]
        
        if board.turn == chess.BLACK:
            h ^= self.side_key
        
        if board.has_kingside_castling_rights(chess.WHITE):
            h ^= self.castling_keys[0]
        if board.has_queenside_castling_rights(chess.WHITE):
            h ^= self.castling_keys[1]
        if board.has_kingside_castling_rights(chess.BLACK):
            h ^= self.castling_keys[2]
        if board.has_queenside_castling_rights(chess.BLACK):
            h ^= self.castling_keys[3]
        
        #if board.ep_square:
        #    h ^= self.en_passant_keys[board.ep_square]
        
        return h

# create a chess board
board = chess.Board()

print(board)

# create a ZobristHash object
zobrist = ZobristHash()

# get the Zobrist hash of the board
hash_value = zobrist.hash(board)

print(hash_value)



