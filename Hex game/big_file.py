import copy
import time
from math import inf
import sys
import pygame
from typing import List
from dijkstar import Graph, find_path
import pygame
CELL_DIMENSION = 40
LIN = 5
COL = 5
DISPLAY_X = max(int(COL* CELL_DIMENSION +CELL_DIMENSION*0.5*(LIN-1)+1), 300)
DISPLAY_Y = max(CELL_DIMENSION*LIN, 300)
DISPLAY_Y += DISPLAY_Y//5
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 32)
GAME_H_OFFSET = 50
COLOR = (140, 255, 238)

player_1 = None
player_2 = None
estimation_1 = None
estimation_2 = None
algorithm_1 = None
algorithm_2 = None
difficulty_1 = None
difficulty_2 = None
color_1 = None
color_2 = None


def switch_color(color):
    if color == "B":
        return "R"
    return "B"

def switch_min_max(min_max):
    if min_max=="min":
        return "max"
    return "min"


from math import inf

from constants import LIN, COL


def DFS(matrix, x, y, final_x, final_y, viz):
    if viz[x][y] == False:
        viz[x][y] = True
        if x == final_x or y == final_y:
            return (x, y)  # returns the position of the player that won

        current = matrix[x][y]
        # directly up
        if x - 1 >= 0 and viz[x - 1][y] == False and matrix[x - 1][y] == current:
            return DFS(matrix, x - 1, y, final_x, final_y, viz)
        # diagonally up
        if x - 1 >= 0 and y + 1 < COL and viz[x - 1][y + 1] == False and matrix[x - 1][y + 1] == current:
            return DFS(matrix, x - 1, y + 1, final_x, final_y, viz)
        # left
        if y - 1 >= 0 and viz[x][y - 1] == False and matrix[x][y - 1] == current:
            return DFS(matrix, x, y - 1, final_x, final_y, viz)
        # right
        if y + 1 < COL and viz[x][y + 1] == False and matrix[x][y + 1] == current:
            return DFS(matrix, x, y + 1, final_x, final_y, viz)
        # diagonally down
        if x + 1 < LIN and y - 1 >= 0 and viz[x + 1][y - 1] == False and matrix[x + 1][y - 1] == current:
            return DFS(matrix, x + 1, y - 1, final_x, final_y, viz)
        # directly down
        if x + 1 < LIN and viz[x + 1][y] == False and matrix[x + 1][y] == current:
            return DFS(matrix, x + 1, y, final_x, final_y, viz)

def check(x, y):
    if x>=0 and y>=0 and x<LIN and y<COL:
        return True
    return False

def max_path(matrix, color):
    viz = [[False for i in range(LIN)] for j in range(COL)]

    dx = [-1,-1,0,0,1,1]
    dy = [0,1,1,-1,0,-1]

    max_path = 0
    min_lin = inf
    min_col = inf
    max_col = -inf
    max_lin = -inf

    for x in range(LIN):
        for y in range(COL):
            if viz[x][y]==False and matrix[x][y]==color:
                queue = []
                queue.append((x,y))
                while len(queue)>0:
                    curr = queue[0]
                    curr_y = curr[1]
                    curr_x = curr[0]
                    queue.pop(0)
                    viz[curr_x][curr_y] = True

                    min_lin = min(min_lin, curr_x)
                    max_lin = max(max_lin, curr_x)
                    min_col = min(min_col, curr_y)
                    max_col = max(max_col, curr_y)

                    for i in range(6):
                        new_x = curr_x + dx[i]
                        new_y = curr_y + dy[i]
                        if check(new_x, new_y) and matrix[new_x][new_y]==color and viz[new_x][new_y]==False:
                            queue.append((new_x, new_y))
            if color == "R":
                # print(max_lin, min_lin)
                max_path=max(max_path, max_lin-min_lin+1)
            elif color=="B":
                max_path=max(max_col-min_col+1, max_path)

    return max_path




def convert_tuple_to_int(x):
    return x[0] * COL + x[1]


def is_final(matrix, color):
    if color == "R":
        for i in range(COL):
            if matrix[0][i] == "R":
                viz = [[False for i in range(LIN)] for j in range(COL)]
                val = DFS(matrix, 0, i, LIN-1, None, viz)
                if val != None:
                    return True
    elif color == "B":
        for i in range(COL):
            if matrix[i][0] == "B":
                viz = [[False for i in range(LIN)] for j in range(COL)]
                val = DFS(matrix, i, 0, None, COL-1, viz)
                if val != None:
                    return True

    return False

def min_max(state, estimation, depth, color, min_max_var, game):

    # Make an actual State from the matrix given.
    current_state = State(matrix=state, min_max_var=min_max_var, depth=depth, parent=None, estimation_name=estimation, color=color)
    nodes=1
    # print(f"depth {depth} {current_state}")
    # If we reached maximum depth allowed.
    if current_state.depth == 0:
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1
    # Or if one of the players already won.
    if is_final(current_state.matrix, color):
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1
    elif is_final(current_state.matrix, switch_color(color)):
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1

    # Else, we generate the next moves.
    current_state.generate_moves()
    nodes+=len(current_state.moves)
    for i in range(len(current_state.moves)):
        move = current_state.moves[i]
        # Get an estimation for each one of them.
        move.estimation, add_nodes = min_max(move.matrix, estimation, depth-1, switch_color(color), switch_min_max(min_max_var), game)
        nodes+= add_nodes
    estimation_for_moves = current_state.moves

    # print("Next moves:")
    # for elem in estimation_for_moves:
    #     print(f"{elem} {elem.estimation}")
    if len(estimation_for_moves) == 0:
        current_state.estimation = current_state.estimate(estimation)

    # An pck one of them as a next move depending if we're minimizing or maximizing.
    if min_max_var == "max":
        current_state.next_step = max(estimation_for_moves, key = lambda x : x.estimation)
    else:
        current_state.next_step = min(estimation_for_moves, key=lambda x: x.estimation)

    # Modify the current estimation.
    current_state.estimation = current_state.next_step.estimation + 1
    game.matrix = current_state.next_step.matrix
    return current_state.estimation, nodes
def alpha_beta(state, estimation, depth, color, min_max_var, game, alpha=-inf, beta=inf, nodes = 0):
    # Make an actual State from the matrix given.
    current_state = State(matrix=state, min_max_var=min_max_var, depth=depth, parent=None, estimation_name=estimation,
                          color=color)
    nodes = 1
    # print(f"depth {depth} {current_state} {color}")
    # If we reached maximum depth allowed.
    if current_state.depth == 0:
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1
    # Or if one of the players already won.
    if is_final(current_state.matrix, color):
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1
    elif is_final(current_state.matrix, switch_color(color)):
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1

    if alpha > beta:
        current_state.estimation = current_state.estimate(estimation, min_max_var)
        return current_state.estimation, 1



    # Else, we generate the next moves.
    current_state.generate_moves()

    if len(current_state.moves) == 0:
        current_state.estimation = current_state.estimate(estimation)
        return current_state.estimation, 1

    # for node in current_state.moves:
    #     node.estimate(min_max_var, estimation)
    # print([x.estimation for x in current_state.moves])
    # # sorted(current_state.moves, key = lambda x : x.estimation)

    if min_max_var == "max":
        current_estimation = -inf
        for move in current_state.moves:
            new_estimation, gen_nodes = alpha_beta(state=move.matrix, estimation=estimation,
                                        depth=depth-1, min_max_var=switch_min_max(min_max_var),
                                        alpha=alpha, beta=beta, color = switch_color(color),
                                        game = game)
            nodes+=gen_nodes
            move.estimation = copy.deepcopy(new_estimation)
            if current_estimation <= new_estimation:
                current_state.next_step = copy.deepcopy(move)
                current_estimation = copy.deepcopy(new_estimation)
            if alpha < new_estimation:
                new_estimation = alpha
                if alpha >= beta:
                    break
    elif min_max_var == "min":
        current_estimation = inf
        for move in current_state.moves:
            new_estimation, gen_nodes = alpha_beta(state=move.matrix, estimation=estimation,
                                        depth=depth-1, min_max_var=switch_min_max(min_max_var),
                                        alpha=alpha, beta=beta, color = switch_color(color),
                                        game = game)
            nodes+=gen_nodes
            move.estimation =copy.deepcopy(new_estimation)
            if current_estimation >= new_estimation:
                current_state.next_step = copy.deepcopy(move)
                current_estimation = copy.deepcopy(new_estimation)
            if new_estimation < beta:
                beta = min(beta, new_estimation)
                if alpha >= beta:
                    break

    current_state.estimation = copy.deepcopy(current_state.next_step.estimation)
    game.matrix = copy.deepcopy(current_state.next_step.matrix)
    return current_state.estimation, nodes

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


class State:
    def __init__(self, matrix : List[List[str]], min_max_var: str, depth: int, estimation_name: int, color : str, parent = None):
        self.matrix = matrix
        self.min_max_var = min_max_var
        self.depth = depth
        self.parent = parent
        self.estimation = None
        self.estimation_name = estimation_name
        self.moves = []
        self.next_step = None
        self.color = color
        self.red_graph = Graph(undirected=True)
        self.blue_graph = Graph(undirected=True)
        # If this is the root node for the algorithms we construct the graphs from the matrix.
        self.red_source = convert_tuple_to_int((0, -1))
        self.red_dest = convert_tuple_to_int((LIN, COL))
        self.blue_source = convert_tuple_to_int((0, -2))
        self.blue_dest = convert_tuple_to_int((LIN + 1, COL + 1))
        if parent == None:
            self.add_all_neighbours_red()
            self.add_all_neighbours_blue()
        else:
            self.create_red_graph_based_on_parent()
            self.create_blue_graph_based_on_parent()
        # print(self.blue_graph)
        # print(self.red_graph)

    def create_red_graph_based_on_parent(self):
        self.red_graph=copy.deepcopy(self.parent.red_graph)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != self.parent.matrix[i][j]:
                    if self.matrix[i][j]=="B":
                        self.red_graph.remove_node(convert_tuple_to_int((i, j)))
                    elif self.matrix[i][j]=="R":
                        curr_node = convert_tuple_to_int((i, j))
                        incoming = self.red_graph.get_incoming(curr_node)
                        self.red_graph.remove_node(curr_node)
                        for node1 in incoming.keys():
                            for node2 in incoming.keys():
                                self.red_graph.add_edge(node1, node2, 1)

    def create_blue_graph_based_on_parent(self):
        self.blue_graph=copy.deepcopy(self.parent.blue_graph)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != self.parent.matrix[i][j]:
                    if self.matrix[i][j]=="R":
                        self.blue_graph.remove_node(convert_tuple_to_int((i, j)))
                    elif self.matrix[i][j]=="B":
                        curr_node = convert_tuple_to_int((i, j))
                        incoming = self.blue_graph.get_incoming(curr_node)
                        self.blue_graph.remove_node(curr_node)
                        for node1 in incoming.keys():
                            for node2 in incoming.keys():
                                self.blue_graph.add_edge(node1, node2, 1)


    def add_all_neighbours_red(self):
        # We add all og the nodes in the matrix as a node in the graph, except for the blue ones for red.
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != "B":
                    curr_node = convert_tuple_to_int((i,j))
                    self.red_graph.add_node(curr_node)
                    # Neighbours from previuos line.
                    if i >= 1:
                        if self.matrix[i-1][j] != "B":
                            next_node = convert_tuple_to_int((i-1, j))
                            self.red_graph.add_edge(curr_node, next_node, 1)
                        if j < COL - 1:
                            if self.matrix[i-1][j+1] != "B":
                                next_node = convert_tuple_to_int((i - 1, j + 1))
                                self.red_graph.add_edge(curr_node, next_node, 1)
                    # Neighbours from next line.
                    if i < LIN - 1:
                        if self.matrix[i+1][j] != "B":
                            next_node = convert_tuple_to_int((i + 1, j))
                            self.red_graph.add_edge(curr_node, next_node, 1)
                        if j >= 1:
                            if self.matrix[i+1][j-1] != "B":
                                next_node = convert_tuple_to_int((i + 1, j - 1))
                                self.red_graph.add_edge(curr_node, next_node, 1)
                    if j >= 1 and self.matrix[i][j-1]!= "B":
                        next_node = convert_tuple_to_int((i, j - 1))
                        self.red_graph.add_edge(curr_node, next_node, 1)
                    if j < COL - 1 and self.matrix[i][j+1] != "B":
                            next_node = convert_tuple_to_int((i, j + 1))
                            self.red_graph.add_edge(curr_node, next_node, 1)

        # print(f"matrice: {self.matrix}")
        # print(f"dupa adaugarea grafului complet: {self.red_graph}")

        # Lastly, we add the source and destination nodes.
        self.red_graph.add_node(self.red_source)
        self.red_graph.add_node(self.red_dest)
        for i in range(COL):
            self.red_graph.add_edge(self.red_source, convert_tuple_to_int((0, i)), 1)
            self.red_graph.add_edge(convert_tuple_to_int((LIN - 1, i)), self.red_dest, 1)

        # print(f"dupa adaugarea source si dest {self.red_graph}")

        # For the red ones, we delete all of the edges out of a red node and replace them with
        # direct conncetions of the adjecent nodes.
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j]=="R":
                    curr_node = convert_tuple_to_int((i, j))
                    incoming = self.red_graph.get_incoming(curr_node)
                    self.red_graph.remove_node(curr_node)
                    for node1 in incoming.keys():
                        for node2 in incoming.keys():
                            self.red_graph.add_edge(node1, node2, 1)

        # print(f"dupa stergerea nodurilor rosii: {self.red_graph}")
        # print()


    def add_all_neighbours_blue(self):
        # We add all of the nodes in the matrix as a node in the graph, except for the blue ones for blue.
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j]!= "R":
                    curr_node = convert_tuple_to_int((i, j))
                    self.blue_graph.add_node(curr_node)
                    # neighbours from the last line
                    if i >= 1:
                        if self.matrix[i - 1][j] != "R":
                            next_node = convert_tuple_to_int((i - 1, j))
                            self.blue_graph.add_edge(curr_node, next_node, 1)
                        if j < COL - 1 and self.matrix[i - 1][j + 1] != "R":
                            next_node = convert_tuple_to_int((i - 1, j + 1))
                            self.blue_graph.add_edge(curr_node, next_node, 1)
                    #neighbours from the next line
                    if i < LIN - 1:
                        if self.matrix[i + 1][j] != "R":
                            next_node = convert_tuple_to_int((i + 1, j))
                            # print(f"se adauga aici {curr_node} {next_node}")
                            self.blue_graph.add_edge(curr_node, next_node, 1)
                        # print(self.blue_graph)
                        if j >= 1:
                            if self.matrix[i + 1][j - 1] != "R":
                                next_node = convert_tuple_to_int((i + 1, j - 1))
                                self.blue_graph.add_edge(curr_node, next_node, 1)
                    if j >= 1 and self.matrix[i][j - 1] != "R":
                        next_node = convert_tuple_to_int((i, j - 1))
                        self.blue_graph.add_edge(curr_node, next_node, 1)
                    if j < COL - 1 and self.matrix[i][j + 1] != "R":
                        next_node = convert_tuple_to_int((i, j + 1))
                        self.blue_graph.add_edge(curr_node, next_node, 1)

        # print(f"matrice: {self.matrix}")
        # print(f"dupa adaugarea grafului complet: {self.blue_graph}")

        # Lastly, we add the source and destination nodes.
        self.blue_graph.add_node(self.blue_source)
        self.blue_graph.add_node(self.blue_dest)
        for i in range(LIN):
            self.blue_graph.add_edge(self.blue_source, convert_tuple_to_int((i, 0)), 1)
            # print(f"source {self.blue_source} {(i,0)} {convert_tuple_to_int((i, 0))}")
            self.blue_graph.add_edge(convert_tuple_to_int((i, COL - 1)), self.blue_dest, 1)
            # print(f"{(i, COL-1)} {convert_tuple_to_int((i, COL-1))} dest {self.blue_dest}")

        # print(f"dupa adaugarea source si dest {self.blue_graph}")

        # For the red ones, we delete al of the edges out of a red node and replace them with
        # direct conncetions of the adjecent nodes.
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j]=="B":
                    curr_node = convert_tuple_to_int((i, j))
                    incoming = self.blue_graph.get_incoming(curr_node)
                    self.blue_graph.remove_node(curr_node)
                    for node1 in incoming.keys():
                        for node2 in incoming.keys():
                            self.blue_graph.add_edge(node1, node2, 1)
        # print(f"dupa stergerea nodurilor albastre: {self.blue_graph}")
        # print()


    def generate_moves(self):
        for i in range (len(self.matrix)):
            for j in range (len(self.matrix[i])):
                if self.matrix[i][j] == "#":
                    new_matrix = [[x for x in y] for y in self.matrix]
                    new_matrix[i][j] = self.color
                    new_state = State(matrix=new_matrix, min_max_var=switch_min_max(self.min_max_var),
                                      depth=self.depth-1, estimation_name=self.estimation_name, color = switch_color(self.color))
                    self.moves.append(new_state)

    def estimate(self, estimation, min_max_var):
        # Depending on the type of estimation the user chose.
        if estimation == 0:
            red_est = max_path(self.matrix, "R")
            blue_est = max_path(self.matrix, "B")
            if min_max_var=="max":
                if self.color=="R":
                    return red_est-blue_est
                else:
                    return blue_est-red_est
            else:
                if self.color=="R":
                    return blue_est-red_est
                else:
                    return red_est-blue_est
        elif estimation==1:
            try:
                red_est = find_path(self.red_graph, self.red_source, self.red_dest).total_cost
            except:
                red_est = None
            try:
                blue_est = find_path(self.blue_graph, self.blue_source, self.blue_dest).total_cost
            except:
                blue_est = None
            if self.color == "R":
                if red_est == None and min_max_var=="max":
                    return -inf
                if red_est == None and min_max_var=="min":
                    return inf
                if blue_est == None and min_max_var=="min":
                    return red_est
                if blue_est == None and min_max_var=="max":
                    return red_est

                return red_est - blue_est
            elif self.color == "B":
                if blue_est == None and min_max_var=="max":
                    return -inf
                if blue_est == None and min_max_var=="min":
                    return inf
                if red_est == None and min_max_var=="min":
                    return blue_est
                if red_est == None and min_max_var=="max":
                    return blue_est
                return blue_est - red_est

    def __str__(self):
        string = ""
        for elem in self.matrix:
            string += str(elem) + "\n"
        return string

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

def print_title_on_display(content, display):
    text = FONT.render(content, True, (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.center = (DISPLAY_X//2, DISPLAY_Y//12)
    display.blit(text, text_rect)

def display_question(question, answers, display):
    display.fill(COLOR)

    print_title_on_display(question, display)

    X = len(answers)
    Y = len(answers[0])
    display_x = DISPLAY_X
    display_y = DISPLAY_Y
    display_y-= GAME_H_OFFSET

    for i in range(X):
        for j in range(Y):
            rect = pygame.Rect(
                int(display_x / X * i) + 3,
                int(display_y / Y * j) + GAME_H_OFFSET + 3,
                int(display_x / X - 6),
                int(display_y / Y - 6)
            )
            pygame.draw.rect(display, (100, 100, 100), rect, width=4, border_radius=6)

            center_x = int(display_x / X * i + (display_x / X / 2))
            center_y = GAME_H_OFFSET + int(display_y / Y * j + (display_y / Y / 2))
            text = FONT.render(answers[i][j], True, (20, 20, 20))
            text_rect = text.get_rect()
            text_rect.center = (center_x, center_y)
            display.blit(text, text_rect)

    pygame.display.flip()

    while True:
        # Loop through the events of the game.
        for event in pygame.event.get():
            # Quit.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Something was pressed.
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if a move was made, and if yes acknowledge it.
                pos = (pos[0], pos[1] - GAME_H_OFFSET)

                choice = (int(pos[0] / (display_x / X)), int(pos[1] / (display_y / Y)))
                return choice[1]


def main():
    global DISPLAY_X, DISPLAY_Y, player_1, player_2, \
        algorithm_1, algorithm_2, difficulty_1, difficulty_2, estimation_1, estimation_2, \
        color_1, color_2
    pygame.init()
    pygame.display.set_caption('Stan Bianca-Mihaela - Hex game')
    screen = pygame.display.set_mode(size=(DISPLAY_X, DISPLAY_Y))

    players = [["Human", "PC"]]                                     # choose type of first player
    player_1 = display_question("Player 1", players, screen)
    print(player_1)

    if player_1 != 0:                                               # if the first player is the pc
        algorithms = [["Min Max", "Alpha Betha"]]                   # we choose the algorithm
        algorithm_1 = display_question("Algorithm to use", algorithms, screen)

        estimations = [["Estimation 1", "Estimation 2"]]            # the estimation
        estimation_1 = display_question("Estimation to use", estimations, screen)
        print(estimation_1)
        screen.fill(COLOR)

        difficulty = [["Easy", "Medium", "Hard"]]                   # and the difficulty
        difficulty_1 = display_question("Difficulty", difficulty, screen)
        print(difficulty_1)
    else:                                                           # if the first player is human we only chose the color
        colors = [["red", "blue"]]
        color_1 = display_question("Clor to use", colors, screen)
        color_2 = 1-color_1

    player_2 = display_question("Player 2", players, screen)        # same for the second player
    print(player_2)

    if player_2 != 0:
        algorithms = [["Min Max", "Alpha Betha"]]
        algorithm_2 = display_question("Algorithm to use", algorithms, screen)

        estimations = [["Estimation 1", "Estimation 2"]]
        estimation_2 = display_question("Estimation to use", estimations, screen)
        print(estimation_2)
        screen.fill(COLOR)

        difficulty = [["Easy", "Medium", "Hard"]]
        difficulty_2 = display_question("Difficulty", difficulty, screen)
        print(difficulty_2)
    elif player_1 == 1:
        colors = [["red", "blue"]]
        color_2 = display_question("Algorithm to use", colors, screen)
        color_1 = 1-color_2

    print(f"color 1 : {color_1}, color 2 {color_2}")
    players = [Player(player_1, color_1, algorithm_1, estimation_1, difficulty_1),
               Player(player_2, color_2, algorithm_2, estimation_2, difficulty_2)]
    print(players[0].color)
    print(players[1].color)

    if player_1 == 1 and player_2 == 0:                     # if player 1 is the pc and player 2 is human, pc plays as max
        players[0].min_max = "max"
    elif player_1 == 0 and player_2 == 1:
        players[1].min_max = "max"
    elif player_1 == 1 and player_2 == 1:                   # if the match is pc vs pc the first one plays as max
        players[0].min_max = "max"
        players[1].min_max = "min"
        players[0].color = 'R'
        players[1].color = 'B'

    print(f"{algorithm_1, algorithm_2} {estimation_1, estimation_2} {difficulty_1, difficulty_2}")

    game = Game(screen, players, 0)
    screen.fill(COLOR)
    game.draw()
    game.last_switch = time.time()
    start_time = time.time()
    ok = True
    while True:
        if ok==True:
            screen.fill(COLOR)
            print_title_on_display(f"Player {game.player_index}'s turn.", game.display)
            game.draw()
            pygame.display.flip()
            ok=False
        valid = game.players[game.player_index].move(game)                      # we make the current player move
        if valid == True:
            ok=True
            game.draw()
            game.print_in_console()
            pygame.display.flip()
        if is_final(game.matrix, "R"):                                  # we check for final states and print the winner
            time.sleep(2)
            screen.fill(COLOR)
            print_title_on_display(f"R won", game.display)
            print("\n\nR won")
            pygame.display.flip()
            time.sleep(5)
            break
        elif is_final(game.matrix, "B"):
            time.sleep(2)
            screen.fill(COLOR)
            print_title_on_display("B won", game.display)
            print("\n\nB won")
            pygame.display.flip()
            time.sleep(5)
            break
    stop_time = time.time()
    game.play_time = stop_time-start_time

    print("For the first player: ")
    players[0].print_statistics()
    print("For the second player: ")
    players[1].print_statistics()
    game.print_game_statistics()


if __name__ == "__main__":

    main()