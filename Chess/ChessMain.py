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
    # do this once before the game while loop
    loadImages()

    #draw on CLI first time
    printBoard(gs.board)
    
    # keep track of last square clicked tuple(row, col)
    squareSelected = ()
    # track player clicks, two tuples 
    playerClicks = []
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                print("Move log:")
                print(gs.moveLog)
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
                    # append both 1st and 2nd click
                    playerClicks.append(squareSelected)
                # after second click
                if len(playerClicks) == 2:
                    # the engine makes the move
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    gs.makeMove(move)
                    # draw to cli
                    printBoard(gs.board)
                    print(move.getChessNotation())
                    # reset the user clicks
                    squareSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# Responsible for graphics of the current game state
def drawGameState(screen, gs):
    # draw graphical game state
    # draw squares
    drawBoard(screen)
    # add in piece highlights 
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
    n = len(board)
    for i in range(n + 1):
        if i < 8:
            #print(str(i + ((i+1)*8)), end = ' ')
            print(str(Engine.Move.rowsToRanks[i]), end = ' ')
            for j in range(n):
                print(board[i][j], end = ' ')
            print()
    # add letters at bottom
    print("  ", end="")
    for letter in string.ascii_uppercase:
        print(letter + ' ', end = ' ')
        if(letter == 'H'):
            break
    print()

# default notation
if __name__ == "__main__":
    main()


