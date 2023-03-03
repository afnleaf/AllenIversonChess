# constants
# checkmate needs to be higher than anything
CHECKMATE = 100000
STALEMATE = 0
# 2 is pretty fast
# default 3 is usable but runs up to 90 seconds on my machine
# 4 is too slow without adding more optimizations to the game
DEPTH = 3
# increasing this increases the weight of the above positional matrices
POSITIONAL_SCORE_FACTOR = 8
# default limit of 30 seconds per move
TIMELIMIT = 30.0