import random
import time
import threading
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
tetromino_speed = None

score = 0
lines = 0
level = 1
levelup = level * 5

start_time = None
formatted_time = None
collision_time = None

current_state = None
is_paused = False
is_finished = False
is_cleared = False
is_dropped = False
is_ghost = False


class GameState:
    PLAYING = 0
    GAME_OVER = 1


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


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


def draw_ghost(screen, tetromino, x: int, y: int):
    ghost_drop_distance = drop_tetromino(board, tetromino, x, y)
    ghost_y = int(y) + ghost_drop_distance
    if ghost_y < board_height:
        for row in range(len(tetromino)):
            for col in range(len(tetromino[0])):
                if tetromino[row][col]:
                    screen.print_at('@@', x + col * 2, ghost_y + row + 3)


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
    global level
    global levelup
    global tetromino_speed
    current_lines = 0
    amount_of_ones = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            amount_of_ones += board[row][col]
            if amount_of_ones == 10:
                remove_line(board, row)
                current_lines += 1
        amount_of_ones = 0

    if current_lines == 1:
        score += 100 * level
    elif current_lines == 2:
        score += 300 * level
    elif current_lines == 3:
        score += 500 * level
    elif current_lines == 4:
        score += 800 * level
    lines += current_lines

    if lines >= levelup:
        level += 1
        levelup += level * 5
        tetromino_speed = 0.02 * level * 0.75


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
    global tetromino_speed
    global score
    global lines
    global level
    global levelup
    global is_ghost
    global is_dropped
    global start_time
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
    tetromino_speed = 0.02
    score = 0
    lines = 0
    level = 1
    levelup = level * 5
    start_time = time.time()
    collision_time = None
    is_paused = False
    is_finished = False
    is_dropped = False
    is_ghost = False
    current_state = GameState.PLAYING


def display_game(screen):
    global board
    global current_tetromino
    global current_tetromino_type
    global next_tetromino
    global next_tetromino_type
    global tetromino_x
    global tetromino_y
    global tetromino_speed
    global score
    global lines
    global start_time
    global formatted_time
    global collision_time
    global current_state
    global is_paused
    global is_finished
    global is_cleared
    global is_dropped
    global is_ghost
    global start_time

    if start_time is None:
        start_time = time.time()

    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]

    fps = 60
    frametime = 1000 // fps
    previous_time = int(time.time() * 1000)
    total_time = 0
    elapsed_seconds = 0

    current_tetromino, current_tetromino_type = choose_tetromino(None)
    next_tetromino, next_tetromino_type = choose_tetromino(
        current_tetromino_type)
    tetromino_x = board_width // 2 + 2
    tetromino_y = 0

    tetromino_speed = 0.02

    collided = False

    current_state = GameState.PLAYING

    while current_state == GameState.PLAYING:
        current_time = int(time.time() * 1000)
        elapsed_time = current_time - previous_time
        previous_time = current_time
        total_time += elapsed_time

        while total_time >= frametime:
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
                        score += 1

                elif key == ord(' '):
                    is_dropped = True
                    drop_distance = drop_tetromino(
                        board, current_tetromino, tetromino_x, tetromino_y)
                    tetromino_y += drop_distance
                    score += drop_distance * 2

                elif key == ord('G') or key == ord('g'):
                    is_ghost = not is_ghost

            if not is_finished:
                if key == ord('R') or key == ord('r'):
                    restart_game()

                elif key == ord('P') or key == ord('p'):
                    is_paused = not is_paused
                    if is_paused:
                        elapsed_seconds = int(time.time() - start_time)
                    else:
                        start_time = time.time() - elapsed_seconds
                    continue

                elif key == Screen.KEY_ESCAPE or key == ord('Q') or key == ord('q'):
                    is_finished = True
                    is_paused = True
                    break

            if not is_paused:
                if not check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                    tetromino_y += tetromino_speed
                else:
                    collided = True
                    if collision_time is None:
                        collision_time = time.time()

                    elapsed_time = time.time() - collision_time
                    if elapsed_time < 0.5 and not is_dropped:
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

                    elif elapsed_time == 0.5 and not is_dropped:
                        if check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                            collided = True
                        else:
                            collision_time = None
                            collided = False

                    elif is_dropped or collided:
                        update_board(board, current_tetromino,
                                     tetromino_x, tetromino_y)
                        tetromino_x = board_width // 2 + 2
                        tetromino_y = 0
                        current_tetromino = next_tetromino
                        current_tetromino_type = next_tetromino_type
                        next_tetromino, next_tetromino_type = choose_tetromino(
                            current_tetromino_type)
                        collision_time = None
                        is_dropped = False
                        collided = False

                        if check_collision(board, current_tetromino, tetromino_x, tetromino_y):
                            if check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                                is_finished = True
                                is_paused = True
                                break

                check_lines_and_score(board)
                screen.refresh()
                draw_board(screen, board, board_width, board_height)
                if is_ghost:
                    draw_ghost(screen, current_tetromino,
                               tetromino_x, tetromino_y)
                draw_tetromino(screen, current_tetromino,
                               tetromino_x, tetromino_y + 3)
                draw_next_section(screen, next_tetromino,
                                  board_width, score, lines, level, formatted_time)
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
                    draw_end_screen(screen, board_width, score,
                                    lines, level, formatted_time)
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

        if not is_paused:
            elapsed_seconds = int(time.time() - start_time)
        formatted_time = format_time(elapsed_seconds)
        screen.refresh()

    screen.clear()


def main():
    Screen.wrapper(display_game, catch_interrupt=True)


if __name__ == "__main__":
    main()
