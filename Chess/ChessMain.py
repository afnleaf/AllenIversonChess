"""
Main driver
Handle user input and gamestate.
"""

import os
import sys
import string
import pygame as p
from multiprocessing import Process, Queue
# my files
import Engine, AIMoveFinder

# size of window
WIDTH = HEIGHT = 512
# 8x8 board
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
# animations
MAX_FPS = 15
IMAGES = {}
# stop welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

    # choose players
    print("1. White and Black are played by humans.")
    print("2. White is played by human, Black is played by the computer.")
    print("3. White is played by the computer, Black is played by human.")
    print("4. White and Black are played by the computer.")
    
    validChoice = False
    while not validChoice:
        choice = input()
        # if a human is playing, then true
        # if an AI is playing then false
        if(int(choice) == 1):
            playerW = True
            playerB = True
            validChoice = True
        elif(int(choice) == 2):
            playerW = True
            playerB = False
            validChoice = True
        elif(int(choice) == 3):
            playerW = False
            playerB = True
            validChoice = True
        elif(int(choice) == 4):
            playerW = False
            playerB = False
            validChoice = True
    
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()

    # generate valid moves
    validMoves = gs.getValidMoves()
    # flag var for when a move is made
    moveMade = False

    #animation flag
    animate = False

    gameStarted = False

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
    moveUndone = False
    # flags for multiprocessing
    AIThinking = False
    moveFinderProcess = None

    while running:
        # checking if the player is human or not
        humanTurn = (gs.whiteToMove and playerW) or (not gs.whiteToMove and playerB)
        
        # stuff to print out the first time the loop gets run
        if playerTurnChange:
            playerTurnChange = False
            print("Turn " + str(gs.turnCounter))
            if gs.checkMate:
                print("checkmate.")
                gameEnd = True
            elif gs.staleMate:
                print("stalemate.")
                gameEnd = True
            else:
                if gs.whiteToMove:
                    print("white to move")
                else:
                    print("black to move")


        for e in p.event.get():
            if (e.type == p.QUIT) or (e.type == p.KEYDOWN and e.key == p.K_q):
                running = False
                gs.printMoveLog()
                #print(gs.moveLog)
            # mouse input
            elif e.type == p.MOUSEBUTTONDOWN:
                # so that the human player can't click on stuff while the bot is thinking
                if humanTurn:
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
                                print("Moved: " + move.getChessNotation())
                                # change castle flag
                                if validMoves[i].isCastleMove:
                                    move.isCastleMove = True
                                gs.makeMove(move)
                                # if is a pawn promotion ask user what to promote?
                                moveMade = True
                                animate = True
                                gameStarted = True
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
                    animate = False
                    # if youre playing vs a bot, undo the the last two moves
                    if not playerW or not playerB:
                        gs.undoMove()
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True    
                # reset the board
                if e.key == p.K_r:
                    if gameStarted:
                        gs.printMoveLog()
                        gs = Engine.GameState()
                        validMoves = gs.getValidMoves()
                        squareSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameStarted = False
                        gameEnd = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True


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


        # AI move finder logic
        if not gameEnd and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("Calculating...")
                # multi threading
                returnQueue = Queue()
                moveFinderProcess = Process(target=AIMoveFinder.getBestMoveMinMax, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()
                #AIMove = AIMoveFinder.findRandomMove(validMoves)
                #AIMove = AIMoveFinder.findGreedyMove(gs, validMoves)
                #AIMove = AIMoveFinder.findMinMaxDepth2Move(gs, validMoves)
                #AIMove = AIMoveFinder.getBestMoveMinMax(gs, validMoves)

            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()    
                if AIMove is None:
                    AIMove = AIMoveFinder.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                print("Moved: " + AIMove.getChessNotation())
                moveMade = True
                animate = True
                AIThinking = False


        if moveMade:
            #animate da move
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            # gen new set of valid moves
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False
            # reset to print out who moves again
            playerTurnChange = True
            # draw to console
            printBoard(gs.board)


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
    global colors
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
    global colors
    dRow = move.endRow - move.startRow
    dCol = move.endCol - move.startCol
    framesPerSquare = 1
    frameCount = (abs(dRow) + abs(dCol) * framesPerSquare)
    for frame in range(frameCount + 1):
        row, col = (move.startRow + dRow*frame/frameCount, move.startCol + dCol*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw piece on rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    

# default notation
if __name__ == "__main__":
    main()
