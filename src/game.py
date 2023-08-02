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


def choose_tetromino():
    return random.choice(TETROMINOES)


def draw_tetromino(screen, tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                screen.print_at('[]', x + col * 2, y + row)


def check_collision(board, tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                if y + row >= len(board) or x + col * 2 >= len(board[0]) or x + col * 2 < 0:
                    return True
                if board[y + row][x + col * 2] != 0:
                    return True
    return False


def update_board(board, tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                board[y + row][x + col * 2] = 1


def remove_lines(board):
    lines_to_remove = [i for i, row in enumerate(
        board) if all(cell != 0 for cell in row)]
    for line in reversed(lines_to_remove):
        del board[line]
        board.insert(0, [0 for _ in range(len(board[0]))])


def display_game(screen):
    current_platform = platform.system()

    screen.print_at("ASCII Tetris", 0, 0)

    if current_platform == "Windows":
        screen.print_at("(Windows)", 0, 1)
    else:
        screen.print_at("(Unix)", 0, 1)

    screen.refresh()

    board_height = 20
    board_width = 10
    board = [[0 for _ in range(board_width * 2)] for _ in range(board_height)]

    current_tetromino = choose_tetromino()
    tetromino_x = board_width // 2
    tetromino_y = 0

    score = 0

    while True:
        key = screen.get_key()

        if key == Screen.KEY_LEFT:
            if not check_collision(board, current_tetromino, tetromino_x - 2, tetromino_y):
                tetromino_x -= 2

        elif key == Screen.KEY_RIGHT:
            if not check_collision(board, current_tetromino, tetromino_x + 2, tetromino_y):
                tetromino_x += 2

        elif key == Screen.KEY_UP:
            rotated_tetromino = list(zip(*reversed(current_tetromino)))
            if not check_collision(board, rotated_tetromino, tetromino_x, tetromino_y):
                current_tetromino = rotated_tetromino

        elif key == Screen.KEY_DOWN:
            if not check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
                tetromino_y += 1

        elif key == Screen.KEY_ESCAPE:
            break

        if not check_collision(board, current_tetromino, tetromino_x, tetromino_y + 1):
            tetromino_y += 1
        else:
            update_board(board, current_tetromino, tetromino_x, tetromino_y)
            remove_lines(board)
            tetromino_x = board_width // 2
            tetromino_y = 0
            current_tetromino = choose_tetromino()
            if check_collision(board, current_tetromino, tetromino_x, tetromino_y):
                break

        screen.clear()

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

        draw_tetromino(screen, current_tetromino, tetromino_x, tetromino_y + 1)

        screen.print_at(f"Score: {score}", 0, board_height + 2)

        screen.refresh()

        time.sleep(0.25)

    screen.print_at("GAME OVER", board_width // 2 + 1, board_height // 2 + 1)
    screen.refresh()
    time.sleep(2)


def main():
    Screen.wrapper(display_game, catch_interrupt=True)


if __name__ == "__main__":
    main()
