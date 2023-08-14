from asciimatics.screen import Screen


def draw_next_section(screen, tetromino, board_width, score, lines):
    screen.print_at('  ________________ ', board_width * 3 - 2, 0)
    screen.print_at(' /! +++ Next +++ !\ ', board_width * 3 - 2, 1)
    screen.print_at('==================== ', board_width * 3 - 2, 2)
    screen.print_at('! . . . . . . . . .! ', board_width * 3 - 2, 3)
    screen.print_at('! . . . . . . . . .! ', board_width * 3 - 2, 4)
    screen.print_at('! . . . . . . . . .! ', board_width * 3 - 2, 5)
    screen.print_at('! . . . . . . . . .! ', board_width * 3 - 2, 6)
    screen.print_at('!==================! ', board_width * 3 - 2, 7)
    screen.print_at('!                  ! ', board_width * 3 - 2, 8)
    screen.print_at('!                  ! ', board_width * 3 - 2, 9)
    screen.print_at('==================== ', board_width * 3 - 2, 10)
    screen.print_at(f"Score: {score}", board_width * 3, 8)
    screen.print_at(f"Lines: {lines}", board_width * 3, 9)
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                screen.print_at('[]', board_width * 3 + 5 + col * 2, row + 4)


def draw_help_section(screen, board_width):
    screen.print_at('  ________________ ', board_width * 3 - 2, 11)
    screen.print_at(' /! +++ Help +++ !\ ', board_width * 3 - 2, 12)
    screen.print_at('==================== ', board_width * 3 - 2, 13)
    screen.print_at('! ↑, w, k - Rotate ! ', board_width * 3 - 2, 14)
    screen.print_at('! ←, a, h - Left   ! ', board_width * 3 - 2, 15)
    screen.print_at('! →, d, l - Right  ! ', board_width * 3 - 2, 16)
    screen.print_at('! ↓, s, j - Down   ! ', board_width * 3 - 2, 17)
    screen.print_at('! Space - Drop     ! ', board_width * 3 - 2, 18)
    screen.print_at('! g - Toggle Ghost ! ', board_width * 3 - 2, 19)
    screen.print_at('! p - Pause        ! ', board_width * 3 - 2, 20)
    screen.print_at('! r - Restart      ! ', board_width * 3 - 2, 21)
    screen.print_at('! q - Quit         ! ', board_width * 3 - 2, 22)
    screen.print_at('==================== ', board_width * 3 - 2, 23)


def draw_end_screen(screen, board_width, score, lines):
    screen.print_at('========================== ', board_width + 1, 7)
    screen.print_at('!       GAME OVER        ! ', board_width + 1, 8)
    screen.print_at('!------------------------! ', board_width + 1, 9)
    screen.print_at('! Your Score:            ! ', board_width + 1, 10)
    screen.print_at('!------------------------! ', board_width + 1, 11)
    screen.print_at('! Cleared Lines:         ! ', board_width + 1, 12)
    screen.print_at('!------------------------! ', board_width + 1, 13)
    screen.print_at('!      r - Restart       ! ', board_width + 1, 14)
    screen.print_at('!       q - Quit         ! ', board_width + 1, 15)
    screen.print_at('==========================', board_width + 1, 16)
    screen.print_at(f"{score}", board_width * 3 - 5, 10)
    screen.print_at(f"{lines}", board_width * 3 - 2, 12)
