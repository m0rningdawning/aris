import os, art
from game_interface import draw_interface

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game():
    draw_interface()
    pass

def update_game_state(input):
    if input == "q":
        print("Quitting game...")
        exit()
    pass

def game_over_condition():
    pass

def main():
    game_running = True 
    while game_running:
        clear_terminal()
        draw_game()
        user_input = input("Press \"q\" to quit the game: ")

        update_game_state(user_input)

        if game_over_condition():
            game_running = False

    print("Game over! You won/lost!")

if __name__ == "__main__":
    main()
    