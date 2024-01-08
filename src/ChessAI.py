from Board import Board
import random

class ChessAI:
    def __init__(self, color):
        self.color = color

    def calculate_move(self, board):
        # Implement the minimax algorithm with alpha-beta pruning to determine the best move
        # ...
        # Return the best move (in the format used by your code)
        '''
        Code block for random piece selection and move selection (for now)
        
        ai_pieces = [piece for piece in board.tiles.values() if piece is not None and piece.color == self.color]

        if not ai_pieces:
            return None

        for selected_piece in ai_pieces:
            valid_moves = selected_piece.calculate_valid_moves(board)
            if valid_moves:
                valid_move = random.choice(valid_moves)
                print(str(selected_piece.position) + " , " + str(valid_move))
                return selected_piece.position, valid_move

        return None
        '''
        ai_pieces = [piece for piece in board.tiles.values() if piece is not None and piece.color == self.color]

        if not ai_pieces:
            return None

        _ , best_move = self.minimax(board, depth=3, maximizing_player=True)
        print(_)
        #print(f"AI Move: {best_move}")

        return best_move


    def evaluate_board(self, board):
        piece_values = {
            'Pawn': 1,
            'Knight': 3,
            'Bishop': 3,
            'Rook': 5,
            'Queen': 9,
            'King': 100
        }

        my_score = 0
        opponent_score = 0

        for piece in board.tiles.values():
            if piece:
                if piece.color == self.color:
                    my_score += piece_values.get(piece.get_piece_type(), 0)
                else:
                    opponent_score += piece_values.get(piece.get_piece_type(), 0)

        return my_score - opponent_score

    def minimax(self, board, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return self.evaluate_board(board), None

        player_pieces = [piece for piece in board.tiles.values() if piece is not None and piece.color == self.color]
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for piece in player_pieces:
                valid_moves = piece.calculate_valid_moves(board)
                for move in valid_moves:
                    captured_piece = board.tiles[move]
                    board.tiles[piece.position] = None
                    board.tiles[move] = piece
                    eval, _ = self.minimax(board, depth - 1, False, alpha, beta)
                    board.tiles[piece.position] = piece
                    board.tiles[move] = captured_piece

                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece.position, move)

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            #print(max_eval)
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for piece in player_pieces:
                valid_moves = piece.calculate_valid_moves(board)
                for move in valid_moves:
                    captured_piece = board.tiles[move]
                    board.tiles[piece.position] = None
                    board.tiles[move] = piece
                    eval, _ = self.minimax(board, depth - 1, True, alpha, beta)
                    board.tiles[piece.position] = piece
                    board.tiles[move] = captured_piece

                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece.position, move)

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            return min_eval, best_move