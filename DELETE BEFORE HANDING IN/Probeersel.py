from time import sleep


class Board:

    def __init__(self):
        pass
        # TODO setup Points

    def display(self):
        pass


# class Line:   optioneel
#
#     def __init__(self, start: int, end: int):
#         self.start = start
#         self.end = end
#
#     def display(self):
#         pass  # TODO draw line from point a to b


class Player:

    def make_move(self, board: Board):
        pass  # Empty method. Should be overridden in subclass

    def check_move(self):  # extra needed arguments.
        pass  # TODO implement here as it is the same for both Human player and AI player


class HumanPlayer(Player):

    def make_move(self, board: Board):
        pass
        # TODO ask move
        # TODO verify, if not correct ask again


class AIPlayer(Player):

    def make_move(self, board: Board):
        pass


class Game:

    def __init__(self, player1: Player, player2: Player):
        self.player2 = player2
        self.player1 = player1
        self.board = Board()

    def run(self):
        while True:
            # TODO exit event

            self.player1.make_move(self.board)
            self.board.display()
            sleep(1)
            self.player2.make_move(self.board)
            self.board.display()


game = Game(HumanPlayer(), AIPlayer())
game.run()
