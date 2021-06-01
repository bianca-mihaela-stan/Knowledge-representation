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


