def draw_interface():
    screen =   "  __________________         ________________ \n"
    screen +=  " /! +++ Tetris +++ !\       /! +++ Next +++ !\ \n"
    screen +=  "/====================\     /==================\ \n"
    screen +=  "! . . . .[] . . . . .!     ! . . . . . . . . .! \n"
    screen +=  "! . . . .[] . . . . .!     ! . . .[][] . . . .! \n"
    screen +=  "! . . . .[] . . . . .!     ! . . . .[][] . . .! \n"
    screen +=  "! . . . .[] . . . . .!     ! . . . . . . . . .! \n"
    screen +=  "! . . . . . . . . . .!     !==================! \n"
    screen +=  "! . . . . . . . . . .!     ! Score: 9999999   ! \n"
    screen +=  "! . . . . . . . . . .!     ! Lines: 12        ! \n"
    screen +=  "! . . . . . . . . . .!     !==================! \n"
    screen +=  "! . . . . . . . . . .!       ________________ \n"
    screen +=  "! . . . . . . . . . .!      /! +++ Help +++ !\ \n"
    screen +=  "! . . . . . . . . . .!     /==================\ \n"
    screen +=  "! . . . . . . . . . .!     ! ↑, w, k - Rotate ! \n"
    screen +=  "! . . . . . . . . . .!     ! ←, a, h - Left   ! \n"
    screen +=  "! . . . . . . . . . .!     ! →, d, l - Right  ! \n"
    screen +=  "! . . . . . . . . . .!     ! ↓, s, j - Down   ! \n"
    screen +=  "! . . . . @ . . . . .!     ! Space - Drop     ! \n"
    screen +=  "! .[] . . @ . . . . .!     ! g - Toggle Ghost ! \n"
    screen +=  "![][] . . @ . . . . .!     ! p - Pause        ! \n"
    screen +=  "![][] . . @[][] . . .!     ! r - Restart      ! \n"
    screen +=  "![][][] .[][][][][][]!     ! q - Quit         ! \n"
    screen +=  "!====================!     !==================! \n"
    print(screen)
    print(screen[112])