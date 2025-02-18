# -*- coding: utf-8 -*-
"""Tic_tac_toe_enhanced.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1L3orGPh82GcLuX2TFExt_F8FI3tW5wE7
"""

!pip install colorama

import numpy as np
import itertools
import random
import json
from colorama import Fore, Style, init
from typing import Tuple, Optional, Dict

# Initialize colorama for colored output
init(autoreset=True)

def print_board(board: np.ndarray) -> None:
    """
    Print the current state of the board with row and column indices.

    Args:
        board (np.ndarray): The game board represented as a 2D numpy array.
    """
    size: int = board.shape[0]
    # Print header row with column indices
    print("  " + " ".join(map(str, range(size))))
    # Print each row with row index and formatted cells
    for i in range(size):
        row_str = " ".join(
            [
                f"{Fore.RED}X{Style.RESET_ALL}" if cell == 'X'
                else f"{Fore.BLUE}O{Style.RESET_ALL}" if cell == 'O'
                else cell
                for cell in board[i]
            ]
        )
        print(f"{i} {row_str}")
    print()

def check_winner(board: np.ndarray, player: str, size: int) -> bool:
    """
    Check if the specified player has won the game.

    Args:
        board (np.ndarray): The game board.
        player (str): The player symbol ('X' or 'O').
        size (int): The size of the board.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check rows for a win
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns for a win (using numpy's transpose)
    for col in board.T:
        if all(cell == player for cell in col):
            return True
    # Check main diagonal
    if all(board[i, i] == player for i in range(size)):
        return True
    # Check anti-diagonal
    if all(board[i, size - 1 - i] == player for i in range(size)):
        return True
    return False

def get_move(size: int) -> Tuple[int, int]:
    """
    Prompt the player to enter their move and validate the input.

    Args:
        size (int): The size of the board.

    Returns:
        Tuple[int, int]: A tuple (row, col) representing the move.
    """
    while True:
        move_input: str = input("Enter your move (row and column, e.g., 0 1): ").strip()
        parts = move_input.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            row, col = int(parts[0]), int(parts[1])
            if 0 <= row < size and 0 <= col < size:
                return row, col
        print("Invalid move. Please try again.")

def ai_move(board: np.ndarray) -> Tuple[int, int]:
    """
    Generate a random move for the AI.

    Args:
        board (np.ndarray): The game board.

    Returns:
        Tuple[int, int]: The (row, col) position chosen by the AI.
    """
    size: int = board.shape[0]
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i, j] == ' ']
    # In case the board is full, though this should be handled before calling ai_move
    return random.choice(empty_cells) if empty_cells else (-1, -1)

def play_game(board: np.ndarray, size: int, players: itertools.cycle, ai: bool = False) -> Optional[str]:
    """
    Manage gameplay by alternating turns between players, updating the board,
    and checking for a winner after each move.

    Args:
        board (np.ndarray): The game board.
        size (int): The size of the board.
        players (itertools.cycle): Cycle iterator for player turns.
        ai (bool): Whether the game is played against an AI. Defaults to False.

    Returns:
        Optional[str]: The winning player's symbol if there's a winner, otherwise None.
    """
    print_board(board)
    for _ in range(size * size):
        current_player: str = next(players)
        print(f"Player {current_player}'s turn.")
        # Get move from AI or user
        if ai and current_player == 'O':
            row, col = ai_move(board)
        else:
            row, col = get_move(size)
        # Validate move: ensure the cell is empty
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

def save_scores(scores: Dict[str, int], filename: str) -> None:
    """
    Save the player scores to a JSON file.

    Args:
        scores (Dict[str, int]): Dictionary containing scores for each player.
        filename (str): The filename to save scores to.
    """
    with open(filename, 'w') as file:
        json.dump(scores, file)

def load_scores(filename: str) -> Dict[str, int]:
    """
    Load player scores from a JSON file.

    Args:
        filename (str): The filename to load scores from.

    Returns:
        Dict[str, int]: Dictionary of player scores.
    """
    try:
        with open(filename, 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {'X': 0, 'O': 0}
    return scores

def main() -> None:
    """
    Main function to run the Tic Tac Toe game. It manages score loading,
    game initialization, and handling multiple rounds of gameplay.
    """
    scores_file: str = 'scores.json'
    scores: Dict[str, int] = load_scores(scores_file)

    while True:
        try:
            size_input: str = input("Enter the board size (e.g., 3 for 3x3, 4 for 4x4, etc.): ").strip()
            size: int = int(size_input)
        except ValueError:
            print("Invalid board size. Please enter a valid integer.")
            continue

        ai_choice: str = input("Do you want to play against the AI? (y/n): ").strip().lower()
        ai_flag: bool = ai_choice == 'y'

        # Initialize the game board with empty spaces
        board: np.ndarray = np.full((size, size), ' ')
        players = itertools.cycle(['X', 'O'])
        winner: Optional[str] = play_game(board, size, players, ai_flag)

        if winner:
            scores[winner] = scores.get(winner, 0) + 1
        print(f"Scores: Player X: {scores.get('X', 0)} | Player O: {scores.get('O', 0)}")
        save_scores(scores, scores_file)

        new_game: str = input("Do you want to start a new game? (y/n): ").strip().lower()
        if new_game != 'y':
            break

    print("Thank you for playing Tic Tac Toe!")

if __name__ == "__main__":
    main()