import random
import time
import platform
from asciimatics.screen import Screen


# Global variables

board = None
board_width = 10
board_height = 20
previous_tetromino = None
current_tetromino = None
tetromino_x = None
tetromino_y = None
score = None
collision_time = None
current_state = None
is_paused = False


TETROMINOES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]


class GameState:
    PLAYING = 0
    GAME_OVER = 1


def choose_tetromino(prevoius_tetromino):
    choice = random.choice(TETROMINOES)
    while (choice == prevoius_tetromino):
        choice = random.choice(TETROMINOES)
    return choice


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


def update_board(board, tetromino, x: int, y: int):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                board[int(y) + row][x + col * 2] = 1


def draw_board(screen, board, board_width, board_height):
    for row in range(board_height + 2):
        screen.print_at('!', 0, row)
        screen.print_at('!', board_width * 2 + 1, row)
        for col in range(board_width * 2 + 2):
            screen.print_at('=', col, 0)
            screen.print_at('=', col, board_height + 1)

        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    if col % 2:
                        screen.print_at('.', col + 1, row + 1)
                    else:
                        screen.print_at(' ', col + 1, row + 1)
                else:
                    screen.print_at('[]', col, row + 1)


def check_lines_and_score(board, score):
    amount = 0
    lines = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            amount += board[row][col]
            if amount == 10:
                remove_line(board, row)
                lines += 1
        amount = 0

    if lines != 0:
        score += 100 * lines

    return score


def remove_line(board, targ_row):
    while targ_row != 0:
        board[targ_row] = board[targ_row - 1][:]
        targ_row -= 1


# def pause_game():

def restart_game():
    global board
    global previous_tetromino
    global current_tetromino
    global tetromino_x
    global tetromino_y
    global score
    global collision_time
    global current_state
    global is_paused

    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]
    previous_tetromino = None
    current_tetromino = choose_tetromino(previous_tetromino)
    tetromino_x = board_width // 2 + 2
    tetromino_y = 0
    score = 0
    collision_time = None
    is_paused = False
    current_state = GameState.PLAYING


def display_game(screen):
    global board
    global previous_tetromino
    global current_tetromino
    global tetromino_x
    global tetromino_y
    global score
    global collision_time
    global current_state
    global is_paused

    current_platform = platform.system()

    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]

    fps = 60
    frametime = 1000 // fps
    previous_time = int(time.time() * 1000)
    total_time = 0

    current_tetromino = choose_tetromino(previous_tetromino)
    tetromino_x = board_width // 2 + 2
    tetromino_y = 0

    score = 0

    screen.print_at("ASCII Tetris", 0, 0)

    if current_platform == "Windows":
        screen.print_at("(Windows)", 0, 1)
    else:
        screen.print_at("(Unix)", 0, 1)

    screen.refresh()

    current_state = GameState.PLAYING

    while current_state == GameState.PLAYING:
        current_time = int(time.time() * 1000)
        elapsed_time = current_time - previous_time
        previous_time = current_time
        total_time += elapsed_time

        while total_time >= frametime:
            current_tetromino_speed = 0.025
            key = screen.get_key()
            if not is_paused:
                if key == Screen.KEY_LEFT:
                    if not check_collision(board, current_tetromino, tetromino_x - 2, tetromino_y):
                        tetromino_x -= 2

                elif key == Screen.KEY_RIGHT:
                    if not check_collision(board, current_tetromino, tetromino_x + 2, tetromino_y):
                        tetromino_x += 2

                elif key == Screen.KEY_UP:
                    rotated_tetromino = list(zip(*reversed(current_tetromino)))
                    if not check_collision(board, rotated_tetromino, tetromino_x, int(tetromino_y)):
                        current_tetromino = rotated_tetromino

                elif key == Screen.KEY_DOWN:
                    if not check_collision(board, current_tetromino, tetromino_x, int(tetromino_y) + 1):
                        tetromino_y += 1

            if key == ord('R') or key == ord('r'):
                restart_game()

            elif key == ord(' '):
                is_paused = not is_paused
                continue

            elif key == Screen.KEY_ESCAPE:
                current_state = GameState.GAME_OVER
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
                        if key == Screen.KEY_LEFT:
                            if not check_collision(board, current_tetromino, tetromino_x - 2, tetromino_y):
                                tetromino_x -= 2

                        elif key == Screen.KEY_RIGHT:
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
                        current_tetromino = choose_tetromino(
                            previous_tetromino)
                        previous_tetromino = current_tetromino
                        collision_time = None

                        if check_collision(board, current_tetromino, tetromino_x, tetromino_y):
                            if check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                                current_state = GameState.GAME_OVER
                                break

                score = check_lines_and_score(board, score)
                screen.refresh()
                draw_board(screen, board, board_width, board_height)
                draw_tetromino(screen, current_tetromino,
                               tetromino_x, tetromino_y + 1)

            else:
                screen.print_at("GAME PAUSED", board_width //
                                2, board_height // 2 + 1)

            total_time -= frametime
            screen.print_at(f"Score: {score}", 0, board_height + 2)

            screen.refresh()

    screen.clear()
    screen.print_at("GAME OVER", board_width // 2 + 1, board_height // 2)
    screen.print_at("Your Score:", board_width // 2, board_height // 2 + 1)
    screen.print_at(f"{score}", board_width, board_height // 2 + 2)
    screen.refresh()
    time.sleep(2)


def main():
    Screen.wrapper(display_game, catch_interrupt=True)


if __name__ == "__main__":
    main()
