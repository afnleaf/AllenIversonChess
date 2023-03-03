"""
Main driver
Handle user input and gamestate.
"""

import os
import sys
import string
import io
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
# stop welcome message before importing pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as p
from multiprocessing import Process, Queue
# my files
import Engine, AIMoveFinder

# size of window
WIDTH = HEIGHT = 720
# 8x8 board
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
# animations
MAX_FPS = 60
IMAGES = {}




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


# Init global dictionary of chess piece images.
# Called once in main.
def load_images():
    for piece in ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']:
        # Can access image by calling dictionary "IMAGES['wP']"
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    

# draw graphical game state
def draw_game_state(screen, gs, valid_moves, square_selected):
    # draw squares
    draw_board_base(screen)
    # add on piece highlights
    highlight_squares(screen, gs, valid_moves, square_selected)
    # draw pieces on top of the squares
    draw_pieces(screen, gs.board)


# draw the squares
# call this before draw_pieces()
def draw_board_base(screen):
    global colors
    # top left square is light
    colors = [p.Color("#fceaa8"), p.Color("#145f4e")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            square = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, square)


# highlight squares visually so that the player knows what moves are valid
def highlight_squares(screen, gs, valid_moves, square_selected):
    # not empty
    if square_selected:
        row, col = square_selected
        piece = gs.board[row][col]
        if piece != '--' and piece.startswith('w' if gs.white_to_move else 'b'):
            # highlight selected square
            selected_square = p.Surface((SQ_SIZE, SQ_SIZE))
            selected_square.set_alpha(100)
            selected_square.fill(p.Color('red'))
            screen.blit(selected_square, (col*SQ_SIZE, row*SQ_SIZE))

            # highlight valid moves coming from that square
            valid_square = p.Surface((SQ_SIZE, SQ_SIZE))
            valid_square.set_alpha(100)
            valid_square.fill(p.Color('blue'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(valid_square, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))


# draw the pieces using the current board data
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            # check for empty square
            if piece != '--':
                piece_to_draw = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                screen.blit(IMAGES[piece], piece_to_draw)


# draw the pieces to the command line
def print_board(board):    
    # because we call it twice letters
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


# animated moves
def animate_move(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 4
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square

    for frame in range(frame_count + 1):
        row = move.start_row + (d_row * (frame / frame_count))
        col = move.start_col + (d_col * (frame / frame_count))
        draw_board_base(screen)
        draw_pieces(screen, board)

        # erase piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)

        # draw piece on rectangle
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)

        # draw moving piece
        moving_piece = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        screen.blit(IMAGES[move.piece_moved], moving_piece)
        p.display.flip()
        clock.tick(60)


# let the user choose the game mode before the game loads up
def choose_game_mode():
    print("1. White and Black are played by humans.")
    print("2. White is played by human, Black is played by the computer.")
    print("3. White is played by the computer, Black is played by human.")
    print("4. White and Black are played by the computer.")

    choice = int(input())
    if choice == 1:
        return True, True
    elif choice == 2:
        return True, False
    elif choice == 3:
        return False, True
    elif choice == 4:
        return False, False
    else:
        print("Invalid input. Please enter a number between 1 and 4.")
        return choose_game_mode()

def main():
    # choose players
    playerW,playerB = choose_game_mode()
    print("Make sure you bring the pygame window to front.", end="\n\n")

    play(playerW, playerB)

# default notation
if __name__ == "__main__":
    main()
