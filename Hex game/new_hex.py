import time
from State import State
from Player import Player
from Game import Game
import sys
import pygame
from constants import CELL_DIMENSION
from constants import LIN
from constants import COL
from constants import FONT
from constants import DISPLAY_X
from constants import DISPLAY_Y
from constants import CELL_DIMENSION
from constants import GAME_H_OFFSET
from constants import player_1, player_2, estimation_1, estimation_2
from constants import algorithm_2, algorithm_1, difficulty_2, difficulty_1
from constants import color_2, color_1, COLOR
from helpers import DFS
from algorithms import is_final
from helpers import max_path

def print_title_on_display(content, display):
    text = FONT.render(content, True, (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.center = (DISPLAY_X//2, DISPLAY_Y//12)
    display.blit(text, text_rect)

def display_question(question, answers, display):
    """
    Display a questions with multiple answer options on the display.
    """
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

def valid_choice(current_state, cell_x, cell_y):
    return cell_x < LIN and \
           cell_y < COL and \
           current_state.tabla_joc.matr[cell_x][cell_y] == "#"

def switch_players(game):
    if game.player_index==0:
        game.player_index = 1
        return
    game.player_index=0


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