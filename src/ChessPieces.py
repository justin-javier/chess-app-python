from MoveValidator import (
    VerticalMoveValidator, 
    HorizontalMoveValidator, 
    DiagonalMoveValidator, 
    KnightMoveValidator, 
    SingleMoveValidator, 
    PawnMoveValidator
)

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

    def set_valid_moves(self, board):
        # Clear previous valid moves
        self.valid_moves = []
        for validator in self.move_validators:
            self.valid_moves.extend(validator.get_valid_moves(board, self.position, self.color))

    def get_valid_moves(self):
        return self.valid_moves

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            PawnMoveValidator()
        ])

    def special_pawn_method(self):
        print(f"This is a special method for {self.__class__.__name__}")

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            KnightMoveValidator()
        ])

    def special_knight_method(self):
        print(f"This is a special method for {self.__class__.__name__}")

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            DiagonalMoveValidator()
        ])

    def special_bishop_method(self):
        print(f"This is a special method for {self.__class__.__name__}")

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            VerticalMoveValidator(),
            HorizontalMoveValidator()        
        ])

    def special_rook_method(self):
        print(f"This is a special method for {self.__class__.__name__}")

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            VerticalMoveValidator(),
            HorizontalMoveValidator(),
            DiagonalMoveValidator()
        ])

    def special_queen_method(self):
        print(f"This is a special method for {self.__class__.__name__}")

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.move_validators.extend([
            SingleMoveValidator()
        ])

    def special_king_method(self):
        print(f"This is a special method for {self.__class__.__name__}")