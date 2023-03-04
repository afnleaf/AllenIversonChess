# Chess Moves -----------------------------------------------------------------

# get all pawn moves for the Pawn at board[row][col]
# add moves to list
# todo: pawn promotion, en-passant?
def getPawnMoves_old(self, row, col, moves):
    n = len(self.board)
    # white pawn moves
    if self.whiteToMove:
        # 1 square pawn advance
        if self.board[row-1][col] == '--':
            moves.append(Move((row, col), (row-1, col), self.board))
            # 2 square pawn advance
            if row == 6 and self.board[row-2][col] == '--':
                moves.append(Move((row, col), (row-2, col), self.board))
        # diagonal capture left
        if col-1 >= 0:
            # check for enemy piece
            if self.board[row-1][col-1][0] == 'b':
                moves.append(Move((row, col), (row-1, col-1), self.board))
        # diagonal capture right
        if col+1 < n:
            # check for enemy piece
            if self.board[row-1][col+1][0] == 'b':
                moves.append(Move((row, col), (row-1, col+1), self.board))

    # black pawn moves
    else:
        # 1 square pawn advance
        if self.board[row+1][col] == '--':
            moves.append(Move((row, col), (row+1, col), self.board))
            # 2 square pawn advance
            if row == 1 and self.board[row+2][col] == '--':
                moves.append(Move((row, col), (row+2, col), self.board))
        # diagonal capture right
        if col-1 >= 0:
            # check for enemy piece
            if self.board[row+1][col-1][0] == 'w':
                moves.append(Move((row, col), (row+1, col-1), self.board))
        # diagonal capture right
        if col+1 < n:
            # check for enemy piece
            if self.board[row+1][col+1][0] == 'w':
                moves.append(Move((row, col), (row+1, col+1), self.board))

# get all moves for the Knight at board[row][col]
# add moves to list
# to:do refactor
def getKnightMoves_old(self, row, col, moves):
    n = len(self.board)
    # white knight moves
    if self.whiteToMove:
        # check up
        if row-2 >= 0:
            if col+1 < n and (self.board[row-2][col+1] == '--' or self.board[row-2][col+1][0] == 'b'):
                moves.append(Move((row, col), (row-2, col+1), self.board))
            if col-1 >= 0 and (self.board[row-2][col-1] == '--' or self.board[row-2][col-1][0] == 'b' ):
                moves.append(Move((row, col), (row-2, col-1), self.board))
        # check down
        if row+2 < n:
            if col+1 < n and (self.board[row+2][col+1] == '--' or self.board[row+2][col+1][0] == 'b'):
                moves.append(Move((row, col), (row+2, col+1), self.board))
            if col-1 >= 0 and (self.board[row+2][col-1] == '--' or self.board[row+2][col-1][0] == 'b'):
                moves.append(Move((row, col), (row+2, col-1), self.board))
        # check right
        if col-2 >= 0:
            if row-1 >= 0 and (self.board[row-1][col-2] == '--' or self.board[row-1][col-2][0] == 'b'):
                moves.append(Move((row, col), (row-1, col-2), self.board))
            if row+1 < n and (self.board[row+1][col-2] == '--' or self.board[row+1][col-2][0] == 'b'):
                moves.append(Move((row, col), (row+1, col-2), self.board))
        # check left
        if col+2 < n:
            if row-1 >= 0 and (self.board[row-1][col+2] == '--' or self.board[row-1][col+2][0] == 'b'):
                moves.append(Move((row, col), (row-1, col+2), self.board))
            if row+1 < n and (self.board[row+1][col+2] == '--' or self.board[row+1][col+2][0] == 'b'):
                moves.append(Move((row, col), (row+1, col+2), self.board))
    # black knight moves
    else:
        # check up
        if row-2 >= 0:
            if col+1 < n and (self.board[row-2][col+1] == '--' or self.board[row-2][col+1][0] == 'w'):
                moves.append(Move((row, col), (row-2, col+1), self.board))
            if col-1 >= 0 and (self.board[row-2][col-1] == '--' or self.board[row-2][col-1][0] == 'w' ):
                moves.append(Move((row, col), (row-2, col-1), self.board))
        # check down
        if row+2 < n:
            if col+1 < n and (self.board[row+2][col+1] == '--' or self.board[row+2][col+1][0] == 'w'):
                moves.append(Move((row, col), (row+2, col+1), self.board))
            if col-1 >= 0 and (self.board[row+2][col-1] == '--' or self.board[row+2][col-1][0] == 'w'):
                moves.append(Move((row, col), (row+2, col-1), self.board))
        # check right
        if col-2 >= 0:
            if row-1 >= 0 and (self.board[row-1][col-2] == '--' or self.board[row-1][col-2][0] == 'w'):
                moves.append(Move((row, col), (row-1, col-2), self.board))
            if row+1 < n and (self.board[row+1][col-2] == '--' or self.board[row+1][col-2][0] == 'w'):
                moves.append(Move((row, col), (row+1, col-2), self.board))
        # check left
        if col+2 < n:
            if row-1 >= 0 and (self.board[row-1][col+2] == '--' or self.board[row-1][col+2][0] == 'w'):
                moves.append(Move((row, col), (row-1, col+2), self.board))
            if row+1 < n and (self.board[row+1][col+2] == '--' or self.board[row+1][col+2][0] == 'w'):
                moves.append(Move((row, col), (row+1, col+2), self.board))

# check all 8 squares for moves around the King at board[row][col]
# add moves to list
# to:do refactor
def getKingMoves_old(self, row, col, moves):
    n = len(self.board)
    # white king moves
    if self.whiteToMove:
        # check up
        if row-1 >= 0 and self.board[row-1][col][0] != 'w':
            moves.append(Move((row, col), (row-1, col), self.board))
        # check down
        if row+1 < n and self.board[row+1][col][0] != 'w':
            moves.append(Move((row, col), (row+1, col), self.board))
        # check right
        if col+1 < n and self.board[row][col+1][0] != 'w':
            moves.append(Move((row, col), (row, col+1), self.board))
        # check left
        if col-1 >= 0 and self.board[row][col-1][0] != 'w':
            moves.append(Move((row, col), (row, col-1), self.board))

        # check up right
        if row-1 >= 0 and col+1 < n and self.board[row-1][col+1][0] != 'w':
            moves.append(Move((row, col), (row-1, col+1), self.board))
        # check up left
        if row-1 >= 0 and col-1 >= 0 and self.board[row-1][col-1][0] != 'w':
            moves.append(Move((row, col), (row-1, col-1), self.board))
        # check down right
        if row+1 < n and col+1 < n and self.board[row+1][col+1][0] != 'w':
            moves.append(Move((row, col), (row+1, col+1), self.board))
        # check down left
        if row+1 < n and col-1 < n and self.board[row+1][col-1][0] != 'w':
            moves.append(Move((row, col), (row+1, col-1), self.board))
    # black king moves
    else:
        # check up
        if row-1 >= 0 and self.board[row-1][col][0] != 'b':
            moves.append(Move((row, col), (row-1, col), self.board))
        # check down
        if row+1 < n and self.board[row+1][col][0] != 'b':
            moves.append(Move((row, col), (row+1, col), self.board))
        # check right
        if col+1 < n and self.board[row][col+1][0] != 'b':
            moves.append(Move((row, col), (row, col+1), self.board))
        # check left
        if col-1 >= 0 and self.board[row][col-1][0] != 'b':
            moves.append(Move((row, col), (row, col-1), self.board))

        # check up right
        if row-1 >= 0 and col+1 < n and self.board[row-1][col+1][0] != 'b':
            moves.append(Move((row, col), (row-1, col+1), self.board))
        # check up left
        if row-1 >= 0 and col-1 >= 0 and self.board[row-1][col-1][0] != 'b':
            moves.append(Move((row, col), (row-1, col-1), self.board))
        # check down right
        if row+1 < n and col+1 < n and self.board[row+1][col+1][0] != 'b':
            moves.append(Move((row, col), (row+1, col+1), self.board))
        # check down left
        if row+1 < n and col-1 < n and self.board[row+1][col-1][0] != 'b':
            moves.append(Move((row, col), (row+1, col-1), self.board))

# get diagonal possible moves for a piece
# to:do refactor
def getDiagonal_old(self, row, col, moves):
    n = len(self.board)

    # white piece moves
    if self.whiteToMove:
        # check up and right
        rminu = row - 1
        cplus = col + 1
        while rminu >= 0 and cplus < n:
            piece = self.board[rminu][cplus]
            if piece == '--':
                moves.append(Move((row, col), (rminu, cplus), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (rminu, cplus), self.board))
                break
            elif piece[0] == 'w':
                break
            rminu -= 1
            cplus += 1

        # check up and left
        rminu = row - 1
        cminu = col - 1
        while rminu >= 0 and cminu < n:
            piece = self.board[rminu][cminu]
            if piece == '--':
                moves.append(Move((row, col), (rminu, cminu), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (rminu, cminu), self.board))
                break
            elif piece[0] == 'w':
                break
            rminu -= 1
            cminu -= 1

        # check down and right
        rplus = row + 1
        cplus = col + 1
        while rplus < n and cplus < n:
            piece = self.board[rplus][cplus]
            if piece == '--':
                moves.append(Move((row, col), (rplus, cplus), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (rplus, cplus), self.board))
                break
            elif piece[0] == 'w':
                break
            rplus += 1
            cplus += 1

        # check down and left
        rplus = row + 1
        cminu = col - 1
        while rplus < n and cminu >= 0:
            piece = self.board[rplus][cminu]
            if piece == '--':
                moves.append(Move((row, col), (rplus, cminu), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (rplus, cminu), self.board))
                break
            elif piece[0] == 'w':
                break
            rplus += 1
            cminu -= 1

    # black piece moves
    else:
        # check up and right
        rminu = row - 1
        cplus = col + 1
        while rminu >= 0 and cplus < n:
            piece = self.board[rminu][cplus]
            if piece == '--':
                moves.append(Move((row, col), (rminu, cplus), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (rminu, cplus), self.board))
                break
            elif piece[0] == 'b':
                break
            rminu -= 1
            cplus += 1

        # check up and left
        rminu = row - 1
        cminu = col - 1
        while rminu >= 0 and cminu < n:
            piece = self.board[rminu][cminu]
            if piece == '--':
                moves.append(Move((row, col), (rminu, cminu), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (rminu, cminu), self.board))
                break
            elif piece[0] == 'b':
                break
            rminu -= 1
            cminu -= 1

        # check down and right
        rplus = row + 1
        cplus = col + 1
        while rplus < n and cplus < n:
            piece = self.board[rplus][cplus]
            if piece == '--':
                moves.append(Move((row, col), (rplus, cplus), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (rplus, cplus), self.board))
                break
            elif piece[0] == 'b':
                break
            rplus += 1
            cplus += 1

        # check down and left
        rplus = row + 1
        cminu = col - 1
        while rplus < n and cminu >= 0:
            piece = self.board[rplus][cminu]
            if piece == '--':
                moves.append(Move((row, col), (rplus, cminu), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (rplus, cminu), self.board))
                break
            elif piece[0] == 'b':
                break
            rplus += 1
            cminu -= 1

# get horizontal possible moves for a piece
# to:do refactor
def getHorizontal_old(self, row, col, moves):
    n = len(self.board)
    # white piece moves
    if self.whiteToMove:
        #print("white piece at: " + str(row) + "," + str(col))
        # check right
        for i in range(col+1, n):
            piece = self.board[row][i]
            #print("right: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif piece[0] == 'w':
                break
        # check left
        for i in reversed(range(col)):
            piece = self.board[row][i]
            #print("left: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif piece[0] == 'w':
                break
    # black piece moves
    else:
        #print("black rook at: " + str(row) + "," + str(col))
        # check right
        for i in range(col+1, n):
            piece = self.board[row][i]
            #print("right: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif piece[0] == 'b':
                break
        # check left
        for i in reversed(range(col)):
            piece = self.board[row][i]
            #print("left: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (row, i), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (row, i), self.board))
                break
            elif piece[0] == 'b':
                break

# get vertical possible moves for a piece
# to:do refactor
def getVertical_old(self, row, col, moves):
    n = len(self.board)
    # white piece moves
    if self.whiteToMove:
        #print("white rook at: " + str(row) + "," + str(col))
        # check up
        for i in reversed(range(row)):
            piece = self.board[i][col]
            #print("up: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif piece[0] == 'w':
                break
        # check down
        for i in range(row+1, n):
            piece = self.board[i][col]
            #print("down: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif piece[0] == 'b':
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif piece[0] == 'w':
                break
    # black piece moves
    else:
        #print("black rook at: " + str(row) + "," + str(col))
        # check up
        for i in reversed(range(row)):
            piece = self.board[i][col]
            #print("up: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif piece[0] == 'b':
                break
        # check down
        for i in range(row+1, n):
            piece = self.board[i][col]
            #print("down: " + piece)
            if piece == '--':
                moves.append(Move((row, col), (i, col), self.board))
            elif piece[0] == 'w':
                moves.append(Move((row, col), (i, col), self.board))
                break
            elif piece[0] == 'b':
                break

    # all moves without considering checks
    # consider all moves that are possible based on how a piece is legally allowed to move
    """
    def get_all_possible_moves(self):
        # moves = [Move((6,4), (4,4), self.board)]
        moves = []
        # check all pieces on our board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # find the colour of the piece
                turn = self.board[row][col][0]
                if(turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    # get the piece type
                    piece = self.board[row][col][1]
                    # calls the appropriate move function based on the piece type
                    self.move_functions[piece](row, col, moves)
        return moves
    """

# AI --------------------------------------------------------------------------

EVALUTATOR = 1

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

simple_piece_value = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'P': 1
}

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

# CHESSMAIN -------------------
 #move_keyboard_input = []
    # some turbo mad shit
    if e.key == p.K_RETURN:
        print()
        print("commit move")
        print(move_keyboard_input)
        move_keyboard_input.clear()
    if e.key == p.K_a:
        print('a', end='')
        move_keyboard_input.append('a')
    if e.key == p.K_b:
        print('b', end='')
        move_keyboard_input.append('b')
    if e.key == p.K_c:
        print('c', end='')
        move_keyboard_input.append('c')
    if e.key == p.K_d:
        print('d', end='')
        move_keyboard_input.append('d')
    if e.key == p.K_e:
        print('e', end='')
        move_keyboard_input.append('e')
    if e.key == p.K_f:
        print('f', end='')
        move_keyboard_input.append('f')
    if e.key == p.K_g:
        print('g', end='')
        move_keyboard_input.append('g')
    if e.key == p.K_h:
        print('h', end='')
        move_keyboard_input.append('h')
    if e.key == p.K_1:
        print('1')
        move_keyboard_input.append('1')
    if e.key == p.K_2:
        print('2')
        move_keyboard_input.append('2')
    if e.key == p.K_3:
        print('3')
        move_keyboard_input.append('3')
    if e.key == p.K_4:
        print('4')
        move_keyboard_input.append('4')
    if e.key == p.K_5:
        print('5')
        move_keyboard_input.append('5')
    if e.key == p.K_6:
        print('6')
        move_keyboard_input.append('6')
    if e.key == p.K_7:
        print('7')
        move_keyboard_input.append('7')
    if e.key == p.K_8:
        print('8')
        move_keyboard_input.append('8')


    # if youre playing vs a bot, undo the the last two moves
    #if not playerW or not playerB:
    #    gs.undo_move()

# Main driver
# User input
# Updates gfx
def play(playerW, playerB):   
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()

    # do this once before the game while loop
    load_images()
    #draw on console first time
    print_board(gs.board)
    
    # generate valid moves
    valid_moves = gs.get_valid_moves()
    # flag var for when a move is made
    move_made = False
    #animation flag
    animate = False
    game_started = False
    # keep track of last square clicked tuple(row, col)
    square_selected = ()
   
    # track player clicks, two tuples 
    player_clicks = []
    running = True
    player_turn_change = True
    game_end = False
    move_undone = False
    # flags for multiprocessing
    ai_thinking = False
    move_finder_process = None

    while running:
        # checking if the player is human or not
        human_turn = (gs.white_to_move and playerW) or (not gs.white_to_move and playerB)
        
        # stuff to print out the first time the loop gets run
        if player_turn_change:
            player_turn_change = False
            print("Turn " + str(gs.turn_counter))
            if gs.checkmate:
                print("checkmate.")
                game_end = True
            elif gs.stalemate:
                print("stalemate.")
                game_end = True
            else:
                if gs.white_to_move:
                    print("white to move")
                else:
                    print("black to move")


        for e in p.event.get():
            if (e.type == p.QUIT) or (e.type == p.KEYDOWN and e.key == p.K_q):
                running = False
                gs.print_move_log()
                if ai_thinking:
                    move_finder_process.terminate()
                    ai_thinking = False
                move_undone = True
                #print(gs.moveLog)
            # mouse input
            elif e.type == p.MOUSEBUTTONDOWN:
                # so that the human player can't click on stuff while the bot is thinking
                if human_turn:
                    # get (x,y) location of the mouse
                    mousepos = p.mouse.get_pos()
                    row = mousepos[1]//SQ_SIZE
                    col = mousepos[0]//SQ_SIZE
                    # check if same square selected
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        curr_move = Engine.Move(square_selected, (0,0), gs.board)
                        print("\t" + curr_move.get_rank_file(square_selected[0], square_selected[1]))
                        # append both 1st and 2nd click
                        player_clicks.append(square_selected)
                    # after second click
                    if len(player_clicks) == 2:
                        # the engine makes the move
                        move = Engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            # check that the move selected is actually valid
                            if move == valid_moves[i]:
                                print("Moved: " + move.get_chess_notation())
                                # change castle flag
                                if valid_moves[i].is_castle_move:
                                    move.is_castle_move = True
                                gs.make_move(move)
                                # if is a pawn promotion ask user what to promote?
                                move_made = True
                                animate = True
                                # reset the user clicks
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            #print("invalid move")
                            player_clicks = [square_selected]
                    
            # keyboard input
            elif e.type == p.KEYDOWN:
                # undo when z is pressed
                if e.key == p.K_z:
                    gs.undo_move()
                    # prevent this from printing again
                    #draw on console again
                    print("undo")
                    print_board(gs.board)
                    #valid_moves = gs.get_valid_moves()
                    move_made = True
                    animate = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True    
                # reset the board
                if e.key == p.K_r:
                    if game_started:
                        gs.print_move_log()
                        gs = Engine.GameState()
                        valid_moves = gs.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_started = False
                        game_end = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = False
                        move_finder_process = None
                        player_turn_change = True
                        if not playerW or not playerB:
                            ai_thinking = False

        # AI move finder logic
        if not game_end and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                print("Calculating...")
                # multi threading
                returnQueue = Queue()
                move_finder_process = Process(target=AIMoveFinder.get_best_move_minmax, args=(gs, valid_moves, returnQueue))
                move_finder_process.start()
                #AIMove = AIMoveFinder.find_random_move(valid_moves)
                #AIMove = AIMoveFinder.findGreedyMove(gs, valid_moves)
                #AIMove = AIMoveFinder.findMinMaxDepth2Move(gs, valid_moves)
                #AIMove = AIMoveFinder.get_best_move_minmax(gs, valid_moves)

            if not move_finder_process.is_alive():
                ai_move = returnQueue.get()    
                if ai_move is None:
                    ai_move = AIMoveFinder.find_random_move(valid_moves)
                gs.make_move(ai_move)
                print("Moved: " + ai_move.get_chess_notation())
                move_made = True
                animate = True
                ai_thinking = False


        if move_made:
            #animate da move
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            # gen new set of valid moves
            print("pieces left: ", gs.num_pieces_left)
            valid_moves = gs.get_valid_moves()
            move_made = False
            game_started = True
            animate = False
            move_undone = False
            # reset to print out who moves again
            player_turn_change = True
            # draw to console
            print_board(gs.board)

        draw_game_state(screen, gs, valid_moves, square_selected)
        clock.tick(MAX_FPS)
        p.display.flip()

# Draw the pieces to the command line
def print_board(board):    
    # Because we call it twice
    def print_letters():
        print("  ", end='')
        for letter in string.ascii_uppercase:
            print(letter + ' ', end = ' ')
            if(letter == 'H'):
                break
        print()

    n = len(board)
    print_letters()
    for i in range(n + 1):
        if i < 8:
            print(str(Engine.Move.rows_to_ranks[i]), end = ' ')
            for j in range(n):
                print(board[i][j], end = ' ')
            print(str(Engine.Move.rows_to_ranks[i]), end = ' ') 
            print()
    print_letters()
    print('', end = '\n\n')

# zobrist -----------------------------------------------------------------------------------------
'''
if __name__ == "__main__":
    # create a chess board
    #board = chess.Board()
    board1 = [
        ['bR','bN','bB','bQ','bK','bB','bN','bR'],
        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        ['--','--','--','--','--','--','--','--'],
        ['--','--','--','--','--','--','--','--'],
        ['--','--','--','--','--','--','--','--'],
        ['--','--','--','--','--','--','--','--'],
        ['wP','wP','wP','wP','wP','wP','wP','wP'],
        ['wR','wN','wB','wQ','wK','wB','wN','wR']
    ]

    board2 = [
        ['bR','bN','bB','bQ','bK','bB','bN','bR'],
        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        ['--','--','--','--','--','--','--','--'],
        ['--','--','--','--','--','--','--','--'],
        ['--','--','--','wP','--','--','--','--'],
        ['--','--','--','--','--','--','--','--'],
        ['wP','wP','wP','--','wP','wP','wP','wP'],
        ['wR','wN','wB','wQ','wK','wB','wN','wR']
    ]

    table = {}

    # create a ZobristHash object
    zobrist = ZobristHash()

    # get the Zobrist hash of the board
    #hash_value = zobrist.hash(board1, True, CastlingRights(True, True, True, True))
    hash_value = ZobristHash().hash(board1, True, CastlingRights(True, True, True, True))
    print(hash_value)

    #hash_value = zobrist.hash(board2, False, CastlingRights(True, True, True, True))
    hash_value = ZobristHash().hash(board2, False, CastlingRights(True, True, True, True))
    print(hash_value)

    #hash_value = zobrist.hash(board1, True, CastlingRights(True, True, True, True))
    hash_value = ZobristHash().hash(board1, True, CastlingRights(True, True, True, True))
    print(hash_value)
'''

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

                '''
        if board.turn == chess.BLACK:
            hash_value ^= self.side_key
        '''

        '''
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                piece_type = piece.symbol().upper()
                hash_value ^= self.piece_keys[(piece_type, i)]
        '''