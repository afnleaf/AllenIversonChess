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

# Handles the initialization of the gamestate
# Contains the player keyboard functions
# Loops the game
class GameLoop():
    
    # init the game state and the flags that go with it
    def __init__(self, playerW, playerB):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.gs = Engine.GameState()

        # do this once before the game while loop
        load_images()
        #draw on console first time
        print_board(self.gs.board)
        
        self.playerW = playerW
        self.playerB = playerB

        # keep track of last square clicked tuple(row, col)
        self.square_selected = ()
        # track player clicks, two tuples 
        self.player_clicks = []
        
        # Flags
        self.move_made = False
        self.animate = False
        self.game_started = False
        self.player_turn_change = True
        self.game_end = False
        self.move_undone = False
        self.running = True
        # flags for multiprocessing
        self.ai_thinking = False
        self.move_finder_process = None    

    # Quitting the game.
    def quit(self):
        print("Quitting game.")
        self.kill_process()
        self.running = False
        self.game_end= True
        self.gs.print_move_log()


    # Undoing a move.
    def undo(self):
        self.gs.undo_move()
        # prevent this from printing again
        #draw on console again
        print("undo")
        print_board(self.gs.board)
        #valid_moves = gs.get_valid_moves()
        self.move_made = True
        self.animate = False
        self.kill_process()
        self.move_undone = True
    

    # Resetting the game state to the start.
    def reset(self):
        self.gs.print_move_log()
        self.gs = Engine.GameState()
        self.square_selected = ()
        self.player_clicks = []
        self.move_made = False
        self.animate = False
        self.game_started = False
        self.game_end = False
        self.kill_process()
        self.move_undone = False
        self.move_finder_process = None
        self.player_turn_change = True
        if not self.playerW or not self.playerB:
            self.ai_thinking = False

        return self.gs.get_valid_moves()

    # handle the ai thinking process
    def kill_process(self):
        if self.ai_thinking:
            self.move_finder_process.terminate()
            self.ai_thinking = False


    # stuff to print out the first time the loop gets run
    def on_first_run(self):
        if self.player_turn_change:
            self.player_turn_change = False
            print("Turn ", str(self.gs.turn_counter))
            # even if game ends we need to keep the loop running for keybinds
            if self.gs.checkmate:
                print("Checkmate.")
                self.game_end = True
            elif self.gs.stalemate:
                print("Stalemate.")
                self.game_end = True
            else:
                if self.gs.white_to_move:
                    print("white to move")
                else:
                    print("black to move")

    def player_input(self, valid_moves):
        # get (x,y) location of the mouse
        mousepos = p.mouse.get_pos()
        row = mousepos[1]//SQ_SIZE
        col = mousepos[0]//SQ_SIZE
        # check if same square selected
        if self.square_selected == (row, col):
            self.square_selected = ()
            self.player_clicks = []
        else:
            self.square_selected = (row, col)
            curr_move = Engine.Move(self.square_selected, (0,0), self.gs.board)
            print("\t" + curr_move.get_rank_file(self.square_selected[0], self.square_selected[1]))
            # append both 1st and 2nd click
            self.player_clicks.append(self.square_selected)
        # after second click
        if len(self.player_clicks) == 2:
            # the engine makes the move
            move = Engine.Move(self.player_clicks[0], self.player_clicks[1], self.gs.board)
            for i in range(len(valid_moves)):
                # check that the move selected is actually valid
                if move == valid_moves[i]:
                    print("Moved: " + move.get_chess_notation())
                    # change castle flag
                    if valid_moves[i].is_castle_move:
                        move.is_castle_move = True
                    self.gs.make_move(move)
                    # if is a pawn promotion ask user what to promote?
                    self.move_made = True
                    self.animate = True
                    # reset the user clicks
                    self.square_selected = ()
                    self.player_clicks = []
            if not self.move_made:
                #print("invalid move")
                self.player_clicks = [self.square_selected]


    # hanles changing sides and turn animation
    def when_move_made(self):
        #animate the move
        if self.animate:
            animate_move(self.gs.move_log[-1], self.screen, self.gs.board, self.clock)
        print("pieces left: ", self.gs.num_pieces_left)
        self.move_made = False
        self.game_started = True
        self.animate = False
        self.move_undone = False
        # reset to print out who moves again
        self.player_turn_change = True
        # draw to console
        print_board(self.gs.board)

        # gen new set of valid moves
        return self.gs.get_valid_moves()


    # the game playing loop
    def play(self):
        # on first run generate valid moves
        valid_moves = self.gs.get_valid_moves()

        while self.running:
            # checking if the player is human or not
            human_turn = (self.gs.white_to_move and self.playerW) or (not self.gs.white_to_move and self.playerB)
            
            self.on_first_run()
            
            for e in p.event.get():
                # quitting the game
                if (e.type == p.QUIT) or (e.type == p.KEYDOWN and e.key == p.K_q):
                    self.quit()
                # mouse input
                elif e.type == p.MOUSEBUTTONDOWN:
                    # so that the human player can't click on stuff while the bot is thinking
                    if human_turn:
                        self.player_input(valid_moves)
                # keyboard input
                elif e.type == p.KEYDOWN:
                    # undo when z is pressed
                    if e.key == p.K_z:
                        self.undo() 
                    # reset the board
                    if e.key == p.K_r:
                        if self.game_started:
                            valid_moves = self.reset()

            # AI move finder logic
            if not self.game_end and not human_turn and not self.move_undone:
                if not self.ai_thinking:
                    self.ai_thinking = True
                    print("Calculating...")
                    # multi threading
                    returnQueue = Queue()
                    self.move_finder_process = Process(target=AIMoveFinder.get_best_move_minmax, args=(self.gs, valid_moves, returnQueue))
                    self.move_finder_process.start()

                if not self.move_finder_process.is_alive():
                    ai_move = returnQueue.get()    
                    if ai_move is None:
                        ai_move = AIMoveFinder.find_random_move(valid_moves)
                    self.gs.make_move(ai_move)
                    print("Moved: " + ai_move.get_chess_notation())
                    self.move_made = True
                    self.animate = True
                    self.ai_thinking = False

            if self.move_made:
                 valid_moves = self.when_move_made()

            draw_game_state(self.screen, self.gs, valid_moves, self.square_selected)
            self.clock.tick(MAX_FPS)
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
    #load_game(playerW, playerB)

    game = GameLoop(playerW, playerB)
    game.play()

# default notation
if __name__ == "__main__":
    main()
