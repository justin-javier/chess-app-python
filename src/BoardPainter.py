import pygame
import os

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
LIGHT_TILE_COLOR = (227, 193, 111) # White brown
DARK_TILE_COLOR = (184, 139, 74) # Brown
HIGHLIGHT_TILE_COLOR = (186, 202, 68) # Light green

class BoardPainter:
    def __init__(self):
        print(os.getcwd() + "/resources/")
        self.piece_images = self.load_piece_images(os.getcwd() + "/resources/") # Load all images into board

    def draw_tile(self, screen, position, color):       
        x, y = position
        pygame.draw.rect(screen, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_regular_tile(self, screen, position):
        x, y = position
        is_even = (x + y) % 2 == 0
        color = LIGHT_TILE_COLOR if is_even else DARK_TILE_COLOR
        self.draw_tile(screen, position, color)

    def draw_highlighted_tile(self, screen, position):
        center_x = (position[0] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (WIDTH - GRID_SIZE * SQUARE_SIZE) // 2
        center_y = (position[1] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (HEIGHT - GRID_SIZE * SQUARE_SIZE) // 2

        radius = SQUARE_SIZE // 2.5

        self.draw_regular_tile(screen, position)
        pygame.draw.circle(screen, HIGHLIGHT_TILE_COLOR, (center_x, center_y), radius)

    def highlight_valid_move_tiles(self, screen, board):
        for move in board.selected_piece.valid_moves:
            self.draw_highlighted_tile(screen, move)
            self.draw_piece(screen, board.tiles.get(move))

    def unhighlight_valid_move_tiles(self, screen, board):
        for move in board.last_valid_moves:
            self.draw_regular_tile(screen, move)
            self.draw_piece(screen, board.tiles.get(move))

    def draw_board(self, screen):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.draw_regular_tile(screen, (x, y))

    def draw_piece(self, screen, piece):
        if piece is not None:
            png_name = piece.get_png_name()
            x, y = piece.position
            screen.blit(self.piece_images[png_name], (x * SQUARE_SIZE, y * SQUARE_SIZE))

    def draw_all_pieces(self, screen, board):
        for piece in board.tiles.values():
            if piece is not None:
                self.draw_piece(screen, piece)

    # Takes references to the screen, board, piece's old position, and piece
    def draw_move_to_empty_tile(self, screen, board, piece, old_position):
        self.unhighlight_valid_move_tiles(screen, board)
        self.draw_regular_tile(screen, old_position)
        self.draw_piece(screen, piece)

    def draw_switch_selected_piece(self, screen, board, old_piece, new_piece):
        self.unhighlight_valid_move_tiles(screen, board)
        # Draw the unselection of the old selected piece
        self.draw_regular_tile(screen, old_piece.position)
        self.draw_piece(screen, old_piece)
        # Draw selection of the new selected piece
        self.draw_highlighted_tile(screen, new_piece.position)
        self.draw_piece(screen, new_piece)
        self.highlight_valid_move_tiles(screen, board)

    def draw_select_new_piece(self, screen, board, piece):
        self.draw_highlighted_tile(screen, piece.position)
        self.draw_piece(screen, piece)
        # Highlight the selected piece's valid moves
        self.highlight_valid_move_tiles(screen, board)
    
    def draw_deselect_selected_piece(self, screen, board, piece):
        self.unhighlight_valid_move_tiles(screen, board)
        self.draw_regular_tile(screen, piece.position)
        self.draw_piece(screen, piece)

    # Takes in screen, board, the capturing piece and its old position
    def draw_capture(self, screen, board, piece, old_position):
        self.unhighlight_valid_move_tiles(screen, board)
        self.draw_regular_tile(screen, piece.position)
        self.draw_regular_tile(screen, old_position)
        self.draw_piece(screen, piece)

    def load_piece_images(self, directory):
        images = {}
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".png"):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(directory, filename)
                    image = pygame.image.load(path).convert_alpha()
                    scaled_image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    images[name] = scaled_image
        except FileNotFoundError:
            print(f"Error: Directory not found - {directory}")
        return images
