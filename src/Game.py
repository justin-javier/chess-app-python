import pygame
import sys
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn    
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
        self.white_player = Player(player_type="White")
        self.black_player = Player(player_type="Black")
        self.player_turn = "White"

    def main(self): 
        self.board.init_start_positions() # Places all pieces in game start positions

        self.board.painter.draw_board(self.screen) # Draw the board using board.draw_tile()
        self.board.painter.draw_all_pieces(self.screen, self.board) # Paint all the piece images according to piece positions in board

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle the mouse click
                    self.handle_mouse_click(event)

            # Update the display
            pygame.display.flip()

    # Handle the mouse click event 
    def handle_mouse_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse coordinates to grid position
        pos_x = mouse_x // SQUARE_SIZE 
        pos_y = mouse_y // SQUARE_SIZE

        # Clicked outside the chessboard, do nothing
        if not (0 <= pos_x < GRID_SIZE and 0 <= pos_y < GRID_SIZE):
            return

        print(f"Clicked on square ({pos_x}, {pos_y})")

        # If the tile is empty (no piece)
        if self.board.get_piece_at_position((pos_x, pos_y)) is None: 
            # If we want to move the selected piece to a new tile
            self.handle_select_empty_tile((pos_x, pos_y))
        
        # If we're selecting a piece
        else:
            self.handle_select_piece_tile((pos_x, pos_y))
        #print(self.player_turn)

    # Handles selecting of a piece (clicking tile with a piece inside)
    def handle_select_piece_tile(self, position):
        sp = self.board.selected_piece
        # If no piece is currently selected and its the color of the current turn player
        if (sp is None):
            np = self.board.get_piece_at_position(position)
            if (np.color == self.player_turn):
                # Save piece as selected_piece (piece that wants to move)
                self.board.set_selected_piece(np) 
                # This will highlight the tile and draw the piece selected
                self.board.painter.draw_select_new_piece(self.screen, self.board, np)

        # If a piece is selected already
        else:
            # If we are selecting the same piece (for deselection)
            if sp.position[0] == position[0] and sp.position[1] == position[1]:
                self.board.set_selected_piece(None)
                self.board.painter.draw_deselect_selected_piece(self.screen, self.board, sp)
            # Else we want to select a new piece
            else:
                np = self.board.get_piece_at_position(position) # New piece selected

                # If we want to capture
                if (sp.color != np.color) and (position in sp.get_valid_moves()):
                    old_position = sp.position
                    # Moving selected piece to new position after capture
                    self.board.set_piece_at_position(position, sp)
                    self.board.set_selected_piece(None)
                    self.board.set_piece_at_position(old_position, None)

                    if sp.color == "White":
                        self.white_player.capture_piece(np)
                    else:
                        self.black_player.capture_piece(np)

                    # Update graphics
                    self.board.painter.draw_capture(self.screen, self.board, sp, old_position)

                    # Change player turn
                    self.switch_turn()

                else:
                    if (np.color == sp.color):
                        # If we want to switch our selected piece
                        self.board.set_selected_piece(np)

                        # painter func here
                        self.board.painter.draw_switch_selected_piece(self.screen, self.board, sp, np)

    # Handles selecting of a empty tile
    def handle_select_empty_tile(self, position):
        sp = self.board.selected_piece
        # If we want to move the selected piece to a new tile
        if sp is not None:
            if position in sp.get_valid_moves():
                old_position = sp.position
                # Remove the piece's old position in pieces_on_board
                self.board.set_piece_at_position(old_position, None)
                # Clear the currently selected piece
                self.board.set_selected_piece(None)
                # Update the position in pieces_on_board
                self.board.set_piece_at_position(position, sp) 

                self.board.painter.draw_move_to_empty_tile(self.screen, self.board, sp, old_position)

                self.switch_turn()

    def switch_turn(self):
            if self.player_turn == "White":
                self.player_turn = "Black"
            else:
                self.player_turn = "White"

if __name__ == "__main__":
    game = Game()
    game.main()