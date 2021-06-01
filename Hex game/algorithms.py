import copy
import random
from math import inf

from State import State
from constants import LIN, COL
from helpers import DFS
from constants import LIN, COL
from constants import switch_color, switch_min_max

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

