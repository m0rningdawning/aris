import random
import time
import platform
from asciimatics.screen import Screen


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
    PAUSED = 2


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


def display_game(screen):
    current_platform = platform.system()

    board_height = 20
    board_width = 10
    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]

    fps = 60
    frametime = 1000 // fps
    previous_time = int(time.time() * 1000)
    total_time = 0

    previous_tetromino = None
    current_tetromino = choose_tetromino(previous_tetromino)
    tetromino_x = board_width // 2
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

            elif key == Screen.KEY_ESCAPE:
                current_state = GameState.GAME_OVER
                break

            if not check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                tetromino_y += current_tetromino_speed
            else:
                update_board(board, current_tetromino,
                             tetromino_x, tetromino_y)
                tetromino_x = board_width // 2
                tetromino_y = 0
                current_tetromino = choose_tetromino(previous_tetromino)
                previous_tetromino = current_tetromino
                if check_collision(board, current_tetromino, tetromino_x, tetromino_y):
                    if check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                        current_state = GameState.GAME_OVER
                        break

            total_time -= frametime

        score = check_lines_and_score(board, score)

        screen.refresh()

        draw_board(screen, board, board_width, board_height)

        draw_tetromino(screen, current_tetromino, tetromino_x, tetromino_y + 1)

        screen.print_at(f"Score: {score}", 0, board_height + 2)

        screen.refresh()

    screen.print_at("GAME OVER", board_width // 2 + 1, board_height // 2 + 1)
    screen.refresh()
    time.sleep(2)


def main():
    Screen.wrapper(display_game, catch_interrupt=True)


if __name__ == "__main__":
    main()
