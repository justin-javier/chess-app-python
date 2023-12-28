# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE

class MoveValidator:

    def get_valid_moves(self, current_position, target_position):
        raise NotImplementedError("Subclasses must implement this method")


class VerticalMoveValidator(MoveValidator):

    def get_valid_moves(self, board, position, color):
        valid_moves = []
        # Loop from y-1 to 0
        for i in range(position[1] - 1, -1, -1):
            check_piece = board.get_piece_at_position((position[0], i))
            # If there is no piece there 
            if check_piece is None:
                valid_position = (position[0], i)
                valid_moves.append(valid_position)
            else:
                # Opposite colors
                if check_piece.color is not color:
                    valid_moves.append(check_piece.position)
                    break
                else:
                    break           

        # Loop from y+1 to 7
        for i in range(position[1] + 1, GRID_SIZE):
            check_piece = board.get_piece_at_position((position[0], i))
            if check_piece is None:
                valid_position = (position[0], i)
                valid_moves.append(valid_position)
            else:
                # Opposite colors
                if check_piece.color is not color:
                    valid_moves.append(check_piece.position)
                    break
                else:
                    break 

        return valid_moves


class HorizontalMoveValidator(MoveValidator):

    def get_valid_moves(self, board, position, color):
        valid_moves = []
        # Loop from x-1 to 0
        for i in range(position[0] - 1, -1, -1):
            check_piece = board.get_piece_at_position((i, position[1]))
            # If there is no piece there 
            if check_piece is None:
                valid_position = (i, position[1])
                valid_moves.append(valid_position)
            else:
                # Opposite colors 
                if check_piece.color is not color:
                    valid_moves.append(check_piece.position)
                    break
                else:
                    break           

        # Loop from y+1 to 7
        for i in range(position[0] + 1, GRID_SIZE):
            check_piece = board.get_piece_at_position((i, position[1]))
            if check_piece is None:
                valid_position = (i, position[1])
                valid_moves.append(valid_position)
            else:
                # Opposite colors
                if check_piece.color != color:
                    valid_moves.append(check_piece.position)
                break

        return valid_moves


class DiagonalMoveValidator(MoveValidator):

    def get_valid_moves(self, board, position, color):
        valid_moves = []

        # Loop from x-1, y-1 to 0, 0 (top-left diagonal)
        for i, j in zip(range(position[0] - 1, -1, -1), range(position[1] - 1, -1, -1)):
            check_piece = board.get_piece_at_position((i, j))
            if check_piece is None:
                valid_moves.append((i, j))
            else:
                if check_piece.color != color:
                    valid_moves.append(check_piece.position)
                break

        # Loop from x+1, y+1 to 7, 7 (bottom-right diagonal)
        for i, j in zip(range(position[0] + 1, GRID_SIZE), range(position[1] + 1, GRID_SIZE)):
            check_piece = board.get_piece_at_position((i, j))
            if check_piece is None:
                valid_moves.append((i, j))
            else:
                if check_piece.color != color:
                    valid_moves.append(check_piece.position)
                break

        # Loop from x-1, y+1 to 0, 7 (top-right diagonal)
        for i, j in zip(range(position[0] - 1, -1, -1), range(position[1] + 1, GRID_SIZE)):
            check_piece = board.get_piece_at_position((i, j))
            if check_piece is None:
                valid_moves.append((i, j))
            else:
                if check_piece.color != color:
                    valid_moves.append(check_piece.position)
                break

        # Loop from x+1, y-1 to 7, 0 (bottom-left diagonal)
        for i, j in zip(range(position[0] + 1, GRID_SIZE), range(position[1] - 1, -1, -1)):
            check_piece = board.get_piece_at_position((i, j))
            if check_piece is None:
                valid_moves.append((i, j))
            else:
                if check_piece.color != color:
                    valid_moves.append(check_piece.position)
                break

        return valid_moves

class KnightMoveValidator(MoveValidator):

    def get_valid_moves(self, board, position, color):
        valid_moves = []

        # Possible knight moves relative to its position
        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for move in knight_moves:
            new_position = (position[0] + move[0], position[1] + move[1])

            if 0 <= new_position[0] < GRID_SIZE and 0 <= new_position[1] < GRID_SIZE:
                check_piece = board.get_piece_at_position(new_position)

                if check_piece is None or check_piece.color != color:
                    valid_moves.append(new_position)

        return valid_moves


class PawnMoveValidator(MoveValidator):

    def get_valid_moves(self, board, position, color):
        valid_moves = []
        # Define the direction of pawn movement based on its color
        y_direction = -1 if color == "White" else 1

        if (color == "Black" and position[1] == 1) or (color == "White" and position[1] == 6):
            has_moved = False
        else:
            has_moved = True

        # Single step forward
        new_position = (position[0], position[1] + y_direction)
        if 0 <= new_position[0] < GRID_SIZE and 0 <= new_position[1] < GRID_SIZE:
            check_piece = board.get_piece_at_position(new_position)
            if check_piece is None:
                valid_moves.append(new_position)

                # If the pawn hasn't moved yet, allow for the double step forward
                if not has_moved:
                    new_position = (position[0], position[1] + 2 * y_direction)
                    check_piece = board.get_piece_at_position(new_position)
                    if check_piece is None:
                        valid_moves.append(new_position)

        # Diagonal captures
        capture_offsets = [(1, y_direction), (-1, y_direction)]
        for offset in capture_offsets:
            new_position = (position[0] + offset[0], position[1] + offset[1])
            if 0 <= new_position[0] < GRID_SIZE and 0 <= new_position[1] < GRID_SIZE:
                check_piece = board.get_piece_at_position(new_position)
                if check_piece is not None and check_piece.color != color:
                    valid_moves.append(new_position)

        return valid_moves


class SingleMoveValidator(MoveValidator):
   
    def get_valid_moves(self, board, position, color):
        valid_moves = []

        # Possible king moves relative to its position
        single_moves = [
            (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1),
            (-1, 0), (-1, 1)
        ]

        for move in single_moves:
            new_position = (position[0] + move[0], position[1] + move[1])

            if 0 <= new_position[0] < GRID_SIZE and 0 <= new_position[1] < GRID_SIZE:
                check_piece = board.get_piece_at_position(new_position)

                if check_piece is None or check_piece.color != color:
                    valid_moves.append(new_position)

        return valid_moves
