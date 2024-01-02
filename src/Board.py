import pygame
import os
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from BoardPainter import BoardPainter
from MoveValidator import (
    VerticalMoveValidator, 
    HorizontalMoveValidator, 
    DiagonalMoveValidator, 
    KnightMoveValidator, 
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
        self.king_positions = {"White": None, "Black": None}
        self.painter = BoardPainter()

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

    def get_piece_at_position(self, position):
        return self.tiles.get(position)

    def set_piece_at_position(self, position, piece):
        if piece is not None:
            piece.move(position)
            if isinstance(piece, King):
                self.king_positions[piece.color] = position
        self.tiles[position] = piece

    # Sets all the valid moves for every piece
    def set_all_valid_moves(self):
        for position in self.tiles.values():
            piece = self.get_piece_at_position(position)
            if piece is not None:
                valid_moves = piece.calculate_valid_moves(self)
                piece.set_valid_moves(valid_moves)

    '''
    Given the board's piece layout, check if a king is in check.
    When calculating a piece's valid moves, we temporarily alter the board to a state where
    a potential valid move is made, then check if it exposes the king.
    Otherwise, if called on a non-altered board state, it will return True if there is a current check
    '''
    def is_king_exposed(self, color):
        # Get king position
        king_position = self.king_positions[color]
        # Check each of the relevant validators
        for validator in [VerticalMoveValidator(), HorizontalMoveValidator(), DiagonalMoveValidator(), KnightMoveValidator()]:
            # Calculate valid moves per validator
            moves = validator.get_valid_moves(self, king_position, color)
            # Check if any of the moves ends with an enemy piece that has the same validator
            for move in moves:
                piece = self.get_piece_at_position(move)
                if piece is not None:
                    for piece_validator in piece.move_validators:
                        if piece_validator.get_type() == validator.get_type():
                            return True
        return False

    def is_checkmate(self, color):
        # Check if the king is in check
        if self.is_king_exposed(color):
            print("CHECK!")
            # Iterate through all pieces of the current player
            pieces = [piece for piece in self.tiles.values() if piece and piece.color == color]
            all_moves = []
            for piece in pieces:
                all_moves.extend(piece.calculate_valid_moves(self))

            return len(all_moves) == 0
        return False

        # If there are no legal moves, it's checkmate
        return len(all_moves) == 0

    def is_stalemate(self, color):
        # Check if the king is not in check
        if not self.is_king_exposed(color):
            # Iterate over all pieces of the specified color
            pieces = [piece for piece in self.tiles.values() if piece and piece.color == color]
            for piece in pieces:
                # Check if the piece has any valid moves
                if piece.calculate_valid_moves(self):
                    # If any piece has valid moves, it's not stalemate
                    return False
            # All pieces have no valid moves, it's stalemate
            return True
        # King is in check, not stalemate
        return False

    # Populate the pieces_on_board with the starting positions of all pieces
    def init_start_positions(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(GRID_SIZE):
            black_pawn = Pawn(color="Black", position=(i, 1))
            white_pawn = Pawn(color="White", position=(i, 6))

            self.set_piece_at_position((i, 1), black_pawn)
            self.set_piece_at_position((i, 6), white_pawn)

        for i, piece_type in enumerate(piece_order):
            black_piece = piece_type(color="Black", position=(i, 0))
            white_piece = piece_type(color="White", position=(i, 7))

            self.set_piece_at_position((i, 0), black_piece)
            self.set_piece_at_position((i, 7), white_piece)

