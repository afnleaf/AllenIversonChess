import random

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

CHECKMATE = 1000
STALEMATE = 0
EVALUTATOR = 1
DEPTH = 2


# sometimes the AI needs this when it gets stuck
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


# handles different evaluators based on the EVALUATOR flag
def scoreMaterial(board):
    if EVALUTATOR == 0:
        return simpleScoreMaterial(board)
    elif EVALUTATOR == 1:
        return complexScoreMaterial(board) 

# evaluator simple
def simpleScoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += simplePieceValue[square[1]]
            elif square[0] == 'b':
                score -= simplePieceValue[square[1]]
    return score

def complexScoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += complexPieceValue[square[1]]
            elif square[0] == 'b':
                score -= complexPieceValue[square[1]]
    return score


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
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += simplePieceValue[square[1]]
            elif square[0] == 'b':
                score -= simplePieceValue[square[1]]
    return score


# move finder GREEDY algorithm
def findGreedyMove(gs, validMoves):
    # is it black turn or white turn 
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkMate:
            score = CHECKMATE
        elif gs.staleMate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove


# move finder minmax algorithm, depth of 2
def findMinMaxDepth2Move(gs, validMoves):
    # is it black turn or white turn 
    turnMultiplier = 1 if gs.whiteToMove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    # add some randomness
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        if gs.staleMate:
            oppMaxScore = STALEMATE
        elif gs.checkMate:
            oppMaxScore = CHECKMATE
        else:
            oppMaxScore = -CHECKMATE
            for oppMove in oppMoves:
                gs.makeMove(oppMove)
                # kinda innefficient
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                    #bestPlayerMove = playerMove
                gs.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


# makes the first recursive call
def getBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMinMaxMove(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


# recursive to depth of tree provided
def findMinMaxMove(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore



