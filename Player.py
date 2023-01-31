from Board import Board

class Player:
    def __init__(self, moves_done):
        self.moves_done = moves_done

        self.id_to_index = Board.id_to_index
        self.check_move_made_box = Board.check_move_made_box


    def move(self, is_user, id1, id2, board):  # SPEECH?
        # connects id1 and id2
        board[self.id_to_index(id1)].partners.append(id2)
        board[self.id_to_index(id2)].partners.append(id1)
        self.moves_done.append((id1, id2))
        self.moves_done_persons.append(is_user)
        return self.check_move_made_box(is_user, id1, id2)