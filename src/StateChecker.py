from MoveValidator import (
    VerticalMoveValidator, 
    HorizontalMoveValidator, 
    DiagonalMoveValidator, 
    KnightMoveValidator, 
    SingleMoveValidator, 
    PawnMoveValidator
)

class CheckStateChecker(StateChecker):
    def __init__(self, board):
        self.move_validators = [
            VerticalMoveValidator(),
            HorizontalMoveValidator(),
            DiagonalMoveValidator(),
            KnightMoveValidator()
        ]

    # Check if the current state is a check
    def check_under_attack(self, board, position, color):
        for validator in self.move_validators:
            valid_moves = validator.get_valid_moves(board, position, color)
            for move in valid_moves:
                piece = board.get_piece_at_position(move)
                # If there's an enemy piece at this position with the same validator, return True
                if piece is not None and piece.color != color and validator in piece.move_validators:
                    return True
        return False

    def is_piece_pinned(self, board, piece, color):
        """
        Check if a piece is pinned by an enemy piece, meaning moving the piece would expose the king to a check.

        Args:
            board (Board): The chess board.
            piece (Piece): The piece to check for pinning.
            color (str): The color of the pieces that can pin the piece.

        Returns:
            bool: True if the piece is pinned, False otherwise.
        """
        king_position = self.find_king_position(board, color)
        
        if king_position is None:
            # Handle the case where the king is not on the board
            return False

        for enemy_piece in self.get_enemy_pieces(board, color):
            for validator in enemy_piece.move_validators:
                for target_position in validator.get_valid_moves(board, enemy_piece.position, enemy_piece.color):
                    if target_position == king_position:
                        # The enemy piece attacks the king; check if it pins the current piece
                        if self.is_valid_move_exposing_king(board, piece.position, enemy_piece.position, color):
                            return True

        return False

    def find_king_position(self, board, color):
        """
        Find the position of the king on the board.

        Args:
            board (Board): The chess board.
            color (str): The color of the king.

        Returns:
            tuple or None: The position of the king if found, None otherwise.
        """
        for row in board.tiles:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    return piece.position
        return None

    def get_enemy_pieces(self, board, color):
    """
    Get a list of enemy pieces on the board.

    Args:
        board (Board): The chess board.
        color (str): The color of the enemy pieces.

    Returns:
        list: A list of enemy pieces.
    """
    enemy_pieces = []
    for row in board.tiles:
        for piece in row:
            if piece is not None and piece.color != color:
                enemy_pieces.append(piece)
    return enemy_pieces