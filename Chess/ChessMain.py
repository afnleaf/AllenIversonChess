"""
Main driver
Handle user input and gamestate.
"""

import sys
import string
import pygame as p
import Engine

# size of window
WIDTH = HEIGHT = 512
# 8x8 board
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
# animations
MAX_FPS = 15
IMAGES = {}


# Init global dictionary of chess piece images.
# Called once in main.
def loadImages():
    pieces = ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # Can access image by calling dictionary "IMAGES['wP']"


# Main driver
# User input
# Updates gfx
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()

    # generate valid moves
    validMoves = gs.getValidMoves()
    # flag var for when a move is made
    moveMade = False

    # do this once before the game while loop
    loadImages()

    #draw on console first time
    printBoard(gs.board)
    
    # keep track of last square clicked tuple(row, col)
    squareSelected = ()
    moveKeyboardIn = []
    # track player clicks, two tuples 
    playerClicks = []
    running = True
    playerTurnChange = True
    gameEnd = False
    while running:
        # stuff to print out the first time the loop gets run
        if playerTurnChange:
            playerTurnChange = False
            if gs.checkMate:
                print("checkmate.")
            elif gs.staleMate:
                print("stalemate.")
            else:
                if gs.whiteToMove:
                    print("white to move")
                else:
                    print("black to move")
        for e in p.event.get():
            if (e.type == p.QUIT) or (e.type == p.KEYDOWN and e.key == p.K_q):
                running = False
                print("Move log:")
                gs.printMoveLog()
                #print(gs.moveLog)
            # mouse input
            elif e.type == p.MOUSEBUTTONDOWN:
                # get (x,y) location of the mouse
                mousepos = p.mouse.get_pos()
                row = mousepos[1]//SQ_SIZE
                col = mousepos[0]//SQ_SIZE
                # check if same square selected
                if squareSelected == (row, col):
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    currMove = Engine.Move(squareSelected, (0,0), gs.board)
                    print("\t" + currMove.getRankFile(squareSelected[0], squareSelected[1]))
                    # append both 1st and 2nd click
                    playerClicks.append(squareSelected)
                # after second click
                if len(playerClicks) == 2:
                    # the engine makes the move
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        # check that the move selected is actually valid
                        if move == validMoves[i]:
                        #if move in validMoves:
                            print("Moved: " + move.getChessNotation())
                            # change castle flag
                            if validMoves[i].isCastleMove:
                                move.isCastleMove = True
                            gs.makeMove(move)
                            #print("test")
                            #print(move.isCastleMove)
                            # if is a pawn promotion ask user what to promote?
                            moveMade = True
                            # draw to console
                            printBoard(gs.board)
                            # reset the user clicks
                            squareSelected = ()
                            playerClicks = []
                    if not moveMade:
                        #print("invalid move")
                        playerClicks = [squareSelected]
                    
            # keyboard input
            elif e.type == p.KEYDOWN:
                # undo when z is pressed
                if e.key == p.K_z:
                    gs.undoMove()
                    # prevent this from printing again
                    #draw on console again
                    print("undo")
                    printBoard(gs.board)
                    #validMoves = gs.getValidMoves()
                    moveMade = True
                # some turbo mad shit
                if e.key == p.K_RETURN:
                    print()
                    print("commit move")
                    print(moveKeyboardIn)
                    moveKeyboardIn.clear()
                if e.key == p.K_a:
                    print('a', end='')
                    moveKeyboardIn.append('a')
                if e.key == p.K_b:
                    print('b', end='')
                    moveKeyboardIn.append('b')
                if e.key == p.K_c:
                    print('c', end='')
                    moveKeyboardIn.append('c')
                if e.key == p.K_d:
                    print('d', end='')
                    moveKeyboardIn.append('d')
                if e.key == p.K_e:
                    print('e', end='')
                    moveKeyboardIn.append('e')
                if e.key == p.K_f:
                    print('f', end='')
                    moveKeyboardIn.append('f')
                if e.key == p.K_g:
                    print('g', end='')
                    moveKeyboardIn.append('g')
                if e.key == p.K_h:
                    print('h', end='')
                    moveKeyboardIn.append('h')
                if e.key == p.K_1:
                    print('1')
                    moveKeyboardIn.append('1')
                if e.key == p.K_2:
                    print('2')
                    moveKeyboardIn.append('2')
                if e.key == p.K_3:
                    print('3')
                    moveKeyboardIn.append('3')
                if e.key == p.K_4:
                    print('4')
                    moveKeyboardIn.append('4')
                if e.key == p.K_5:
                    print('5')
                    moveKeyboardIn.append('5')
                if e.key == p.K_6:
                    print('6')
                    moveKeyboardIn.append('6')
                if e.key == p.K_7:
                    print('7')
                    moveKeyboardIn.append('7')
                if e.key == p.K_8:
                    print('8')
                    moveKeyboardIn.append('8')

        if moveMade:
            # gen new set of valid moves
            validMoves = gs.getValidMoves()
            moveMade = False
            # reset to print out who moves again
            playerTurnChange = True

        drawGameState(screen, gs, validMoves, squareSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


# highlight squares visually so that the player knows what moves are valid
def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        row, col = squareSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected squares
            square = p.Surface((SQ_SIZE, SQ_SIZE))
            square.set_alpha(100)
            square.fill(p.Color('red'))
            screen.blit(square, (col*SQ_SIZE, row*SQ_SIZE))
            # highlight valid moves coming from that square
            square.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(square, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


# Responsible for graphics of the current game state
def drawGameState(screen, gs, validMoves, squareSelected):
    # draw graphical game state
    # draw squares
    drawBoard(screen)
    # add in piece highlightsF
    highlightSquares(screen, gs, validMoves, squareSelected)
    # add in move suggestions
    # draw pieces on top of the squares
    drawPieces(screen, gs.board)


# draw the squares
# call this before drawPieces()
def drawBoard(screen):
    # top left square is light
    colors = [p.Color("#fceaa8"), p.Color("#145f4e")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# draw the pieces using the current game state data
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            # check for empty square
            if piece != '--':
                # what is blit()
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# draw the pieces to the command line
def printBoard(board):    
    # because we call it twice letters
    def printLetters():
        print("  ", end='')
        for letter in string.ascii_uppercase:
            print(letter + ' ', end = ' ')
            if(letter == 'H'):
                break
        print()

    n = len(board)
    printLetters()
    for i in range(n + 1):
        if i < 8:
            print(str(Engine.Move.rowsToRanks[i]), end = ' ')
            for j in range(n):
                print(board[i][j], end = ' ')
            print(str(Engine.Move.rowsToRanks[i]), end = ' ') 
            print()
    printLetters()
    print('', end = '\n\n')


# animated moves
def animateMove(move, screen, board, clock):
    pass



# default notation
if __name__ == "__main__":
    main()


