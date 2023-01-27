from speech_rec import Mic as mic #BELANGRIJK
import pygame
import pyaudio


class Test:

    def __init__(self):
        pygame.init()
        self.size = (800, 800)
        self.screen = pygame.display.set_mode(self.size)
        self.time = pygame.time.get_ticks()

        self.mic = mic() #BE  #BELANGRIJK
        self.list = []

        # init Connect4
        # self.game = ConnectFour()
        # self.game_view = GameView(self.game, self.screen)

        # This function runs the game

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.update_game(delta_time)  # Runs the game

        # This functions update the game

    def update_game(self, dt):
        self.tes()

    def tes(self):
        # self.list.append(self.mic.listen())
        p1, p2 = map(int, self.mic.listen().split(","))  #BELANGRIJK
        print(p1,p2)



if __name__ == "__main__":
    test = Test()
    while True:
        test.game_loop()
