from MoveValidator import (
    VerticalMoveValidator, 
    HorizontalMoveValidator, 
    DiagonalMoveValidator, 
    KnightMoveValidator, 
    SingleMoveValidator, 
    PawnMoveValidator
)
GRID_SIZE = 8

class Piece():
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.move_validators = []
        self.valid_moves = []     

    def move(self, position):
        self.position = position

    def get_png_name(self):
        return self.color.lower() + "-" + self.__class__.__name__.lower()
    
    def get_piece_type(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} at {self.position}"

    def is_valid_move(self, position):
        for move in self.valid_moves:
            if move == position: return True

    def calculate_valid_moves(self, board):
        # Clear previous valid moves
        valid_moves = []
        for validator in self.move_validators:
            initial_moves = validator.get_valid_moves(board, self.position, self.color)
            # Check if any of these moves would expose the king to an enemy attack
            filtered_moves = []
            for move in initial_moves:
                # Temporarily move piece to new position and see if the king is exposed
                original_position = self.position
                temp_piece = board.get_piece_at_position(move)
                #print("Temporarily moving " + str(temp_piece) + " and " + str(self))
                board.set_piece_at_position(self.position, None)  # Empty old position
                board.set_piece_at_position(move, self)  # Populate new possible position

                # Check if the king is exposed
                if not board.is_king_exposed(self.color):
                    filtered_moves.append(move)

                # Undo the temporary move
                board.set_piece_at_position(move, temp_piece)
                board.set_piece_at_position(original_position, self)
            valid_moves.extend(filtered_moves)

        return valid_moves
    

    def set_valid_moves(self, valid_moves):
        self.valid_moves = valid_moves

    def get_valid_moves(self):
        return self.valid_moves

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            PawnMoveValidator()
        ])


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            KnightMoveValidator()
        ])


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            DiagonalMoveValidator()
        ])


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            VerticalMoveValidator(),
            HorizontalMoveValidator()        
        ])
        self.has_moved = False

    def move(self, position):
        self.position = position


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            VerticalMoveValidator(),
            HorizontalMoveValidator(),
            DiagonalMoveValidator()
        ])

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            SingleMoveValidator()
        ])
        self.has_moved = False
        
    def move(self, position):
        #print("Moving " + str(self))
        self.position = position

    def calculate_valid_moves(self, board):
        valid_moves = super().calculate_valid_moves(board)

        # Check kingside castling
        if not self.has_moved and self.can_castle_kingside(board):
            valid_moves.append((self.position[0] + 2, self.position[1]))

        # Check queenside castling
        if not self.has_moved and self.can_castle_queenside(board):
            valid_moves.append((self.position[0] - 2, self.position[1]))

        return valid_moves

    def can_castle_kingside(self, board):
        for i in range(self.position[0] + 1, GRID_SIZE - 1):
            piece = board.get_piece_at_position((i, self.position[1]))
            if piece is not None or board.is_position_under_attack((i, self.position[1]), self.color):
                return False
        rook = board.get_piece_at_position((7, self.position[1]))
        return isinstance(rook, Rook) and not rook.has_moved

    def can_castle_queenside(self, board):
        for i in range(self.position[0] - 1, 0, -1):
            piece = board.get_piece_at_position((i, self.position[1]))
            if piece is not None or board.is_position_under_attack((i, self.position[1]), self.color):
                return False
        rook = board.get_piece_at_position((0, self.position[1]))
        return isinstance(rook, Rook) and not rook.has_moved