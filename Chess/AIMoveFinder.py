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

# make king side castling more likely
kingScores = [
    [1, 1, 4, 1, 1, 1, 6, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 4, 1, 1, 1, 6, 1]
]

# get queen on diags, more towards queen side
queenScores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 4, 3, 3, 4, 3, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 4, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
]

# keep rook out of side
rookScores = [
    [4, 2, 4, 4, 4, 4, 2, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 2, 4, 3, 3, 4, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 4, 3, 3, 4, 2, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 2, 4, 4, 4, 4, 2, 4],
]

# get on those diags
bishopScores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4]
]

# central knight is better than rim knight
knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# go towards the promotion
whitePawnScores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 2, 3, 6, 6, 3, 2, 2],
    [1, 2, 3, 5, 5, 3, 2, 1],
    [1, 1, 2, 1, 1, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# 5 for sicilian
blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 1, 1, 2, 1, 1],
    [1, 2, 5, 5, 5, 3, 2, 1],
    [2, 2, 3, 6, 6, 3, 2, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
]

piecePositionScores = {
    'K': kingScores,
    'Q': queenScores,
    'R': rookScores,
    'B': bishopScores,
    'N': knightScores,
    'wP': whitePawnScores,
    'bP': blackPawnScores
}

CHECKMATE = 1000
STALEMATE = 0
EVALUTATOR = 1
DEPTH = 3


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


def scoreBoard_old(gs):
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
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += simplePieceValue[square[1]]
            elif square[0] == 'b':
                score -= simplePieceValue[square[1]]
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
                    score += simplePieceValue[square[1]] + (piecePositionScore*0.2)
                elif square[0] == 'b':
                    score -= simplePieceValue[square[1]] + (piecePositionScore*0.2)
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
def getBestMoveMinMax(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    #findMinMaxMove(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print("Considered: " + str(counter) + " moves.")
    returnQueue.put(nextMove)


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


# yet another better version of MinMax
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


# yet another even better version of MinMax
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)

    # move ordering - toadd

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


