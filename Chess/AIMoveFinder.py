import random
import numpy as np

simplePieceValue = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'P': 1
}

complexPieceValue = {
    'K': 0,
    'Q': 2521,
    'R': 1270,
    'B': 836,
    'N': 817,
    'P': 198
}

# make king side castling more likely
kingPositionScores = np.array([
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
queenPositionScores = np.array([
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 4, 3, 3, 4, 3, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 4, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
])

# keep rook out of side
rookPositionScores = np.array([
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
bishopPositionScores = np.array([
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
knightPositionScores = np.array([
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
whitePawnPositionScores = np.array([
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
blackPawnPositionScores = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 1, 1, 2, 1, 1],
    [1, 2, 5, 5, 5, 3, 2, 1],
    [2, 2, 3, 6, 6, 3, 2, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
])

piecePositionScores = {
    'K': kingPositionScores,
    'Q': queenPositionScores,
    'R': rookPositionScores,
    'B': bishopPositionScores,
    'N': knightPositionScores,
    'wP': whitePawnPositionScores,
    'bP': blackPawnPositionScores
}

# global variables
CHECKMATE = 100000
STALEMATE = 0
# default 3, otherwise it is too slow without adding more optimizations
DEPTH = 3

# Board Evaluator functions ---------------------------------------------------
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            # black wins
            return -CHECKMATE
        else:
            # white wins
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]

            if square != '--':
                # score it positionally
                piecePositionScore = 0
                if square[1] == 'P':
                    pieceToEvaluate = square
                else:
                    pieceToEvaluate = square[1]
                piecePositionScore = piecePositionScores[pieceToEvaluate][row][col]
                    
                if square[0] == 'w':
                    #score += simplePieceValue[square[1]] + (piecePositionScore*0.2)
                    score += complexPieceValue[square[1]] + (piecePositionScore*5)
                elif square[0] == 'b':
                    #score -= simplePieceValue[square[1]] + (piecePositionScore*0.2)
                    score -= complexPieceValue[square[1]] + (piecePositionScore*5)
    return score

# Move Finder functions -------------------------------------------------------

# sometimes the AI needs this when it gets stuck
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

# makes the first recursive call
def getBestMoveMinMax(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    # reverse the list blacks turn to move, so that the moves considered first are deeper in enemy territory
    if not gs.whiteToMove:
        validMoves.reverse()
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print("Considered: " + str(counter) + " moves.")
    returnQueue.put(nextMove)

# yet another even better version of MinMax
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move.getChessNotation(), score)
        gs.undoMove()
        # alphabeta pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


