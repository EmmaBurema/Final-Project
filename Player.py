class Player:
    def __init__(self):


def move(is_user, id1, id2):  # SPEECH?
    # connects id1 and id2
    # depends on somebody else to check if move is valid
    board[id_to_index(id1)].partners.append(id2)
    board[id_to_index(id2)].partners.append(id1)
    moves_done.append((id1, id2))
    moves_done_persons.append(is_user)
    return check_move_made_box(is_user, id1, id2)
