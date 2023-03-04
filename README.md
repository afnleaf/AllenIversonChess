# AllenIversonChess
Simple chess game with board visualization. No enpassant or 3 move stalemate.

## AI Bot
- Nega Max Alpha Beta Pruning
- Evaluating on piece score and positional matrix.
- Transposition table for valid moves only. Uses Zobrist hashing method.

### Configuration
Can be found in `config.py`.

- **CHECKMATE**: score related to checkmate, keep this as a very high number
- **STALEMATE**: keep this at 0
- **DEPTH**: 3 is a good default, anything above will be pretty slow to unusable. Try 2 for speed or 4 for fun.
- **POSITIONAL_SCORE_FACTOR**: How much weight is assigned to piece position.
- **TIMELIMIT**: default is 30, that goes well with depth of 3, which can occassionaly go beyond 30 seconds. 

## How to play
- Choose option:
    - (1) White and Black are played by humans.
    - (2) White is played by human, Black is played by the computer.
    - (3) White is played by the computer, Black is played by human.
    - (4) White and Black are played by the computer.
- Pull up the pygame window, for visuals and control as human player.

### Keybinds
- q/Q
    - Quit the game
    - Print the move log
- r/R
    - Resets the board and game state
- z/Z
    - Undo a move, 2 if one player is the computer

## Dependencies
Must install the following python packages to run this program.

- pygame (for the visualization)
- numpy (for the 2D board representation)

```
python -m pip install -r requirements.txt
or
pip install -r requirements.txt
```

## Running
Linux/macOS:
```
python3 Chess/ChessMain.py
```

Windows:
```
python .\Chess\ChessMain.py
```
