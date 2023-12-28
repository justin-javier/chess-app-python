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

def main(): 

    global screen # Maintains the screen

    # Create the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Returns a pygame.Surface object
    pygame.display.set_caption("Chess Game")

    white_player = Player(player_type="White")
    black_player = Player(player_type="Black")

    # Create the board and initialize it
    board = Board()
    board.load_piece_images() # Load all images into board
    board.init_start_positions() # Places all pieces in game start positions
    board.draw_board(screen) # Draw the board using board.draw_tile()
    board.draw_all_pieces(screen) # Paint all the piece images according to piece positions in board

    # Set selected piece to None for game start
    #selected_piece = None 

    ######
    # We will draw tiles and pieces on demand to prevent repetitive painting in the loop
    ######

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle the mouse click
                handle_mouse_click(board, event)

        # Update the display
        pygame.display.flip()

# Handle the mouse click event 
def handle_mouse_click(board, event):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Convert mouse coordinates to grid position
    pos_x = mouse_x // SQUARE_SIZE 
    pos_y = mouse_y // SQUARE_SIZE

    # Clicked outside the chessboard, do nothing
    if not (0 <= pos_x < GRID_SIZE and 0 <= pos_y < GRID_SIZE):
        return

    print(f"Clicked on square ({pos_x}, {pos_y})")

    # If the tile is empty (no piece)
    if board.get_piece_at_position((pos_x, pos_y)) is None: 
        # If we want to move the selected piece to a new tile
        handle_select_empty_tile(screen, board, (pos_x, pos_y))
    
    # If we're selecting a piece
    else:
        handle_select_piece_tile(screen, board, (pos_x, pos_y))

# Handles selecting of a piece (clicking tile with a piece inside)
def handle_select_piece_tile(screen, board, position):
    x, y = position
    sp = board.get_selected_piece()
    # If no piece is currently selected
    if sp is None:
        sp = board.get_piece_at_position((x, y))
        # Save piece as selected_piece (piece that wants to move)
        board.set_selected_piece(sp)
        # This will highlight the tile and draw the piece selected
        board.draw_highlighted_tile(screen, (x, y))
        board.draw_piece(screen, sp)
        # Highlight the selected piece's valid moves
        board.highlight_valid_move_tiles(screen)

    # If a piece is selected already
    else:
        # If we are selecting the same piece (for deselection)
        if sp.position[0] == x and sp.position[1] == y:
            board.set_selected_piece(None)
            board.unhighlight_valid_move_tiles(screen)
            board.draw_regular_tile(screen, (x, y))
            board.draw_piece(screen, sp)
        # Else we want to select a new piece
        else:

            # Add Capture Logic

            print("Selecting new piece")
            op = board.get_selected_piece() # Old piece selected
            old_x, old_y = op.position
            np = board.get_piece_at_position((x, y)) # New piece selected
            board.set_selected_piece(np)
            board.unhighlight_valid_move_tiles(screen)
            board.draw_regular_tile(screen, (old_x, old_y))
            board.draw_piece(screen, op)
            board.draw_highlighted_tile(screen, (x, y))
            board.draw_piece(screen, np)
            board.highlight_valid_move_tiles(screen)

# Handles selecting of a empty tile
def handle_select_empty_tile(screen, board, position):
    x, y = position
    sp = board.get_selected_piece()
    # If we want to move the selected piece to a new tile
    if sp is not None:
        if position in sp.get_valid_moves():
            old_x, old_y = sp.position
            # Remove the piece's old position in pieces_on_board
            board.set_piece_at_position((old_x, old_y), None)
            # Clear the currently selected piece
            board.set_selected_piece(None)
            board.unhighlight_valid_move_tiles(screen)

            # Update the selected piece's position
            sp.move(board, (x, y)) # Pass a tuple of position 
            # Unhighlight the tile that the piece is moving from
            board.draw_regular_tile(screen, (old_x, old_y))
            # Update the position in pieces_on_board
            board.set_piece_at_position((x, y), sp)         
            # Draw piece and tile at the destination
            board.draw_regular_tile(screen, (x, y)) # Maybe not necessary bc we're moving to empty tile
            board.draw_piece(screen, sp)


if __name__ == "__main__":
    main()