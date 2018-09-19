import os
##CONSTANTS
# Possible spaces on the board
BOUNDS_X = range(0, 4) # Possible values are 0, 1, 2, 3
BOUNDS_Y = range(0, 4) # Possible values are 0, 1, 2, 3
WINDOW_X = 600 # Window width
WINDOW_Y = 600 # Window height

TILE_COLOUR_1 = (114,78,34,1)
TILE_COLOUR_2 =(255,218,119,1)

PLAYER1_ADVANCER_ICON = 'icons/Advancer-White.png'
PLAYER2_ADVANCER_ICON = 'icons/Advancer-Black.png'

PLAYER1_ATTACKER_ICON = 'icons/Attacker-White.png'
PLAYER2_ATTACKER_ICON = 'icons/Attacker-Black.png'

PLAYER1_DEFENDER_ICON = 'icons/Defender-White.png'
PLAYER2_DEFENDER_ICON = 'icons/Defender-Black.png'

##GAME RULES
CAPTURE_OWN_PIECES = False
STALEMATE_ON_NO_LEGAL_MOVES = True
LOSE_ON_NO_LEGAL_MOVES = False
LOSE_ON_NO_PIECES = False