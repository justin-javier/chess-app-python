import pygame
import os
from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from BoardPainter import BoardPainter

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
        self.painter = BoardPainter()

    def set_selected_piece(self, piece):
        if piece is not None: 
            piece.set_valid_moves(self)   
            #print("Valid Moves: " + str(piece.get_valid_moves()))   

        sp = self.selected_piece
        if sp is None:
            self.last_valid_moves = piece.get_valid_moves()
        else:
            self.last_valid_moves = sp.get_valid_moves()
        #print("Last Valid Moves: " + str(self.last_valid_moves))
        self.selected_piece = piece

    def get_piece_at_position(self, position):
        x, y = position
        return self.tiles[x][y]

    def set_piece_at_position(self, position, piece):
        x, y = position
        if piece is not None:
            piece.move(position)
        self.tiles[x][y] = piece

    # Sets all the valid moves for every piece
    def set_all_valid_moves(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                piece = self.get_piece_at_position((row, col))
                if piece is not None:
                    piece.set_valid_moves(self)

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
