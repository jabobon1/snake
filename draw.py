import pygame
import numpy as np

WIN_WIDTH = 500
WIN_HEIGHT = 570

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 150, 100)
BG = (69, 69, 69)
BROWN = (248, 77, 77)

pygame.init()
pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)

clock = pygame.time.Clock()

game = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class Grid:
    def __init__(self, grid):
        self.width = 40
        self.height = 40
        self.margin = 3
        self.columns = WIN_WIDTH // 10
        self.row = self.columns
        self.base_start = 10
        self.grid = grid

    def draw(self):
        x_row = self.base_start
        y_row = 11
        for columns in self.grid:
            for row in columns:
                if row == 2:
                    pygame.draw.rect(game, BROWN, (x_row, y_row, self.height, self.width))
                elif row == 0:
                    pygame.draw.rect(game, (250, 250, 250), (x_row, y_row, self.height, self.width))
                elif row == 1:
                    pygame.draw.rect(game, ORANGE, (x_row, y_row, self.height, self.width))

                x_row += self.columns - 1
            x_row = self.base_start
            y_row += self.row - 1

    def draw_window(self, score, level):
        # Fields on edge
        game.fill(BG)
        self.draw()
        pygame.draw.rect(game, (147, 0, 173), (0, 2, 500, 498), 8)
        score = STAT_FONT.render('Score: ' + str(score), True, (255, 255, 255))
        level = STAT_FONT.render('Level: ' + str(level), True, (255, 255, 255))
        game.blit(score, (WIN_WIDTH - 25 - score.get_width(), WIN_HEIGHT - 50))
        game.blit(level, (25, WIN_HEIGHT - 50))

        pygame.display.update()

    def event_loop(self, fps=None):
        run = True
        self.draw_window(1, 1)
        while run:
            matrix, score, run = (yield)
            self.grid = matrix
            self.draw_window(score, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Quit')
                    pygame.quit()
                    run = False
            if fps:
                clock.tick(fps)


if __name__ == '__main__':
    FPS = 3
    score = 0
    level = 1
    run = True

    grid = Grid(np.zeros((10, 10)))
    ev_loop = grid.event_loop(FPS, score, level)
    ev_loop.__next__()
    while True:
        ev_loop.send((np.zeros((10, 10)), score, True))
