from math import inf

from constants import LIN, COL


def DFS(matrix, x, y, final_x, final_y, viz):
    """
    A DFS to check if a matrix is a final state.
    """
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
    """
    Finds the length of the maximum path of color in matrix.
    """
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

# def dijkstra(matrix, color):
#
#     graph = Graph()
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             graph.add_node((i, j))
#
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#
#             if i >=1:
#                 graph.add_edge((i,j), (i-1, j))
#
#     # while len(queue)>0:
#     #     (i,j) = queue[0]
#     #     queue.pop(0)
#     #     if j-1>=0 and viz[i][j]+1<viz[i][j-1]:
#     #         viz[i][j-1]=viz[i][j]+1
#     #         queue.append(i, j-1)
#     #     if j+1 <= COL-1 and viz[i][j]+1<viz[i][j+1]:
#     #         viz[i][j+1]=viz[i][j]+1
#     #         queue.append(i, j+1)
#     #     if i-1 >= 0 and viz[i][j] + 1 < viz[i-1][j]:
#     #         viz[i-1][j] = viz[i][j] + 1
#     #         queue.append(i-1, j)
#     #     if i-1 >= 0 and j+1 <= COL-1 and viz[i][j]+1<viz[i-1][j+1]:
#     #         viz[i-1][j+1]=viz[i][j]+1
#     #         queue.append(i-1, j+1)
#     #     if i+1 <= LIN - 1 and j-1 >= 0 and viz[i][j]+1<viz[i+1][j-1]:
#     #         viz[i+1][j-1]=viz[i][j]+1
#     #         queue.append(i+1, j - 1)
#     #     if i+1 <= LIN - 1  and viz[i][j]+1<viz[i+1][j]:
#     #         viz[i+1][j]=viz[i][j]+1
#     #         queue.append(i+1, j)
