from math import inf

from algorithms import min_max, alpha_beta
import pygame
from constants import CELL_DIMENSION, LIN, COL, DISPLAY_Y
import sys
from algorithms import is_final
import time

def valid_choice(current_state, cell_x, cell_y):
    return cell_x < LIN and \
           cell_y < COL and \
           current_state.matrix[cell_x][cell_y] == '#'

def switch_players(game):
    if game.player_index==0:
        game.player_index = 1
        return
    game.player_index=0

class Player:
    def __init__(self, type, color, algorithm=None, estimation=None, difficulty=None):
        self.type = type
        self.min_max = None
        if color == 0:
            self.color = 'R'
        else:
            self.color = 'B'
        if self.type == 1:
            if algorithm==0:
                self.algorithm = min_max
            else:
                self.algorithm = alpha_beta
            self.estimation = estimation
            if difficulty == 0:
                self.depth = 1
            elif difficulty == 1:
                self.depth = 2
            elif difficulty == 2:
                self.depth = 3
        else:
            self.algorithm = None
            self.estimation = None
            self.depth = None
        self.minimum_thinking_time = inf
        self.maximum_thinking_time = -inf
        self.mean_thinking_time = None
        self.median_thinking_time = None
        self.thinking_times = []
        self.minimum_nodes = inf
        self.maximum_nodes = -inf
        self.mean_nodes = None
        self.median_nodes = None
        self.nodes = []


    def move(self, current_state):
        """
        Performs a move, based on the type of the player.
        """
        start_time = time.time()
        if self.type == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    current_state.print_game_statistics()
                    self.print_statistics()
                    current_state.players[1-current_state.player_index].print_statistics()
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Calculating the cell the player clicked on based on the position of the mouse.
                    cell_x = (pos[1] - DISPLAY_Y//6) // CELL_DIMENSION
                    cell_y = (pos[0] // (CELL_DIMENSION // 2) - cell_x) // 2

                    if valid_choice(current_state, cell_x, cell_y):
                        current_state.matrix[cell_x][cell_y] = self.color
                        # if is_final(current_state.matrix, self.color):
                        #     print(f"A castigat {self.color} ")
                        #     return
                        now = time.time()
                        print(
                            f"Thinking time of player {self.color} was {now-current_state.last_switch} s.")
                        current_state.last_switch = now
                        if current_state.player_index==0:
                            current_state.player_1_moves += 1
                        else:
                            current_state.player_2_moves+=1
                        switch_players(current_state)

                        stop_time = time.time()
                        self.thinking_times.append(stop_time - start_time)
                        self.minimum_thinking_time = min(self.minimum_thinking_time, self.thinking_times[-1])
                        self.maximum_thinking_time = max(self.maximum_thinking_time, self.thinking_times[-1])
                        self.mean_thinking_time = sum(self.thinking_times) / len(self.thinking_times)
                        mid = len(self.thinking_times) // 2
                        self.median_thinking_time = self.thinking_times[mid]
                        return True

        else:
            estimation, nodes = self.algorithm(current_state.matrix, self.estimation, self.depth, self.color, self.min_max, current_state)
            print(f"Estimation given by the computer is {estimation}.")
            print(f"Number of nodes generated: {nodes}")
            self.nodes.append(nodes)
            self.minimum_nodes = min(self.minimum_nodes, nodes)
            self.maximum_nodes = max(self.maximum_nodes, nodes)
            self.mean_nodes = sum(self.nodes) / len(self.nodes)
            self.median_nodes = self.nodes[len(self.nodes)//2]
            if current_state.player_index == 0:
                current_state.player_1_moves += 1
            else:
                current_state.player_2_moves += 1
            now = time.time()
            print(
                f"Thinking time of player {self.color} was {now - current_state.last_switch} s.")
            current_state.last_switch = now
            switch_players(current_state)
            stop_time = time.time()
            self.thinking_times.append(stop_time - start_time)
            self.minimum_thinking_time = min(self.minimum_thinking_time, self.thinking_times[-1])
            self.maximum_thinking_time = max(self.maximum_thinking_time, self.thinking_times[-1])
            self.mean_thinking_time = sum(self.thinking_times) / len(self.thinking_times)
            mid = len(self.thinking_times) // 2
            self.median_thinking_time = self.thinking_times[mid]

            return True
        return False


    def print_statistics(self):
        print(f"Minimum thinking time: {self.minimum_thinking_time}")
        print(f"Maximum thinking time: {self.maximum_thinking_time}")
        print(f"Mean thinking time: {self.mean_thinking_time}")
        print(f"Medial thinking time: {self.median_thinking_time}")

        if self.type==1:
            print(f"Minimum nodes generated: {self.minimum_nodes}")
            print(f"Maximum nodes generated: {self.maximum_nodes}")
            print(f"Mean nodes generated: {self.mean_nodes}")
            print(f"Median nodes generated: {self.median_nodes}")




