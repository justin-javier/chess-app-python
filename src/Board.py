import pygame
import os
import copy
import random
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from BoardPainter import BoardPainter
from MoveValidator import (
    VerticalMoveValidator,
    HorizontalMoveValidator,
    DiagonalMoveValidator,
    KnightMoveValidator,
    PawnMoveValidator,
    SingleMoveValidator
)

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
        self.tiles = {}
        self.selected_piece = None
        self.last_valid_moves = []
        self.painter = None
        self.init_start_positions()

    def set_selected_piece(self, piece):
        if piece is not None: 
            valid_moves = piece.calculate_valid_moves(self)   
            piece.set_valid_moves(valid_moves)

        sp = self.selected_piece
        if sp is None:
            self.last_valid_moves = piece.get_valid_moves()
        else:
            self.last_valid_moves = sp.get_valid_moves()

        self.selected_piece = piece
        #print("selected piece: " + str(self.selected_piece))

    def set_piece_at_position(self, piece, position):
        if piece is not None:
            piece.move(position)
            # Disable En Passant if not done immediately
            for enemy_pos in self.tiles:
                enemy_piece = self.tiles.get(enemy_pos)
                if (
                    enemy_piece is not None
                    and isinstance(enemy_piece, Pawn)
                    and enemy_piece.color != piece.color
                ):
                    enemy_piece.en_passant_vulnerable = False
        self.tiles[position] = piece

    # Get all the valid moves for every piece of a color
    def get_color_valid_moves(self, color):
        ai_pieces = [piece for piece in board.tiles.values() if piece and piece.color == self.color]
        # Select a random piece
        selected_piece = random.choice(ai_pieces)

        valid_moves = selected_piece.get_valid_moves(self)
        for position in self.tiles.values():
            piece = self.tiles.get(position)
            if piece is not None and piece.color == color:
                valid_moves = piece.calculate_valid_moves(self)
        return valid_moves
    
    def is_position_under_attack(self, position, color):
        """
        Check if a given position is under attack by any opponent pieces.
        """
        validators = [
            VerticalMoveValidator(),
            HorizontalMoveValidator(),
            DiagonalMoveValidator(),
            KnightMoveValidator(),
            PawnMoveValidator(),
            SingleMoveValidator()
        ]
        for validator in validators:
            # Calculate valid moves for color per validator
            moves = validator.get_valid_moves(self, position, color)
            # Check if any of the moves ends with an enemy piece that has the same validator
            for move in moves:
                piece = self.tiles.get(move)
                if piece is not None:
                    for piece_validator in piece.move_validators:
                        if piece_validator.get_type() == validator.get_type():
                            return True
        return False

    def is_king_exposed(self, color):
        """
        Check if the king of the specified color is exposed.
        """
        # Get king position
        king_position = self.get_king_position(color)

        # Ensure king_position is a tuple (x, y)
        if not isinstance(king_position, tuple):
            return False
        # Check if the king position is under attack
        return self.is_position_under_attack(king_position, color)

    def get_king_position(self, color):
        for pos, piece in self.tiles.items():
            if piece is not None and isinstance(piece, King) and piece.color == color:
                return pos
        return
    
    def create_piece_instance(self, option, color, position):
        # Create an instance of the selected piece based on the option
        if option == "Queen":
            return Queen(color, position)
        elif option == "Rook":
            return Rook(color, position)
        elif option == "Knight":
            return Knight(color, position)
        elif option == "Bishop":
            return Bishop(color, position)
        else:
            # Handle unexpected option (return None, raise an exception, or provide a default)
            return None

    # Populate the pieces_on_board with the starting positions of all pieces
    def init_start_positions(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(GRID_SIZE):
            black_pawn = Pawn(color="Black", position=(i, 1))
            white_pawn = Pawn(color="White", position=(i, 6))

            self.tiles[(i, 1)] = black_pawn
            self.tiles[(i, 6)] = white_pawn

        for i, piece_type in enumerate(piece_order):
            black_piece = piece_type(color="Black", position=(i, 0))
            white_piece = piece_type(color="White", position=(i, 7))

            self.tiles[(i, 0)] = black_piece
            self.tiles[(i, 7)] = white_piece

    def init_display(self, screen):    
        self.painter = BoardPainter(screen)



