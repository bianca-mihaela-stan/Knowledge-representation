import copy
from math import inf
from typing import List
from dijkstar import Graph, find_path
import pygame
import Game
from constants import LIN, COL
from helpers import DFS, convert_tuple_to_int, max_path
from constants import switch_color, switch_min_max

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
        # red_graph and blue_graph are graphs that are used to perform dijktra for estimation 2.
        self.red_graph = Graph(undirected=True)
        self.blue_graph = Graph(undirected=True)
        self.red_source = convert_tuple_to_int((0, -1))
        self.red_dest = convert_tuple_to_int((LIN, COL))
        self.blue_source = convert_tuple_to_int((0, -2))
        self.blue_dest = convert_tuple_to_int((LIN + 1, COL + 1))
        # If this is the root node for the algorithms we construct the graphs from the matrix.
        if parent == None:
            self.add_all_neighbours_red()
            self.add_all_neighbours_blue()
        else:
            self.create_red_graph_based_on_parent()
            self.create_blue_graph_based_on_parent()

    def create_red_graph_based_on_parent(self):
        """
        Creates red_graph for current state using the red_graph of its parent.
        """
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


        # Lastly, we add the source and destination nodes.
        self.red_graph.add_node(self.red_source)
        self.red_graph.add_node(self.red_dest)
        for i in range(COL):
            self.red_graph.add_edge(self.red_source, convert_tuple_to_int((0, i)), 1)
            self.red_graph.add_edge(convert_tuple_to_int((LIN - 1, i)), self.red_dest, 1)


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

        # Lastly, we add the source and destination nodes.
        self.blue_graph.add_node(self.blue_source)
        self.blue_graph.add_node(self.blue_dest)
        for i in range(LIN):
            self.blue_graph.add_edge(self.blue_source, convert_tuple_to_int((i, 0)), 1)
            self.blue_graph.add_edge(convert_tuple_to_int((i, COL - 1)), self.blue_dest, 1)

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



    def generate_moves(self):
        """
        Function to generate next moves from a State.
        For each # in the matrix we replace it with the current color.
        """
        for i in range (len(self.matrix)):
            for j in range (len(self.matrix[i])):
                if self.matrix[i][j] == "#":
                    new_matrix = [[x for x in y] for y in self.matrix]
                    new_matrix[i][j] = self.color
                    new_state = State(matrix=new_matrix, min_max_var=switch_min_max(self.min_max_var),
                                      depth=self.depth-1, estimation_name=self.estimation_name, color = switch_color(self.color))
                    self.moves.append(new_state)

    def estimate(self, estimation, min_max_var):
        """
        Estimates how good a state is.
        """
        # Depending on the type of estimation the user chose.
        if estimation == 0:
            # First estimations counts the longest path for each of the colors using Lee's algorithm.
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
            # The second estimations calculates the minimum number of nodes needed to get to target.
            try:
                red_est = find_path(self.red_graph, self.red_source, self.red_dest).total_cost
            except:
                red_est = None
            try:
                blue_est = find_path(self.blue_graph, self.blue_source, self.blue_dest).total_cost
            except:
                blue_est = None
            if self.color == "R":
                # If red_est is None it means there's no way for R to win.
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