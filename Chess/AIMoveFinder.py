import random
import numpy as np

simple_piece_value = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'P': 1
}

complex_piece_value = {
    'K': 0,
    'Q': 2521,
    'R': 1270,
    'B': 836,
    'N': 817,
    'P': 198
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
    [1, 4, 4, 3, 3, 3, 3, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 4, 3, 3, 3, 2, 1],
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
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
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

# global variables
CHECKMATE = 100000
STALEMATE = 0
# default 3, otherwise it is too slow without adding more optimizations
DEPTH = 3

# Board Evaluator functions ---------------------------------------------------
def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            # black wins
            return -CHECKMATE
        else:
            # white wins
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]

            if square != '--':
                # score it positionally
                curr_piece_pos_score = 0
                if square[1] == 'P':
                    curr_piece = square
                else:
                    curr_piece = square[1]
                curr_piece_pos_score = piece_pos_scores[curr_piece][row][col]
                    
                if square[0] == 'w':
                    #score += simple_piece_value[square[1]] + (curr_piece_pos_score*0.2)
                    score += complex_piece_value[square[1]] + (curr_piece_pos_score*5)
                elif square[0] == 'b':
                    #score -= simple_piece_value[square[1]] + (curr_piece_pos_score*0.2)
                    score -= complex_piece_value[square[1]] + (curr_piece_pos_score*5)
    return score

# Move Finder functions -------------------------------------------------------

# sometimes the AI needs this when it gets stuck
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

# makes the first recursive call
def get_best_move_minmax(gs, valid_moves, return_queue):
    global next_move, counter
    next_move = None
    # reverse the list blacks turn to move, so that the moves considered first are deeper in enemy territory
    if not gs.white_to_move:
        valid_moves.reverse()
    counter = 0
    find_move_negamax_alphabeta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print("Considered: " + str(counter) + " moves.")
    return_queue.put(next_move)

# yet another even better version of MinMax
def find_move_negamax_alphabeta(gs, valid_moves, depth, alpha, beta, turnMultiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*score_board(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax_alphabeta(gs, next_moves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move.get_chess_notation(), score)
        gs.undo_move()
        # alphabeta pruning
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


