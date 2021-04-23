import copy
import sys
import time
from math import inf

import pygame

CELL_DIMENSION = 40
LIN = 11
COL = 11
DISPLAY_X = int(COL* CELL_DIMENSION +CELL_DIMENSION*0.5*(LIN-1)+1)
DISPLAY_Y = CELL_DIMENSION*LIN
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 32)
GAME_H_OFFSET = 50

class State:
    def __init__(self, col, lin, display, input_file = None):
        self.lin= lin
        self.col=col
        self.matrix = [["#" for i in range(lin)] for j in range(col)]
        self.display = display

        if input_file!=None:
            f = open(input_file)
            input = f.read().split("\n")
            matrix = []
            for line in input:
                matrix.append([ x for x in line.split(" ")])
            self.matrix = matrix

    def show(self):
        '''
            Displays the state in the console.
        '''
        for i in range(self.lin):
            for j in range(self.lin):
                    print(self.matrix[i][j], end=" ")
            print("\n" + str(" " * i), end="")

    def draw(self):
        global CELL_DIMENSION
        for i in range(self.lin):
            for j in range(self.col):
                color = None
                if self.matrix[i][j] == "a":
                    color = (51, 204, 255)
                elif self.matrix[i][j] == "b":
                    color = (255, 80, 80)
                else:
                    color = (255, 255, 255)

                # print("here", self.display)
                pygame.draw.rect(self.display, color,
                                 pygame.Rect(j * CELL_DIMENSION + 1 + CELL_DIMENSION* 0.5 *i, i * CELL_DIMENSION + 1, CELL_DIMENSION,
                                             CELL_DIMENSION))
                pygame.draw.rect(self.display, (0, 0, 0),
                                 pygame.Rect(j * CELL_DIMENSION + 1 + CELL_DIMENSION* 0.5 *i, i * CELL_DIMENSION + 1, CELL_DIMENSION,
                                             CELL_DIMENSION), 1)
                pygame.display.flip()


    def create_copy(self):
        '''
            Returns a deep copy of the state. Used for modifying the copy
            without changing the original object.
        '''
        s = State(self.col, self.lin, None)
        s.taken = copy.deepcopy(self.matrix)
        s.display= self.display
        return s

    def is_final(self):
        for i in range(self.lin):
            if self.matrix[i][0] != "#":
                viz = [[False for i in range(self.lin)] for j in range(self.col)]
                val = DFS(self, i, 0, None, self.col - 1, viz)
                if val != None:
                    return val
            elif self.matrix[0][i] != "#":
                viz = [[False for i in range(self.lin)] for j in range(self.col)]
                val = DFS(self, 0, i, self.lin - 1 , None, viz)
                if val != None:
                    return val
        return 0


def DFS(state, x, y, final_x, final_y, viz):
    if viz[x][y]==False:
        viz[x][y]=True
        if x==final_x or y==final_y:
            return state.matrix[x][y]        # returns the player that won

        current = state.matrix[x][y]
        if x-1>=0 and viz[x-1][y]==False and state.matrix[x-1][y]==current:
            return DFS(state, x-1, y, final_x, final_y, viz)
        elif x-1>=0 and y+1<state.col and viz[x-1][y+1]==False and state.matrix[x-1][y+1]==current:
            return DFS(state, x-1, y+1, final_x, final_y, viz)
        elif y-1>=0 and viz[x][y-1]==False and state.matrix[x][y-1]==current:
            return DFS(state, x, y-1, final_x, final_y, viz)
        elif y+1<state.col and viz[x][y+1]==False and state.matrix[x][y+1]==current:
            return DFS(state, x, y+1, final_x, final_y, viz)
        elif x+1<state.lin and y-1>=0 and viz[x+1][y-1]==False and state.matrix[x+1][y-1]==current:
            return DFS(state, x, y-1, final_x, final_y, viz)
        elif x+1<state.lin and viz[x+1][y]==False and state.matrix[x+1][y]==current:
            return DFS(state, x+1, y, final_x, final_y, viz)


def generate_successors(state, player):
    successors = []
    for i in range(state.lin):
        for j in range(state.col):
            if state.matrix[i][j]=="#":
                new_state = state.create_copy()
                new_state[i][j]= player
                successors.append(new_state)

    return successors

def estimate_state(state, estimation_type):
    lee_matrix = [[+inf for i in range(state.lin)] for j in range(state.col)]
    if estimation_type=="estimation 2":
        for i in range(state.lin):
            for j in range (state.col):
                if


def min(state, player):
    print(f"Player {player} minimizes")



def valid_choice(current_state, cell_x, cell_y):
    return cell_x < current_state.lin and \
           cell_y < current_state.col and \
           current_state.matrix[cell_x][cell_y] == "#"

def switch(current_symbol):
    if current_symbol=="a":
        return "b"
    return "a"

def game_loop(current_state, players, algorithm_choices, estimation_choices, difficulty_choices):
    current_symbol = "a"
    current_player = 0
    # algorithms = [min_max, alpha_betha]
    estimations = ["estimation 1", "estimation 2"]
    difficulties = [1, 3, 5]

    while True:
        current_state.draw()

        final = current_state.is_final()
        if final != 0:
            print(f"A castigat jucatorul {final}")
            pygame.quit()
            sys.exit(0)

        # if players[current_player]==1:
        #     algorithms[algorithm_choices[current_player]](estimations[estimation_choices[current_player]],
        #                                                   difficulties[difficulty_choices[current_player]])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Calculating the cell the player clicked on based on the position of the mouse.
                cell_x = pos[1] // CELL_DIMENSION
                cell_y = (pos[0] // (CELL_DIMENSION // 2) - cell_x) // 2
                print(f"Player attempted a move {cell_x} {cell_y}.")

                if valid_choice(current_state, cell_x, cell_y):
                    current_state.matrix[cell_x][cell_y] = current_symbol
                    current_symbol = switch(current_symbol)


def print_title_on_display(content, display):
    '''
        Prints a given title on the display.
    '''
    text = FONT.render(content, True, (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.center = (DISPLAY_X//2, DISPLAY_Y//12)
    display.blit(text, text_rect)

def display_question(question, answers, display):
    display.fill((230, 255, 215))

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
    global DISPLAY_X, DISPLAY_Y
    pygame.init()
    pygame.display.set_caption('Hex game')
    screen = pygame.display.set_mode(size=(DISPLAY_X, DISPLAY_Y))

    player_1 = None
    player_2 = None
    estimation_1 = None
    estimation_2 = None
    algorithm_1 = None
    algorithm_2 = None
    difficulty_1 = None
    difficulty_2 = None

    players = [["Human", "PC"]]
    player_1 = display_question("Player 1", players, screen)
    print(player_1)

    if player_1!= 0:
        algorithms = [["Min Max", "Alpha Betha"]]
        algorithm_1 = display_question("Algorithm to use", algorithms, screen)

        estimations = [["Estimation 1", "Estimation 2"]]
        estimation_1 = display_question("Estimation to use", estimations, screen)
        print(estimation_1)
        screen.fill((230, 255, 215))

        difficulty = [["Easy", "Medium", "Hard"]]
        difficulty_1 = display_question("Difficulty", difficulty, screen)
        print(difficulty_1)

    player_2 = display_question("Player 2", players, screen)
    print(player_2)

    if player_2 != 0:
        algorithms = [["Min Max", "Alpha Betha"]]
        algorithm_2 = display_question("Algorithm to use", algorithms, screen)

        estimations = [["Estimation 1", "Estimation 2"]]
        estimation_2 = display_question("Estimation to use", estimations, screen)
        print(estimation_2)
        screen.fill((230, 255, 215))

        difficulty = [["Easy", "Medium", "Hard"]]
        difficulty_2 = display_question("Difficulty", difficulty, screen)
        print(difficulty_2)

    players = [player_1, player_2]
    algorithms = [algorithm_1, algorithm_2]
    estimations = [estimation_1, estimation_2]
    difficulties = [difficulty_1, difficulty_2]
    current_state = State(11, 11, screen, "input.txt")
    game_loop(current_state, players, algorithms, estimations, difficulties)

if __name__ == '__main__':
    main()