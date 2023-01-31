class Game:
    def __init__(self, BOARDSIZE):
        self.boardsize = BOARDSIZE
        self.size = self.broadsize * 100 + 100
        self.SURF = pygame.display.set_mode((self.size, self.size))

    def gameLoop(self):
        SURF.fill((255, 255, 255))
        disp_board()
        pygame.display.update()

        while True:
            # write event handlers here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # clear the screen before drawing
            SURF.fill((255, 255, 255))
            is_user_turn = True
            disp_board()
            pygame.display.update()
            user_move()
            disp_board()
            # display what was drawn
            pygame.display.update()
            # sleep(0.5)
            is_user_turn = False
            disp_board()
            pygame.display.update()
            sleep(0.5)
            decide_and_move()
            check_complete()
            SURF.fill((255, 255, 255))
            disp_board()
            pygame.display.update()
            sleep(0.5)
            # sleep(1.5)
            # run at 20 fps
            # clock.tick(20)