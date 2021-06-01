import copy
from math import inf
from typing import List

import pygame
from constants import CELL_DIMENSION
from constants import LIN
from constants import COL
from constants import DISPLAY_Y

class Game:
    def __init__(self, display, players : list, player_index: int, matrix = [["#" for i in range(LIN)] for j in range (COL)]):
        self.matrix = matrix
        # print(matrix)
        # print(matrix[LIN-1][COL-2])
        self.display = display
        self.players = players
        self.player_index = player_index
        self.player_1_moves = 0
        self.player_2_moves = 0
        self.play_time = 0
        self.number_of_generated_nodes = []
        self.minimum_generated_nodes = inf
        self.maximum_generated_nodes = -inf
        self.mean_generated_nodes = None
        self.median_generated_tinmes = None
        self.last_switch = None

    def print_in_console(self):
        for x in self.matrix:
            print(x)
        print()

    def draw(self):
        """
        Draws the current state of the game.
        """
        global CELL_DIMENSION, LIN, COL


        for i in range(LIN):
            for j in range(COL):
                color = None
                if self.matrix[i][j] == "B":
                    color = (51, 204, 255)
                elif self.matrix[i][j] == "R":
                    color = (255, 80, 80)
                else:
                    color = (255, 255, 255)

                # print("here", self.display)
                pygame.draw.rect(self.display, color,
                                 pygame.Rect(j * CELL_DIMENSION + 1 + CELL_DIMENSION * 0.5 * i, DISPLAY_Y//6 + i * CELL_DIMENSION + 1,
                                             CELL_DIMENSION,
                                             CELL_DIMENSION))
                pygame.draw.rect(self.display, (0, 0, 0),
                                 pygame.Rect(j * CELL_DIMENSION + 1 + CELL_DIMENSION * 0.5 * i, DISPLAY_Y//6 + i * CELL_DIMENSION + 1,
                                             CELL_DIMENSION,
                                             CELL_DIMENSION), 1)
                pygame.display.flip()


    def print_game_statistics(self):
        print(f"Total play time: {self.play_time}")
        print(f"Player 1 moves: {self.player_1_moves}")
        print(f"Player 2 moves: {self.player_2_moves}")
