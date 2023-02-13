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