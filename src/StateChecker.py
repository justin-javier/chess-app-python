from ChessPieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from Board import Board


class StateChecker:

    def is_checkmate(self, board, color):
        # Check if the king is in check
        if board.is_king_exposed(color):
            print("CHECK!")
            # Iterate through all pieces of the current player
            pieces = [piece for piece in board.tiles.values() if piece and piece.color == color]
            all_moves = []
            for piece in pieces:
                all_moves.extend(piece.calculate_valid_moves(board))
                if len(all_moves) != 0:
                    return False
            return True
        return False

    def is_stalemate(self, board, color):
        # Check if the king is not in check
        if not board.is_king_exposed(color):
            # Iterate over all pieces of the specified color
            pieces = [piece for piece in board.tiles.values() if piece and piece.color == color]
            for piece in pieces:
                # Check if the piece has any valid moves
                if piece.calculate_valid_moves(board):
                    # If any piece has valid moves, it's not stalemate
                    return False
            # All pieces have no valid moves, it's stalemate
            return True
        # King is in check, not stalemate
        return False

    # Takes the color of who may have now lost
    def check_if_lost(self, board, color):
        winning_color = "White" if color == "Black" else "Black"

        # Check for checkmate
        if self.is_checkmate(board, color):
            print("Checkmate! " + winning_color + " wins!")
            #pygame.quit()
            #sys.exit()

        # Check for stalemate
        if self.is_stalemate(board, color):
            print("Stalemate! No one wins.")
            #pygame.quit()
            #sys.exit()