import copy
import sys
import time

import pygame

CELL_DIMENSION = 40
LIN = 11
COL = 11

class State:
    def __init__(self, col, lin, display, input_file = None):
        self.lin= lin
        self.col=col
        self.matrix = [[-1 for i in range(lin)] for j in range(col)]
        self.display = display

        if input_file!=None:
            f = open(input_file)
            input = f.read().split("\n")
            matrix = []
            for line in input:
                matrix.append([ int(x) for x in line.split(" ")])
            self.matrix = matrix

    def show(self):
        '''
            Displays the state in the console.
        '''
        for i in range(self.lin):
            for j in range(self.lin):
                if self.matrix[i][j] == -1:
                    print("# ", end="")
                else:
                    print(self.matrix[i][j], end=" ")
            print("\n" + str(" " * i), end="")

    def draw(self):
        global CELL_DIMENSION
        for i in range(self.lin):
            for j in range(self.col):
                color = None
                if self.matrix[i][j] == 1:
                    color = (51, 204, 255)
                elif self.matrix[i][j] == 2:
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
            if self.matrix[i][0] != -1:
                viz = [[False for i in range(self.lin)] for j in range(self.col)]
                val = DFS(self, i, 0, None, self.col - 1, viz)
                if val != None:
                    return val
            elif self.matrix[0][i] != -1:
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
        if state.matrix[x-1][y]==current and x-1>=0 and viz[x-1][y]==False:
            return DFS(state, x-1, y, final_x, final_y, viz)
        elif state.matrix[x-1][y+1]==current  and x-1>=0 and y+1<state.col and viz[x-1][y+1]==False:
            return DFS(state, x-1, y+1, final_x, final_y, viz)
        elif state.matrix[x][y-1]==current and y-1>=0 and viz[x][y-1]==False:
            return DFS(state, x, y-1, final_x, final_y, viz)
        elif state.matrix[x][y+1]==current and y+1<state.col and viz[x][y+1]==False:
            return DFS(state, x, y+1, final_x, final_y, viz)
        elif state.matrix[x+1][y-1]==current and x+1<state.lin and y-1>=0 and viz[x+1][y-1]==False:
            return DFS(state, x, y-1, final_x, final_y, viz)
        elif state.matrix[x+1][y]==current and x+1<state.lin and viz[x+1][y]==False:
            return DFS(state, x+1, y, final_x, final_y, viz)

pygame.init()
pygame.display.set_caption('Hex game')
screen = pygame.display.set_mode(size=(int(COL* CELL_DIMENSION +CELL_DIMENSION*0.5*(LIN-1)+1), CELL_DIMENSION*LIN))
current_state = State(11, 11, screen, "input.txt")
switch=1

while True :
    current_state.draw()

    final = current_state.is_final();
    if final!=0:
        print(f"A castigat jucatorul {final}")
        pygame.quit()
        sys.exit(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Calculating the cell the player clicked on based on the position of the mouse.
            cell_x = pos[1]//CELL_DIMENSION
            cell_y = (pos[0]//(CELL_DIMENSION // 2) - cell_x ) // 2
            print(f"Player attempted a move {cell_x} {cell_y}.")

            if cell_x<current_state.lin and cell_y<current_state.col and current_state.matrix[cell_x][cell_y]==-1:
                current_state.matrix[cell_x][cell_y]=switch
                switch=3-switch