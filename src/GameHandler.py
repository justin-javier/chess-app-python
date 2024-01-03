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

class GameHandler():
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.white_player = Player(player_type="White")
        self.black_player = Player(player_type="Black")
        self.player_turn = "White"
    
     # Handle the mouse click event 
    def handle_mouse_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse coordinates to grid position
        pos_x = mouse_x // SQUARE_SIZE 
        pos_y = mouse_y // SQUARE_SIZE

        # Clicked outside the chessboard, do nothing
        if not (0 <= pos_x < GRID_SIZE and 0 <= pos_y < GRID_SIZE):
            return

        #print(f"Clicked on square ({pos_x}, {pos_y})")

        # If the tile is empty (no piece)
        if self.board.get_piece_at_position((pos_x, pos_y)) is None: 
            # If we want to move the selected piece to a new tile
            self.handle_select_empty_tile((pos_x, pos_y))
        
        # If we're selecting a piece
        else:
            self.handle_select_piece_tile((pos_x, pos_y))
        
        self.check_game_end()

    def check_game_end(self):
        # Check for checkmate
        if self.is_checkmate("White"):
            print("Checkmate! Black wins.")
            #pygame.quit()
            #sys.exit()
        elif self.is_checkmate("Black"):
            print("Checkmate! White wins.")
            #pygame.quit()
            #sys.exit()

        # Check for stalemate
        if self.is_stalemate("White") or self.is_stalemate("Black"):
            print("Stalemate! No one wins.")
            #pygame.quit()
            #sys.exit()

    # Handles selecting of a piece (clicking tile with a piece inside)
    def handle_select_piece_tile(self, position):
        sp = self.board.selected_piece
        # If no piece is currently selected and its the color of the current turn player
        if (sp is None):
            np = self.board.get_piece_at_position(position)
            if (np.color == self.player_turn):
                #print("Empty -> Selected Piece")
                # Save piece as selected_piece (piece that wants to move)
                self.board.set_selected_piece(np) 
                # This will highlight the tile and draw the piece selected
                self.board.painter.draw_select_new_piece(self.screen, self.board, np)

        # If a piece is selected already
        else:
            # If we are selecting the same piece (for deselection)
            if sp.position[0] == position[0] and sp.position[1] == position[1]:
                #print("Deselecting piece")
                self.board.set_selected_piece(None)
                self.board.painter.draw_deselect_selected_piece(self.screen, self.board, sp)
            # Else we want to select a new piece
            else:
                np = self.board.get_piece_at_position(position) # New piece selected

                # If we want to capture
                if (sp.color != np.color) and (position in sp.get_valid_moves()):
                    #print("Capturing a piece")
                    old_position = sp.position
                    # Moving selected piece to new position after capture
                    self.board.set_piece_at_position(position, sp)
                    self.board.set_selected_piece(None)
                    self.board.set_piece_at_position(old_position, None)

                    if (isinstance(sp, King)) or (isinstance(sp, Rook)):
                        sp.has_moved = True

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
                        #print("Switching selected piece")
                        # If we want to switch our selected piece
                        self.board.set_selected_piece(np)
                        self.board.painter.draw_switch_selected_piece(self.screen, self.board, sp, np)

    # Handles selecting of a empty tile
    def handle_select_empty_tile(self, position):
        sp = self.board.selected_piece
        # If we want to move the selected piece to a new tile
        if sp is None:
            return
        if position in sp.get_valid_moves():
            #print("Moving piece to empty tile")
            old_position = sp.position
            # Remove the piece's old position in pieces_on_board
            self.board.set_piece_at_position(old_position, None)
            # Clear the currently selected piece
            self.board.set_selected_piece(None)
            # Update the position in pieces_on_board
            self.board.set_piece_at_position(position, sp) 

            if (isinstance(sp, King)) or (isinstance(sp, Rook)):
                sp.has_moved = True
            # If King is castling left

            self.board.painter.draw_move_to_empty_tile(self.screen, self.board, sp, old_position)
            self.handle_castling(sp, old_position, position)
            
            self.switch_turn()

    def handle_castling(self, piece, old_position, new_position):
        if (isinstance(piece, King)) and (old_position[0] - new_position[0] == 2):
                print("CASTLING LEFT")
                print(new_position)
                rook = self.board.get_piece_at_position((0, new_position[1]))
                self.board.set_piece_at_position((0, new_position[1]), None)
                self.board.set_piece_at_position((new_position[0] + 1, new_position[1]), rook)
                self.board.painter.draw_move_to_empty_tile(self.screen, self.board, rook, (0, new_position[1]))
        # If King is castling right
        elif (isinstance(piece, King)) and (new_position[0] - old_position[0] == 2):
            print("CASTLING RIGHT")
            print(new_position)
            rook = self.board.get_piece_at_position((7, new_position[1]))
            self.board.set_piece_at_position((7, new_position[1]), None)
            self.board.set_piece_at_position((new_position[0] - 1, new_position[1]), rook)
            self.board.painter.draw_move_to_empty_tile(self.screen, self.board, rook, (7, new_position[1]))
    

    def is_checkmate(self, color):
        # Check if the king is in check
        if self.board.is_king_exposed(color):
            print("CHECK!")
            # Iterate through all pieces of the current player
            pieces = [piece for piece in self.board.tiles.values() if piece and piece.color == color]
            all_moves = []
            for piece in pieces:
                all_moves.extend(piece.calculate_valid_moves(self.board))
                if len(all_moves) != 0:
                    return False
            return True
        return False

    def is_stalemate(self, color):
        # Check if the king is not in check
        if not self.board.is_king_exposed(color):
            # Iterate over all pieces of the specified color
            pieces = [piece for piece in self.board.tiles.values() if piece and piece.color == color]
            for piece in pieces:
                # Check if the piece has any valid moves
                if piece.calculate_valid_moves(self.board):
                    # If any piece has valid moves, it's not stalemate
                    return False
            # All pieces have no valid moves, it's stalemate
            return True
        # King is in check, not stalemate
        return False

    def switch_turn(self):
        if self.player_turn == "White":
            self.player_turn = "Black"
        else:
            self.player_turn = "White"