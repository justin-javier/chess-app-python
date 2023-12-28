import pygame
import os
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
LIGHT_TILE_COLOR = (227, 193, 111) # White brown
DARK_TILE_COLOR = (184, 139, 74) # Brown
HIGHLIGHT_TILE_COLOR = (186, 202, 68) # Light green

class Board:
    def __init__(self):
        self.tiles = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_piece = None
        self.piece_images = {}
        self.last_valid_moves = []

    def set_piece_images(self, images):
        self.piece_images = images

    def get_piece_images(self):
        return self.piece_images

    def set_selected_piece(self, piece):
        if piece is not None: 
            piece.set_valid_moves(self)   
            print("Valid Moves: " + str(piece.get_valid_moves()))   

        sp = self.get_selected_piece()
        if sp is None:
            self.last_valid_moves = piece.get_valid_moves()
        else:
            self.last_valid_moves = sp.get_valid_moves()
        print("Last Valid Moves: " + str(self.last_valid_moves))
        self.selected_piece = piece

    def get_selected_piece(self):
        return self.selected_piece

    def get_piece_at_position(self, position):
        x, y = position
        return self.tiles[x][y]

    def set_piece_at_position(self, position, piece):
        x, y = position
        self.tiles[x][y] = piece

    # Paint a tile (and piece if present) given specific coordinates
    def draw_tile(self, screen, position, color):       
        x, y = position
        pygame.draw.rect(screen, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        piece = self.get_piece_at_position((x,y))

    def draw_regular_tile(self, screen, position):
        x, y = position
        is_even = (x + y) % 2 == 0
        # Return color based on even/odd result
        color = LIGHT_TILE_COLOR if is_even else DARK_TILE_COLOR
        self.draw_tile(screen, position, color)

    def draw_highlighted_tile(self, screen, position):
        color = HIGHLIGHT_TILE_COLOR
        center_x = (position[0] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (WIDTH - GRID_SIZE * SQUARE_SIZE) // 2
        center_y = (position[1] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (HEIGHT - GRID_SIZE * SQUARE_SIZE) // 2

        # Calculate the radius of the circle (you can adjust this)
        radius = SQUARE_SIZE // 2.5

        self.draw_regular_tile(screen, position)
        pygame.draw.circle(screen, color, (center_x, center_y), radius)

    # Highlights the tiles a Piece can move to
    def highlight_valid_move_tiles(self, screen):
        piece = self.get_selected_piece()
        valid_moves = piece.get_valid_moves()
        # Get all the potential moves 
        for move in valid_moves:
            self.draw_highlighted_tile(screen, move)
            self.draw_piece(screen, self.get_piece_at_position(move))

    def unhighlight_valid_move_tiles(self, screen):
        #print("Unhighlighting tiles")
        for move in self.last_valid_moves:
            self.draw_regular_tile(screen, move)
            self.draw_piece(screen, self.get_piece_at_position(move))

    # Draws the board
    def draw_board(self, screen):
        # Draw the chessboard
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.draw_regular_tile(screen, (x, y))

    # Draw a piece to a screen given the Piece object
    def draw_piece(self, screen, piece):
        if piece is not None:
            png_name = piece.get_png_name()
            x = piece.position[0]
            y = piece.position[1]
            screen.blit(self.piece_images[png_name], (x * SQUARE_SIZE, y * SQUARE_SIZE))

    # Draw all chess pieces according to their positions
    def draw_all_pieces(self, screen):
        for row in self.tiles:
            for piece in row:
                if piece != None:
                    self.draw_piece(screen, piece)

    # Sets all the valid moves for every piece
    def set_all_valid_moves(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                piece = self.get_piece_at_position((row, col))
                if piece is not None:
                    piece.set_valid_moves(self)

    # Load piece images, scale them down, and return them in a dict 
    def load_piece_images(self):
        images = {}
        directory = "../resources"  # Change this to the actual path of your images folder
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".png"):
                    name = os.path.splitext(filename)[0]  # Extract the filename without extension
                    path = os.path.join(directory, filename)
                    image = pygame.image.load(path).convert_alpha()
                    scaled_image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    images[name] = scaled_image
        except FileNotFoundError:
            print(f"Error: Directory not found - {directory}")

        self.piece_images = images

    # Populate the pieces_on_board with the starting positions of all pieces
    def init_start_positions(self):
        # Populate Pawns
        for i in range(GRID_SIZE):
            self.set_piece_at_position((i, 1), Pawn(color="Black", position=(i,1)))

            self.set_piece_at_position((i, 6), Pawn(color="White", position=(i,6)))
        # Populate Kings
        self.set_piece_at_position((4, 0), King(color="Black", position=(4,0)))
        self.set_piece_at_position((4, 7), King(color="White", position=(4,7)))
        # Populate Queens
        self.set_piece_at_position((3, 0), Queen(color="Black", position=(3,0)))
        self.set_piece_at_position((3, 7), Queen(color="White", position=(3,7)))
        # Populate Knights
        self.set_piece_at_position((1, 0), Knight(color="Black", position=(1,0)))
        self.set_piece_at_position((6, 0), Knight(color="Black", position=(6,0)))
        self.set_piece_at_position((1, 7), Knight(color="White", position=(1,7)))
        self.set_piece_at_position((6, 7), Knight(color="White", position=(6,7)))
        # Populate Bishops
        self.set_piece_at_position((2, 0), Bishop(color="Black", position=(2,0)))
        self.set_piece_at_position((5, 0), Bishop(color="Black", position=(5,0)))
        self.set_piece_at_position((2, 7), Bishop(color="White", position=(2,7)))
        self.set_piece_at_position((5, 7), Bishop(color="White", position=(5,7)))
        # Populate Rooks
        self.set_piece_at_position((0, 0), Rook(color="Black", position=(0,0)))
        self.set_piece_at_position((7, 0), Rook(color="Black", position=(7,0)))
        self.set_piece_at_position((0, 7), Rook(color="White", position=(0,7)))
        self.set_piece_at_position((7, 7), Rook(color="White", position=(7,7)))


# You can add more methods to this class as needed.
