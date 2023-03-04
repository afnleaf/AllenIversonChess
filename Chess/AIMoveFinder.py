import random
import time
import numpy as np
# import constants from config
from config import *

# left midgame, right endgame
complex_piece_value = {
    'K': [0, 0],
    'Q': [2521, 2558],
    'R': [1270, 1281],
    'B': [836, 857],
    'N': [817, 846],
    'P': [198, 258]
}

# make king side castling more likely
king_pos_scores = np.array([
    [1, 1, 4, 1, 1, 1, 6, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 4, 1, 1, 1, 6, 1]
])

# get queen on diags, more towards queen side
queen_pos_scores = np.array([
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 4, 3, 3, 1, 1, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 4, 3, 3, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
])

# keep rook out of side
rook_pos_scores = np.array([
    [4, 2, 4, 4, 4, 4, 2, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 2, 4, 3, 3, 4, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 4, 3, 3, 4, 2, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 2, 4, 4, 4, 4, 2, 4],
])

# get on those diags
bishop_pos_scores = np.array([
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4]
])

# central knight is better than rim knight
knight_pos_scores = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 5, 5, 5, 5, 2, 1],
    [1, 2, 5, 8, 8, 5, 2, 1],
    [1, 2, 5, 8, 8, 5, 2, 1],
    [1, 2, 5, 5, 5, 5, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
])

# go towards the promotion
white_pawn_pos_scores = np.array([
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 2, 3, 6, 6, 3, 2, 2],
    [1, 2, 3, 5, 5, 3, 2, 1],
    [1, 1, 2, 1, 1, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

# 5 for sicilian
black_pawn_pos_scores = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 1, 1, 2, 1, 1],
    [1, 2, 5, 5, 5, 3, 2, 1],
    [2, 2, 3, 6, 6, 3, 2, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
])

piece_pos_scores = {
    'K': king_pos_scores,
    'Q': queen_pos_scores,
    'R': rook_pos_scores,
    'B': bishop_pos_scores,
    'N': knight_pos_scores,
    'wP': white_pawn_pos_scores,
    'bP': black_pawn_pos_scores
}

# Board Evaluator functions ---------------------------------------------------
def score_board(gs):
    if gs.checkmate:
        return -CHECKMATE if gs.white_to_move else CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    # default midgame
    # once above 50 turns, take the endgame value of a piece
    turn_value = 0
    if gs.turn_counter > 50:
        turn_value = 1
    #also can change based on num pieces left in the game
    elif gs.num_pieces_left < 22:
        turn_value = 1

    total_score = 0
    for row_index, row in enumerate(gs.board):
        for col_index, square in enumerate(row):
            if square == '--':
                continue
            # determine if the piece is a pawn or not
            if square[1] == 'P':
                piece = square
            else:
                piece = square[1]
            piece_pos_score = piece_pos_scores[piece][row_index][col_index]
            # Add or subtract the score based on the color of the piece
            color = square[0]
            score = complex_piece_value[square[1]][turn_value] + (piece_pos_score * POSITIONAL_SCORE_FACTOR)
            total_score += score if color == 'w' else -score
    return total_score

# Move Finder functions -------------------------------------------------------

# sometimes the AI needs this when it gets stuck
def find_random_move(valid_moves):
    return random.choice(valid_moves)

# makes the first recursive call
def get_best_move_minmax(gs, valid_moves, return_queue):
    global next_move, counter
    next_move = None
    # reverse the list on blacks turn to move, so that the moves considered first are deeper in enemy territory
    # this introduces a problem where the AI will play the same game everytime against itself
    # would need to implement randomness to the slice of first couple of moves and see if that changes anything
    #if not gs.white_to_move:
    #    valid_moves.reverse()
    # add some randomness
    random.shuffle(valid_moves)
    counter = 0
    time_before = time.time()
    turn = 1 if gs.white_to_move else -1
    find_move_negamax_alphabeta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, turn, time_before)
    time_after = time.time()
    print("Considered: " + str(counter) + " moves.", str("%.2f" % (time_after - time_before)), "seconds.")
    return_queue.put(next_move)

# yet another even better version of minmax
# source: https://en.wikipedia.org/wiki/Negamax
# TODO: implement transposition tables
def find_move_negamax_alphabeta(gs, valid_moves, depth, alpha, beta, turn_multiplier, time_before):
    global next_move, counter
    counter += 1
    time_after = time.time()
    if depth == 0 or time_after - time_before > TIMELIMIT:
        return turn_multiplier*score_board(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        # get opp moves
        next_moves = gs.get_valid_moves()
        # find core for the next moves
        score = -find_move_negamax_alphabeta(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplier, time_before)
        
        if max_score < score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move.get_chess_notation(), score)
        gs.undo_move()
        # alphabeta pruning
        '''
        if max_score > alpha:
            alpha = max_score
        '''
        alpha = max(alpha, max_score)
        if alpha >= beta:
            break        

    return max_score
