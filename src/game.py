import random
import time
import platform
from asciimatics.screen import Screen
from tetrominoes import TETROMINOES
from game_interface import draw_help_section, draw_next_section, draw_end_screen


# Global variables

board = None
board_width = 10
board_height = 20

current_tetromino = None
current_tetromino_type = None
next_tetromino = None
next_tetromino_type = None

tetromino_x = None
tetromino_y = None

score = 0
lines = 0

collision_time = None

current_state = None
is_paused = False
is_finished = False
is_cleared = False


class GameState:
    PLAYING = 0
    GAME_OVER = 1


def choose_tetromino(previous_tetromino):
    available_tetrominos = [tetromino_type for tetromino_type in TETROMINOES.keys(
    ) if tetromino_type != previous_tetromino]
    next_tetromino_type = random.choice(available_tetrominos)
    return TETROMINOES[next_tetromino_type][0], next_tetromino_type


def draw_tetromino(screen, tetromino, x: int, y: int):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                screen.print_at('[]', x + col * 2, int(y) + row)


def check_collision(board, tetromino, x: int, y: int):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                if y + row >= len(board) or x + col * 2 >= len(board[0]) or x + col * 2 < 0:
                    return True
                if board[int(y) + row][x + col * 2] != 0:
                    return True
    return False


def drop_tetromino(board, tetromino, x, y):
    drop_distance = 0
    while not check_collision(board, tetromino, x, y + drop_distance + 1):
        drop_distance += 1
    return drop_distance


def update_board(board, tetromino, x: int, y: int):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                board[int(y) + row][x + col * 2] = 1


def draw_board(screen, board, board_width, board_height):
    screen.print_at('  __________________', 0, 0)
    screen.print_at(' /! +++ Tetris +++ !\ ', 0, 1)
    for row in range(board_height + 2):
        screen.print_at('!', 0, row + 2)
        screen.print_at('!', board_width * 2 + 1, row + 2)
        for col in range(board_width * 2 + 2):
            screen.print_at('=', col, 2)
            screen.print_at('=', col, board_height + 3)

        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    if col % 2:
                        screen.print_at('.', col + 1, row + 3)
                    else:
                        screen.print_at(' ', col + 1, row + 3)
                else:
                    screen.print_at('[]', col, row + 3)


def check_lines_and_score(board):
    global score
    global lines
    current_lines = 0
    amount_of_ones = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            amount_of_ones += board[row][col]
            if amount_of_ones == 10:
                remove_line(board, row)
                current_lines += 1
        amount_of_ones = 0

    if current_lines != 0:
        score += 100 * current_lines
        lines += current_lines


def remove_line(board, targ_row):
    while targ_row != 0:
        board[targ_row] = board[targ_row - 1][:]
        targ_row -= 1


def restart_game():
    global board
    global current_tetromino
    global current_tetromino_type
    global next_tetromino
    global next_tetromino_type
    global tetromino_x
    global tetromino_y
    global score
    global lines
    global collision_time
    global current_state
    global is_paused
    global is_finished

    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]
    current_tetromino, current_tetromino_type = choose_tetromino(None)
    next_tetromino, next_tetromino_type = choose_tetromino(
        current_tetromino_type)
    tetromino_x = board_width // 2 + 2
    tetromino_y = 0
    score = 0
    lines = 0
    collision_time = None
    is_paused = False
    is_finished = False
    current_state = GameState.PLAYING


def display_game(screen):
    global board
    global current_tetromino
    global current_tetromino_type
    global next_tetromino
    global next_tetromino_type
    global tetromino_x
    global tetromino_y
    global score
    global lines
    global collision_time
    global current_state
    global is_paused
    global is_finished
    global is_cleared

    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]

    fps = 60
    frametime = 1000 // fps
    previous_time = int(time.time() * 1000)
    total_time = 0

    current_tetromino, current_tetromino_type = choose_tetromino(None)
    next_tetromino, next_tetromino_type = choose_tetromino(
        current_tetromino_type)
    tetromino_x = board_width // 2 + 2
    tetromino_y = 0

    current_state = GameState.PLAYING

    while current_state == GameState.PLAYING:
        current_time = int(time.time() * 1000)
        elapsed_time = current_time - previous_time
        previous_time = current_time
        total_time += elapsed_time

        while total_time >= frametime:
            current_tetromino_speed = 0.02
            key = screen.get_key()
            if not is_paused and not is_finished:
                if key == Screen.KEY_LEFT or key == ord('A') or key == ord('a') or key == ord('H') or key == ord('h'):
                    if not check_collision(board, current_tetromino, tetromino_x - 2, tetromino_y):
                        tetromino_x -= 2

                elif key == Screen.KEY_RIGHT or key == ord('D') or key == ord('d') or key == ord('L') or key == ord('l'):
                    if not check_collision(board, current_tetromino, tetromino_x + 2, tetromino_y):
                        tetromino_x += 2

                elif key == Screen.KEY_UP or key == ord('W') or key == ord('w') or key == ord('K') or key == ord('k'):
                    rotated_tetromino = list(zip(*reversed(current_tetromino)))
                    if not check_collision(board, rotated_tetromino, tetromino_x, int(tetromino_y)):
                        current_tetromino = rotated_tetromino

                elif key == Screen.KEY_DOWN or key == ord('S') or key == ord('s') or key == ord('J') or key == ord('j'):
                    if not check_collision(board, current_tetromino, tetromino_x, int(tetromino_y) + 1):
                        tetromino_y += 1

                elif key == ord(' '):
                    drop_distance = drop_tetromino(
                        board, current_tetromino, tetromino_x, tetromino_y)
                    tetromino_y += drop_distance

            if not is_finished:
                if key == ord('R') or key == ord('r'):
                    restart_game()

                elif key == ord('P') or key == ord('p'):
                    is_paused = not is_paused
                    continue

                elif key == Screen.KEY_ESCAPE or key == ord('Q') or key == ord('q'):
                    is_finished = True
                    is_paused = True
                    break

            if not is_paused:
                if not check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                    tetromino_y += current_tetromino_speed
                else:
                    if collision_time is None:
                        collision_time = time.time()

                    elapsed_time = time.time() - collision_time
                    if elapsed_time < 0.5:
                        key = screen.get_key()
                        if key == Screen.KEY_LEFT or key == ord('A') or key == ord('a') or key == ord('H') or key == ord('h'):
                            if not check_collision(board, current_tetromino, tetromino_x - 2, tetromino_y):
                                tetromino_x -= 2

                        elif key == Screen.KEY_RIGHT or key == ord('D') or key == ord('d') or key == ord('L') or key == ord('l'):
                            if not check_collision(board, current_tetromino, tetromino_x + 2, tetromino_y):
                                tetromino_x += 2

                        elif key == Screen.KEY_UP:
                            rotated_tetromino = list(
                                zip(*reversed(current_tetromino)))
                            if not check_collision(board, rotated_tetromino, tetromino_x, int(tetromino_y)):
                                current_tetromino = rotated_tetromino
                    else:
                        update_board(board, current_tetromino,
                                     tetromino_x, tetromino_y)
                        tetromino_x = board_width // 2 + 2
                        tetromino_y = 0
                        current_tetromino = next_tetromino
                        current_tetromino_type = next_tetromino_type
                        next_tetromino, next_tetromino_type = choose_tetromino(
                            current_tetromino_type)
                        collision_time = None

                        if check_collision(board, current_tetromino, tetromino_x, tetromino_y):
                            if check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                                is_finished = True
                                is_paused = True
                                break

                check_lines_and_score(board)
                screen.refresh()
                draw_board(screen, board, board_width, board_height)
                draw_tetromino(screen, current_tetromino,
                               tetromino_x, tetromino_y + 3)
                draw_next_section(screen, next_tetromino,
                                  board_width, score, lines)
                draw_help_section(screen, board_width)

            else:
                if not is_finished:
                    screen.print_at("GAME PAUSED", board_width //
                                    2, board_height // 2 + 2)
                    screen.refresh()
                if is_finished:
                    if not is_cleared:
                        screen.clear()
                        is_cleared = True
                    draw_end_screen(screen, board_width, score, lines)
                    screen.refresh()
                    if key == ord('R') or key == ord('r'):
                        screen.clear()
                        current_state = GameState.PLAYING
                        is_cleared = False
                        restart_game()
                    elif key == Screen.KEY_ESCAPE or key == ord('Q') or key == ord('q'):
                        is_finished = False
                        is_paused = False
                        current_state = GameState.GAME_OVER

            total_time -= frametime
            screen.refresh()

    screen.clear()


def main():
    Screen.wrapper(display_game, catch_interrupt=True)


if __name__ == "__main__":
    main()
