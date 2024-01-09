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

        _ , best_move = self.minimax(board, 3, "Black")
        #print(_)
        #print(f"AI Move: {best_move}")

        return best_move


    def evaluate_board(self, board, color):
        piece_values = {
            'Pawn': 1,
            'Knight': 3,
            'Bishop': 3,
            'Rook': 5,
            'Queen': 9,
            'King': 10
        }

        my_score = 0
        opponent_score = 0

        for piece in board.tiles.values():
            if piece:
                if piece.color == color:
                    my_score += piece_values.get(piece.get_piece_type(), 0)
                else:
                    opponent_score += piece_values.get(piece.get_piece_type(), 0)
        print(str(my_score) + "," + str(opponent_score))
        return my_score - opponent_score

    def minimax(self, board, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return self.evaluate_board(board, maximizing_player), None
        #print("depth " + str(depth))
        print("alpha " + str(alpha) + " and beta " + str(beta))
        black_player_pieces = [piece for piece in board.tiles.values() if piece is not None and piece.color == "Black"]
        white_player_pieces = [piece for piece in board.tiles.values() if piece is not None and piece.color == "White"]

        best_move = None
        if maximizing_player == "Black":
            max_eval = float('-inf')
            for piece in black_player_pieces:
                valid_moves = piece.calculate_valid_moves(board)
                for move in valid_moves:
                    if depth:
                        print("piece : " + str(piece) + " | depth: " + str(depth) + " | current eval: " + str(alpha) + " | move: " + str(move))
                    original_position = piece.position

                    captured_piece = board.tiles[move]
                    board.tiles[original_position] = None
                    piece.position = move
                    board.tiles[move] = piece
                    eval, _ = self.minimax(board, depth - 1, "White", alpha, beta)
                    piece.position = original_position
                    board.tiles[original_position] = piece
                    board.tiles[move] = captured_piece

                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece.position, move)
                        #print("new best move!")
                    #print("eval for " + str(piece) +  ": " + str(eval))
                    alpha = max(alpha, max_eval)

                    if beta <= alpha:
                        print("PRUNING")
                        break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for piece in white_player_pieces:
                valid_moves = piece.calculate_valid_moves(board)
                for move in valid_moves:
                    if depth:
                        print("piece : " + str(piece) + " | depth: " + str(depth) + " | current eval: " + str(alpha) + " | move: " + str(move))                    
                    original_position = piece.position

                    captured_piece = board.tiles[move]
                    board.tiles[original_position] = None
                    piece.position = move
                    board.tiles[move] = piece
                    eval, _ = self.minimax(board, depth - 1, "Black", alpha, beta)
                    eval = -eval
                    piece.position = original_position
                    board.tiles[original_position] = piece
                    board.tiles[move] = captured_piece

                    if eval < min_eval:
                        min_eval = eval
                        best_move = (original_position, move)
                    beta = min(beta, min_eval)

                    if beta <= alpha:
                        print("PRUNING")
                        break
            return min_eval, best_move

