# AllenIversonChess
Chess game. No enpassant or 3 move stalemate.

## AI Bot
- Nega Max Alpha Beta Pruning
- Evaluating on piece score and positional matrix.
- Depth of 3

## How to play
- Choose option:
    - 1. White and Black are played by humans.
    - 2. White is played by human, Black is played by the computer.
    - 3. White is played by the computer, Black is played by human.
    - 4. White and Black are played by the computer.
- Pull up the pygame window, for visuals and control as human player.

### keybinds
- q/Q
    - quit the game
    - print the move log
- r/R
    - resets the board and game state
- z/Z
    - undo a move, 2 if one player is the computer

## Dependencies
- pygame
- numpy

```
python -m pip install -r requirements.txt
or
pip install -r requirements.txt
```

## Running
Linux:
```
python3 Chess/ChessMain.py
```

Windows:
```
python .\Chess\ChessMain.py
```
