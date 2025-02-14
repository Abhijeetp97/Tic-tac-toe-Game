import numpy as np
import itertools
import random
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_board(board):
    """
    Print the current state of the board with row and column indices.
    """
    size = len(board)
    print("  " + " ".join(map(str, range(size))))
    for i, row in enumerate(board):
        print(i, " ".join([Fore.RED + 'X' + Style.RESET_ALL if s == 'X' else Fore.BLUE + 'O' + Style.RESET_ALL if s == 'O' else s for s in row]))
    print()

def check_winner(board, player, size):
    """
    Check if the current player has won the game.
    Returns True if the player has won, otherwise False.
    """
    for row in board:
        if all([s == player for s in row]):
            return True
    for col in board.T:
        if all([s == player for s in col]):
            return True
    if all([board[i, i] == player for i in range(size)]):
        return True
    if all([board[i, size-1-i] == player for i in range(size)]):
        return True
    return False

def get_move(size):
    """
    Prompt the player to enter their move and validate the input.
    Returns the row and column indices of the move.
    """
    while True:
        move = input("Enter your move (row and column, e.g., 0 1): ").strip().split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit():
            row, col = int(move[0]), int(move[1])
            if 0 <= row < size and 0 <= col < size:
                return row, col
        print("Invalid move. Please try again.")

def ai_move(board):
    """
    Generate a random move for the AI.
    Returns the row and column indices of the move.
    """
    size = len(board)
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i, j] == ' ']
    return random.choice(empty_cells)

def play_game(board, size, players, ai=False):
    """
    Manage the gameplay, alternating between players, checking for a winner,
    and printing the board after each move.
    """
    print_board(board)
    for _ in range(size * size):
        current_player = next(players)
        print(f"Player {current_player}'s turn.")
        if ai and current_player == 'O':
            row, col = ai_move(board)
        else:
            row, col = get_move(size)
        while board[row, col] != ' ':
            print("This position is already taken. Please try again.")
            row, col = get_move(size)
        board[row, col] = current_player
        print_board(board)
        if check_winner(board, current_player, size):
            print(f"Player {current_player} wins!")
            return current_player
    print("It's a draw!")
    return None

def save_scores(scores, filename):
    """
    Save the scores to a JSON file.
    """
    with open(filename, 'w') as file:
        json.dump(scores, file)

def load_scores(filename):
    """
    Load the scores from a JSON file.
    Returns a dictionary with the scores.
    """
    try:
        with open(filename, 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {'X': 0, 'O': 0}
    return scores

def main():
    """
    Main function to handle the overall flow of the game,
    including loading and saving scores, initializing the board,
    and managing multiple rounds of gameplay.
    """
    scores_file = 'scores.json'
    scores = load_scores(scores_file)
    while True:
        size = int(input("Enter the board size (e.g., 3 for 3x3, 4 for 4x4, etc.): "))
        ai = input("Do you want to play against the AI? (y/n): ").strip().lower() == 'y'
        board = np.full((size, size), ' ')
        players = itertools.cycle(['X', 'O'])
        winner = play_game(board, size, players, ai)
        if winner:
            scores[winner] += 1
        print(f"Scores: Player X: {scores['X']} | Player O: {scores['O']}")
        save_scores(scores, scores_file)
        new_game = input("Do you want to start a new game? (y/n): ").strip().lower()
        if new_game != 'y':
            break

    print("Thank you for playing Tic Tac Toe!")

if __name__ == "__main__":
    main()