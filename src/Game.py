import pygame
import sys
from GameHandler import GameHandler
from Board import Board
from Player import Player

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
LIGHT_TILE_COLOR = (227, 193, 111) # White brown
DARK_TILE_COLOR = (184, 139, 74) # Brown
HIGHLIGHT_TILE_COLOR = (186, 202, 68) # Light green

# Initialize all Pygame modules (draw, display, color, etc.)
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.board = Board()
        self.handler = GameHandler(self.screen, self.board)

    def main(self): 
        self.board.init_start_positions() # Places all pieces in game start positions
        self.board.init_painter()
        self.board.painter.draw_board(self.screen) # Draw the board using board.draw_tile()
        self.board.painter.draw_all_pieces(self.screen, self.board) # Paint all the piece images according to piece positions in board
        update_display = False

        clock = pygame.time.Clock()
        FRAME_RATE = 15

        pygame.display.flip()
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Use MOUSEBUTTONUP instead of MOUSEBUTTONDOWN
                    # Handle the mouse click
                    self.handler.handle_mouse_click(event)
                    pygame.display.flip()
            
            clock.tick(FRAME_RATE)

            


if __name__ == "__main__":
    game = Game()
    game.main()