import pygame
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from StateChecker import StateChecker
from Board import Board
from Player import Player
from ChessAI import ChessAI

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
        self.board.init_display(self.screen)
        self.state_checker = StateChecker()
        self.ai = ChessAI("Black")
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
        if self.player_turn == "White":
            if self.board.tiles.get((pos_x, pos_y)) is None: 
                self.handle_select_empty_tile((pos_x, pos_y))
            
            # If we're selecting a piece
            else:
                self.handle_select_a_piece((pos_x, pos_y))

        elif self.player_turn == "Black":
            #self.handle_ai_move()
            if self.board.tiles.get((pos_x, pos_y)) is None: 
                self.handle_select_empty_tile((pos_x, pos_y))
            
            # If we're selecting a piece
            else:
                self.handle_select_a_piece((pos_x, pos_y))
        
    # Handles selecting of a piece (clicking tile with a piece inside)
    def handle_select_a_piece(self, position):

        sp = self.board.selected_piece

        if (sp is None):

            self.handle_new_selected_piece(position)

        else:
            # If we are selecting the same piece (for deselection)
            if sp.position == position:

                self.board.set_selected_piece(None)
                self.board.painter.draw_deselect_selected_piece(self.board, sp)
            # Else we want to select a new piece
            else:
                self.handle_piece_to_piece(sp.position, position)
                
    def handle_piece_to_piece(self, old_position, new_position):

        old_piece = self.board.tiles.get(old_position)
        new_piece = self.board.tiles.get(new_position) 

        # If we want to capture
        if (old_piece.color != new_piece.color) and (new_position in old_piece.get_valid_moves()):

            # Moving selected piece to new position after capture
            self.board.set_piece_at_position(old_piece, new_position)
            self.board.set_selected_piece(None)
            self.board.set_piece_at_position(None, old_position)

            if old_piece.color == "White":
                self.white_player.capture_piece(new_piece)
            else:
                self.black_player.capture_piece(new_piece)

            # Update graphics
            self.board.painter.draw_capture(self.board, old_piece, old_position)

            self.handle_promotion(old_piece)

            # Change player turn
            self.switch_turn()
            self.state_checker.check_if_lost(self.board, self.player_turn)
            self.handle_ai_move()

        elif (old_piece.color == new_piece.color):
                # If we want to switch our selected piece
                self.board.set_selected_piece(new_piece)
                self.board.painter.draw_switch_selected_piece(self.board, old_piece, new_piece)

    # Going from no selected piece to a possible selected piece
    def handle_new_selected_piece(self, position):
        piece = self.board.tiles.get(position)
        if (piece.color == self.player_turn):
            self.board.set_selected_piece(piece) 
            self.board.painter.draw_select_new_piece(self.board, piece)

    # Handles selecting of a empty tile
    def handle_select_empty_tile(self, position):
        sp = self.board.selected_piece
        # If we want to move the selected piece to a new tile
        if sp is None:
            return
        if position in sp.get_valid_moves():

            old_position = sp.position
            # Remove the piece's old position in pieces_on_board
            self.board.set_piece_at_position(None, old_position)
            # Clear the currently selected piece
            self.board.set_selected_piece(None)
            # Update the position in pieces_on_board
            self.board.set_piece_at_position(sp, position) 

            self.board.painter.draw_move_to_empty_tile(self.board, sp, old_position)

            self.handle_castling(sp, old_position)
            self.handle_en_passant(sp, old_position)
            self.handle_promotion(sp)

            self.switch_turn()
            self.state_checker.check_if_lost(self.board, self.player_turn)
            self.handle_ai_move()

    def handle_castling(self, piece, old_position):

        if (isinstance(piece, King)) and (old_position[0] - piece.position[0] == 2):

            rook = self.board.tiles.get((0, piece.position[1]))
            self.board.set_piece_at_position(None, (0, piece.position[1]))
            self.board.set_piece_at_position(rook, (piece.position[0] + 1, piece.position[1]))
            self.board.painter.draw_move_to_empty_tile(self.board, rook, (0, piece.position[1]))

        # If King is castling right
        elif (isinstance(piece, King)) and (piece.position[0] - old_position[0] == 2):

            rook = self.board.tiles.get((7, piece.position[1]))
            self.board.set_piece_at_position(None, (7, piece.position[1]))
            self.board.set_piece_at_position(rook, (piece.position[0] - 1, piece.position[1]))
            self.board.painter.draw_move_to_empty_tile(self.board, rook, (7, piece.position[1]))

    def handle_en_passant(self, piece, old_position): 

        if (
            isinstance(piece, Pawn)
            and abs(old_position[0] - piece.position[0]) == 1  # Diagonal move
            and abs(old_position[1] - piece.position[1]) == 1  # Diagonal move
        ):
            # Determine the position of the passed pawn
            passed_pawn_position = (piece.position[0], old_position[1])

            # Remove the passed pawn from the board
            passed_pawn = self.board.tiles.pop(passed_pawn_position, None)

            # Update the graphics
            if passed_pawn:
                self.board.painter.draw_regular_tile(passed_pawn_position)
                if piece.color == "White":
                    self.white_player.capture_piece(passed_pawn)
                else:
                    self.black_player.capture_piece(passed_pawn)

    def handle_promotion(self, piece):

        if not isinstance(piece, Pawn):
            return
        if (piece.color == "White" and piece.position[1] == 0) or (piece.color == "Black" and piece.position[1]) == 7:
        
            promoted_p_type = self.board.painter.draw_promotion_menu(piece.color)
            promoted_p = self.board.create_piece_instance(promoted_p_type, piece.color, piece.position)
            self.board.set_piece_at_position(None, piece.position)
            self.board.set_piece_at_position(promoted_p, piece.position)

            self.board.painter.refresh(self.board)

    def handle_ai_move(self):
        ai_move = self.ai.calculate_move(self.board)
        if ai_move:
            old_position, new_position = ai_move

            old_piece = self.board.tiles[old_position]
            new_piece = self.board.tiles[new_position]

            self.board.set_piece_at_position(None, old_position)
            self.board.set_piece_at_position(old_piece, new_position)

            if not new_piece:
                self.board.painter.draw_move_to_empty_tile(self.board, old_piece, old_position)
            else:
                self.board.painter.draw_capture(self.board, old_piece, old_position)
                self.black_player.capture_piece(new_piece)

            self.switch_turn()
            self.state_checker.check_if_lost(self.board, self.player_turn)

    def switch_turn(self):
        if self.player_turn == "White":
            self.player_turn = "Black"
        else:
            self.player_turn = "White"
