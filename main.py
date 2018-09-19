import pygame
import sys
import config
import engine

# Possible spaces on the board
BOUNDS_X = config.BOUNDS_X
BOUNDS_Y = config.BOUNDS_Y
WINDOW_X = config.WINDOW_X # Window width
WINDOW_Y = config.WINDOW_Y # Window height
SQUARE_WIDTH = WINDOW_X/len(BOUNDS_X)
SQUARE_HEIGHT = WINDOW_Y/len(BOUNDS_Y)

class Display():
    '''
    '''

    def __init__(self, sizex, sizey):
        '''(Display, int, int) -> None
        '''
        self.size = sizex, sizey
        self.window = None
        self.rect_array = []

    def initializeWindow(self):
        '''
        '''
        # Initialize pygame window
        self.window = pygame.display.set_mode(self.size)
        # Create the rectangles for checkerboard pattern
        for i in range(len(BOUNDS_X) * len(BOUNDS_Y)):
            new_rect = pygame.Rect((i % len(BOUNDS_X)) * SQUARE_WIDTH,
                                   (i // len(BOUNDS_X)) * SQUARE_HEIGHT,
                                   SQUARE_WIDTH, SQUARE_HEIGHT)
            self.rect_array.append(new_rect)


    def drawGrid(self, colour1, colour2):
        ''' (Display, pygame.color.Colour, pygame.color.Colour) -> None
        Draws checkerboard pattern on the window. Colour1 is colour of (0,0)
        square.
        '''
        # Draw main background
        self.window.fill(colour1)
        # Draw every second rectangle s.t. a colour2 rect is at board pos (0,0)
        for i in range(len(self.rect_array)):
            # Select squares to colour
            x = i % len(BOUNDS_X) # Square position starting from left to right
            y = i // len(BOUNDS_X) # Square position starting from top to bottom
            if ((x % 2  + y % 2) ==1):
                pygame.draw.rect(self.window, colour2, self.rect_array[i])

    def drawPieces(self, pieces):
        '''(Display, list of GamePiece) -> None
        Given a list of GamePieces, draws them in their
        associated positions.
        '''
        for item in pieces:
            position = item.getPos()
            index = position[0] + position[1] * len(BOUNDS_X)
            rect = self.rect_array[index]
            image = pygame.image.load(item.getIcon())
            image = pygame.transform.scale(image, tuple(rect)[2:])
            self.window.blit(image, rect)


if(__name__ == '__main__'):
    colour1 = config.TILE_COLOUR_1
    colour2 = config.TILE_COLOUR_2
    display = Display(WINDOW_X, WINDOW_Y)
    display.initializeWindow()

    player1 = engine.Player()
    player2 = engine.Player()
    game_board = engine.GameBoard()
    game_board.initalizeDefaultBoard(player1, player2)
    player2.reversePossibleMoves()

    currentTurn = player1
    piece_draging = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    pos_on_board = (int(mouse_x//(WINDOW_X/len(BOUNDS_X))),
                                    int(mouse_y//(WINDOW_Y/len(BOUNDS_Y))))
                    selected_piece = game_board.getPieceAtPos(pos_on_board[0],
                                                              pos_on_board[1])
                    if selected_piece is not None:
                        piece_draging = True
                    #offset_x = rectangle.x - mouse_x
                    #offset_y = rectangle.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and piece_draging is True:
                    pos_on_board = (int(mouse_x//(WINDOW_X/len(BOUNDS_X))),
                                    int(mouse_y//(WINDOW_Y/len(BOUNDS_Y))))
                    print("Moving " + str(selected_piece) + ' to ' + str(pos_on_board))
                    print(selected_piece.moveTo(pos_on_board[0], pos_on_board[1]))
                    piece_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if piece_draging:
                    mouse_x, mouse_y = event.pos
                    #selected_piece.(mouse_x + offset_x,
                    #                      mouse_y + offset_y)


        display.drawGrid(colour1, colour2)
        display.drawPieces(player1.getPieces() + player2.getPieces())
        pygame.display.update()
