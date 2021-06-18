import numpy as np
import pygame as pygame
from pygame.rect import Rect
import random
from graphics.GraphicInterface import GraphicInterface

DISPLAY_FPS = 1200

BLOCK_SIZE = 30
LINE_SIZE = round(BLOCK_SIZE / 10)

COLOR_BACKGROUND = (20, 20, 20)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (189, 189, 189)
COLOR_BLACK = (20, 20, 20)
COLOR_RED = (229, 58, 64)
COLOR_BLOCK = [(229, 58, 64), # red
               (239, 220, 5), # yellow
               (48, 169, 222), # sky blue
               (246, 179, 82), # gold
               (140, 215, 144), # green
               (239, 158, 159), # pink
               (144, 85, 162), # purple
               (94, 94, 95) # gray
               ]


class GraphicModule(GraphicInterface):

    def __init__(self, settings):

        self._board_height = settings.GRID_HEIGHT
        self._board_width = settings.GRID_WIDTH
        self._screen_width = self._board_width * BLOCK_SIZE + 60
        self._screen_height = self._board_height * BLOCK_SIZE + 100

        self.tetris_model = None

        self._tetromino_y = 0
        self._tetromino_x = 0

        self._interface_board = np.zeros((self._board_height, self._board_width))

        pygame.init()
        pygame.display.set_caption("INnS Lab. TETRIS AI")
        self._font_obj = pygame.font.SysFont("comicsansms", BLOCK_SIZE)
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._screen.fill(COLOR_BACKGROUND)
        pygame.draw.rect(self._screen, COLOR_BLACK,
                         Rect(BLOCK_SIZE - LINE_SIZE, BLOCK_SIZE - LINE_SIZE,
                              self._board_width * BLOCK_SIZE + LINE_SIZE * 2,
                              self._board_height * BLOCK_SIZE + LINE_SIZE * 2),
                         0)
        pygame.display.update()

    # Graphic API

    def set_tetris_model(self, tetris_model):
        self.tetris_model = tetris_model

    def draw_graphic(self, tetromino_y, tetromino_x):
        self._tetromino_y = tetromino_y
        self._tetromino_x = tetromino_x

        self._update_screen()
        pygame.time.Clock().tick(DISPLAY_FPS)

    def pump_event(self):
        pygame.event.pump()

    # UI Draw

    def _update_screen(self):
        pygame.draw.rect(self._screen, COLOR_BACKGROUND,
                         Rect(BLOCK_SIZE, BLOCK_SIZE, self._board_width * BLOCK_SIZE, self._board_height * BLOCK_SIZE),
                         0)

        pygame.draw.rect(self._screen, COLOR_BACKGROUND,
                         Rect(self._screen_width - 300, BLOCK_SIZE, self._screen_width, self._screen_height),
                         0)

        self._draw_score_info()
        self._interface_board = np.reshape(self.tetris_model.get_board_data(), (self._board_height, self._board_width))

        if self._tetromino_x is not -1:
            self._draw_tetromino()
            self._draw_ghost_tetromino()

        for y in range(self._board_height):
            for x in range(self._board_width):
                if self._interface_board[y][x] != 0:
                    self._draw_block(y, x, COLOR_BLOCK[self._interface_board[y][x] - 1])
        pygame.display.update()

    def _draw_score_info(self):
        text_obj = self._font_obj.render("Total Score: " + str(round(self.tetris_model.score)), True, COLOR_WHITE)
        self._screen.blit(text_obj, (50, self._screen_height - 50))

        #text_obj2 = self._font_obj.render("Reward: " + str(random.randrange(50,100)), True, COLOR_RED)
        #self._screen.blit(text_obj2, (20, 30))


    def _draw_tetromino(self):
        for col in range(len(self.tetris_model.current_tetromino)):
            for row in range(len(self.tetris_model.current_tetromino[0])):
                if self._interface_board[self._tetromino_y + col][self._tetromino_x + row] == 0 \
                        and self.tetris_model.current_tetromino[col][row] == 1:
                    self._interface_board[self._tetromino_y + col][self._tetromino_x + row] \
                        = self.tetris_model.current_shape_code + 2

    def _draw_ghost_tetromino(self):
        temp_y = 0
        while self.tetris_model.can_move_block(temp_y + 1, self._tetromino_x):
            temp_y += 1
        for col in range(len(self.tetris_model.current_tetromino)):
            for row in range(len(self.tetris_model.current_tetromino[0])):
                if self.tetris_model.current_tetromino[col][row] == 1:
                    self._draw_ghost_block(temp_y + col, self._tetromino_x + row)

    def _draw_block(self, y, x, color):
        pygame.draw.rect(self._screen, color,
                         Rect((x + 1) * BLOCK_SIZE + LINE_SIZE / 2, (y + 1) * BLOCK_SIZE + LINE_SIZE / 2,
                              BLOCK_SIZE - LINE_SIZE / 2, BLOCK_SIZE - LINE_SIZE / 2),
                         0)
        pygame.draw.rect(self._screen, COLOR_WHITE,
                         Rect((x + 1) * BLOCK_SIZE + LINE_SIZE / 2, (y + 1) * BLOCK_SIZE + LINE_SIZE / 2,
                              BLOCK_SIZE - LINE_SIZE / 2, BLOCK_SIZE - LINE_SIZE / 2),
                         LINE_SIZE)

    def _draw_ghost_block(self, y, x):
        pygame.draw.rect(self._screen, COLOR_GRAY,
                         Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0)
