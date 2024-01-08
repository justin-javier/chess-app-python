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

class BoardPainter:
    def __init__(self, screen):
        print(os.getcwd() + "/resources/")
        self.screen = screen
        self.piece_images = self.load_piece_images(os.getcwd() + "/resources/") # Load all images into board

    def draw_tile(self, position, color):       
        x, y = position
        pygame.draw.rect(self.screen, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_regular_tile(self, position):
        x, y = position
        is_even = (x + y) % 2 == 0
        color = LIGHT_TILE_COLOR if is_even else DARK_TILE_COLOR
        self.draw_tile(position, color)

    def draw_highlighted_tile(self, position):
        center_x = (position[0] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (WIDTH - GRID_SIZE * SQUARE_SIZE) // 2
        center_y = (position[1] * SQUARE_SIZE) + (SQUARE_SIZE // 2) + (HEIGHT - GRID_SIZE * SQUARE_SIZE) // 2

        radius = SQUARE_SIZE // 2.5

        self.draw_regular_tile(position)
        pygame.draw.circle(self.screen, HIGHLIGHT_TILE_COLOR, (center_x, center_y), radius)

    def highlight_valid_move_tiles(self, board):
        for move in board.selected_piece.valid_moves:
            self.draw_highlighted_tile(move)
            self.draw_piece(board.tiles.get(move))

    def unhighlight_valid_move_tiles(self, board):
        for move in board.last_valid_moves:
            self.draw_regular_tile(move)
            self.draw_piece(board.tiles.get(move))

    def draw_board(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.draw_regular_tile((x, y))

    def draw_piece(self, piece):
        if piece is not None:
            png_name = piece.get_png_name()
            x, y = piece.position
            self.screen.blit(self.piece_images[png_name], (x * SQUARE_SIZE, y * SQUARE_SIZE))

    def draw_all_pieces(self, board):
        for piece in board.tiles.values():
            if piece is not None:
                self.draw_piece(piece)

    # Takes references to the screen, board, piece's old position, and piece
    def draw_move_to_empty_tile(self, board, piece, old_position):
        self.unhighlight_valid_move_tiles(board)
        self.draw_regular_tile(old_position)
        self.draw_piece(piece)

    def draw_switch_selected_piece(self, board, old_piece, new_piece):
        self.unhighlight_valid_move_tiles(board)
        # Draw the unselection of the old selected piece
        self.draw_regular_tile(old_piece.position)
        self.draw_piece(old_piece)
        # Draw selection of the new selected piece
        self.draw_highlighted_tile(new_piece.position)
        self.draw_piece(new_piece)
        self.highlight_valid_move_tiles(board)

    def draw_select_new_piece(self, board, piece):
        self.draw_highlighted_tile(piece.position)
        self.draw_piece(piece)
        # Highlight the selected piece's valid moves
        self.highlight_valid_move_tiles(board)
    
    def draw_deselect_selected_piece(self, board, piece):
        self.unhighlight_valid_move_tiles(board)
        self.draw_regular_tile(piece.position)
        self.draw_piece(piece)

    # Takes in screen, board, the capturing piece and its old position
    def draw_capture(self, board, piece, old_position):
        self.unhighlight_valid_move_tiles(board)
        self.draw_regular_tile(piece.position)
        self.draw_regular_tile(old_position)
        self.draw_piece(piece)

    def draw_promotion_menu(self, promoted_color):
        promotion_options = ["Queen", "Rook", "Knight", "Bishop"]
        png_names = []

        button_width, button_height = 80, 80  # Adjust the size of the buttons
        vertical_spacing = 10
        total_height = len(promotion_options) * (button_height + vertical_spacing)

        option_buttons = []
            

        for i, promotion in enumerate(promotion_options):
            name = promoted_color.lower() + "-" + promotion.lower()

            button_image = self.piece_images[name]
            button_image = pygame.transform.scale(button_image, (button_width, button_height))

            x = WIDTH // 2 - button_width // 2
            y = HEIGHT // 2 - total_height // 2 + i * (button_height + vertical_spacing)

            button_rect = pygame.Rect(x, y, button_width, button_height)
            self.screen.blit(button_image, button_rect)

            option_buttons.append((button_rect, promotion))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button_rect, option in option_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            return option

            pygame.time.Clock().tick(30)

    def refresh(self, board):
        self.draw_board()
        self.draw_all_pieces(board)

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
