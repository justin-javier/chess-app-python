class Player:
    def __init__(self, player_type):
        self.player_type = player_type
        self.captured_pieces = []

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)

    def __str__(self):
        return f"Player {self.player_type.capitalize()}"