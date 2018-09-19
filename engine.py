#### DON'T FORGET TO ADD UNDERSCORES TO PRIVATE VARIABLES BEFORE UPLOAD###########
### PUT PIECE POSITIONS AND MOVES IN CONFIG
import config

# Possible spaces on the board
BOUNDS_X = config.BOUNDS_X
BOUNDS_Y = config.BOUNDS_Y

class GameBoard():
    '''
    '''
    def __init__(self):
        ''' Initializes game board object.
        '''
        # List of [plater1 pieces, player2 pieces]
        self.boardlist = []

    def initalizeDefaultBoard(self, player1, player2):
        '''(Player, Player, GameBoard) -> None
        Initializes game board with default piece position
        '''
        player2Pieces = [Advancer(0,0,player1,self), Attacker(1,0,player1,self),
                         Attacker(2,0,player1,self), Advancer(3,0,player1,self),
                         Defender(0,1,player1,self), Defender(3,1,player1,self)]
        player1Pieces = [Advancer(0,3,player2,self), Attacker(1,3,player2,self),
                         Attacker(2,3,player2,self), Advancer(3,3,player2,self),
                         Defender(0,2,player2,self), Defender(3,2,player2,self)]

        # Initialize Player icons
        player2Pieces[0].setIcon(config.PLAYER2_ADVANCER_ICON)
        player2Pieces[1].setIcon(config.PLAYER2_ATTACKER_ICON)
        player2Pieces[2].setIcon(config.PLAYER2_ATTACKER_ICON)
        player2Pieces[3].setIcon(config.PLAYER2_ADVANCER_ICON)
        player2Pieces[4].setIcon(config.PLAYER2_DEFENDER_ICON)
        player2Pieces[5].setIcon(config.PLAYER2_DEFENDER_ICON)

        player1Pieces[0].setIcon(config.PLAYER1_ADVANCER_ICON)
        player1Pieces[1].setIcon(config.PLAYER1_ATTACKER_ICON)
        player1Pieces[2].setIcon(config.PLAYER1_ATTACKER_ICON)
        player1Pieces[3].setIcon(config.PLAYER1_ADVANCER_ICON)
        player1Pieces[4].setIcon(config.PLAYER1_DEFENDER_ICON)
        player1Pieces[5].setIcon(config.PLAYER1_DEFENDER_ICON)

        self.boardlist = [player1Pieces, player2Pieces]

        player2.setWinRank(3) # Sets player1 win condition to be at y=3
        player1.setWinRank(0) # Sets player2 win condition to be at y=0

    def getPieceAtPos(self, posx, posy):
        '''(GameBoard, int, int) -> GamePiece
        Returns piece at (posx,posy), if none exists, return None
        REQ: posx in BOUNDS_X, posy in BOUNDS_Y
        '''
        # Searches for piece in (posx, posy)
        for playerPieces in self.boardlist:
            # playerPieces should be a list of pices
            for item in playerPieces:
                # item should be a game piece
                if item.getPos() == (posx, posy):
                    return item
        # If no piece occupys (posx,posy), returns None
        return None

    def removePiece(self, piece):
        '''(GameBoard, GamePiece) -> None
        Removes piece from Gameboard.
        '''
        if(piece in self.boardlist[0]):
            self.boardlist[0].remove(piece)
        elif(piece in self.boardlist[1]):
            self.boardlist[1].remove(piece)
        else:
            pass

class GamePiece():
    '''
    '''

    def __init__(self, posx, posy, player, board):
        ''' (GamePiece, int, int, Player, GameBoard) -> None
        Note position of each piece starts as 0,0
        '''
        self.posx = posx
        self.posy = posy
        player.addPiece(self)
        self.player = player
        self.possibleMoves = []
        self.possibleCaptures = []
        self.board = board
        self.icon = None

    def remove(self):
        '''(GamePiece) -> None
        Removes piece from board and player.
        '''
        self.board.removePiece(self)
        self.board = None
        self.posx = None
        self.posy = None
        self.player.removePiece(self)
        self.possibleMoves = None
        self.possibleCaptures = None
        self.icon = None

    def getPos(self):
        ''' Returns tuple of x and y pos as int
        '''
        return (self.posx, self.posy)

    def moveBy(self, deltax, deltay):
        '''(GamePiece, int, int) -> bool
        REQ: posx and posy is either -1, 0, or 1
        Moves piece by deltax in the x direction and deltay in the y
        Returns true if move was successful
        Returns false if move is illegal
        '''
        if(self.checkMoveLegal(deltax, deltay)):
            new_posx = self.posx + deltax
            new_posy = self.posy + deltay

            # If spot is occupied, but capture is allowed, remove piece
            piece_at_space = self.board.getPieceAtPos(new_posx, new_posy)
            if piece_at_space is not None:
                piece_at_space.remove()

            self.posx = new_posx
            self.posy = new_posy

            result = True
        else:
            result = False
        return result

    def moveTo(self, posx, posy):
        '''(GamePiece, int, int) -> bool
        Moves piece by to board (posx, posy), if legal
        Returns true if move was successful
        Returns false if move is illegal
        '''
        deltax = posx - self.posx
        deltay = posy - self.posy
        result = self.moveBy(deltax, deltay)
        return result

    def checkMoveLegal(self, deltax, deltay):
        ''' Checks if it is legal to move piece to (posx, posy),
        returns true iff
        -move results in piece being in bounds
        -space is empty, or space is not empty but the piece can be captured
        that is not your own
        '''
        newPosx = self.posx + deltax
        newPosy = self.posy + deltay
        in_bounds = (newPosx in BOUNDS_X and newPosy in BOUNDS_Y)
        # Check if something occupies the space we want to move to
        piece_at_space = self.board.getPieceAtPos(newPosx, newPosy)
        if piece_at_space is None:
            # Space is empty/Doesn't exist
            is_possible = [deltax, deltay] in self.possibleMoves
        else:
            # Check if piece at space is your own
            if piece_at_space in self.player.getPieces():
                # Cannot caputure own pieces, at least in default config
                is_possible = config.CAPTURE_OWN_PIECES
            else:
                # Space is not empty, therefore this piece must capture
                is_possible = [deltax, deltay] in self.possibleCaptures
        # If in bounds and empty/capturable, then can move, otherwise cannot
        return in_bounds and is_possible

    def setPossibleCaptures(self, possibleCaptures):
        '''(GamePiece, list of tuples of 2 ints) - > None
        '''
        self.possibleCaptures = possibleCaptures

    def setPossibleMoves(self, possibleMoves):
        '''(GamePiece, list of tuples of 2 ints) - > None
        '''
        self.possibleMoves = possibleMoves

    def getPossibleCaptures(self):
        '''(GamePiece) - > list of tuples of 2 ints
        '''
        return self.possibleCaptures

    def getPossibleMoves(self):
        '''(GamePiece) - > list of tuples of 2 ints
        '''
        return self.possibleMoves

    def setIcon(self, image):
        self.icon = image

    def getIcon(self):
        return self.icon

class Attacker(GamePiece):
    '''
    '''
    def __init__(self, posx, posy, player, board):
        '''
        '''
        GamePiece.__init__(self, posx, posy, player, board)
        self.setPossibleCaptures([[-1,-1],[-1,1],[1,-1],[1,1]])
        self.setPossibleMoves([[-1,-1],[-1,1],[1,-1],[1,1]])

class Defender(GamePiece):
    '''
    '''
    def __init__(self, posx, posy, player, board):
        '''
        '''
        GamePiece.__init__(self, posx, posy, player, board)
        self.setPossibleCaptures([[-1,0],[1,0]])
        self.setPossibleMoves([[0,-1],[0,1],[1,0],[-1,0]])

class Advancer(GamePiece):
    '''
    '''
    def __init__(self, posx, posy, player, board):
        '''
        '''
        GamePiece.__init__(self, posx, posy, player, board)
        self.setPossibleCaptures([[-1,1],[1,1]])
        self.setPossibleMoves([[0,1],[0,-1]])

class Player():
    '''
    '''
    def __init__(self):
        '''
        '''
        self.pieces = []
        self.winRank = int()

    def removePiece(self, piece):
        '''(GameBoard, GamePiece) -> None
        Removes piece from Gameboard.
        '''
        self.pieces.remove(piece)

    def movePiece(self, piece, posx, posy):
        '''(Player, GamePiece, int, int)
        '''

    def addPiece(self, piece):
        '''(Player, GamePiece) -> None
        '''
        self.pieces.append(piece)

    def getPieces(self):
        '''Returns a list of GamePieces
        '''
        return self.pieces

    def setWinRank(self, rank):
        '''(Player, int) -> None
        Sets the y value at which the player wins if they get an advancer
        there in a default game. The word 'rank' is used in the same sense
        of the ranks on a chess board (the y axis, towards your opponent).
        '''
        self.winRank = rank

    def checkDefaultWinCondition(self):
        ''' (Player) -> bool
        Checks default win condition. A player is in a win condition,
        iff they have at least one Advancer piece at y value of self.winRank
        '''
        won = False # var for win condition being met
        for piece in self.pieces:
            if type(piece) is Advancer:
                # Make sure that at least one of the advancers are at the rank
                won = won or piece.getPos()[1] == self.winRank
        return won

    def calculatePossibleActions(self):
        '''Returns a set of possible moves
        '''

    def reversePossibleMoves(self):
        '''Reverses the moves of all of the pieces.
        Intended to make each move symmetrical for both players.
        '''
        for piece in self.pieces:
            for move in piece.getPossibleMoves():
                move[0] = -move[0]
                move[1] = -move[1]
            for capture in piece.getPossibleCaptures():
                capture[0] = -capture[0]
                capture[1] = -capture[1]
