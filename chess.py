import sys
import string

def printBlankBoard():
    n = 8
    for r in range(n):
        print(r+1, end = " ")
        for c in range(n):
            print(".", end = " ")
        print()
    
    # add letters at bottom
    print("  ", end="")
    for letter in string.ascii_uppercase:
        print(letter, end =" ")
        if(letter == 'H'):
            break
    print()

printBlankBoard()
print()

def printBoard(board):
    n = len(board)
    for i in range(n + 1):
        if i != 8:
            print(str(i+1), end = ' ')
            for j in range(n):
                print(start_board[i][j], end = ' ')
            print()
    # add letters at bottom
    print("  ", end="")
    for letter in string.ascii_uppercase:
        print(letter + ' ', end = ' ')
        if(letter == 'H'):
            break
    print()

letters = [' ','A ','B ','C ','D ','E ','F ','G ','H ']

start_board = [['wR','wN','wB','wQ','wK','wB','wN','wR'],
               ['wP','wP','wP','wP','wP','wP','wP','wP'],
               ['. ','. ','. ','. ','. ','. ','. ','. '],
               ['. ','. ','. ','. ','. ','. ','. ','. '],
               ['. ','. ','. ','. ','. ','. ','. ','. '],
               ['. ','. ','. ','. ','. ','. ','. ','. '],
               ['bP','bP','bP','bP','bP','bP','bP','bP'],
               ['bR','bN','bB','bQ','bK','bB','bN','bR']]

board = start_board
printBoard(board)

