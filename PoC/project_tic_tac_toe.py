"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    simulate a completed Tic-Tac-Toe game
    """
    while not board.check_win():
        empty_squares = board.get_empty_squares()
        chosen_square = random.choice(empty_squares)
        board.move(chosen_square[0], chosen_square[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    upon finishing one simulation, update the scores depending on the board
    """
    winner = board.check_win()
    dim = board.get_dim()
    if winner == player:
        for dummy_i in range(dim):
            for dummy_j in range(dim):
                if board.square(dummy_i, dummy_j) == player:
                    scores[dummy_i][dummy_j] += SCORE_CURRENT
                elif board.square(dummy_i, dummy_j) == provided.switch_player(player):
                    scores[dummy_i][dummy_j] -= SCORE_OTHER
    elif winner == provided.switch_player(player):
        for dummy_i in range(dim):
            for dummy_j in range(dim):
                if board.square(dummy_i, dummy_j) == player:
                    scores[dummy_i][dummy_j] -= SCORE_CURRENT
                elif board.square(dummy_i, dummy_j) == provided.switch_player(player):
                    scores[dummy_i][dummy_j] += SCORE_OTHER

def get_best_move(board, scores):
    """
    randomly choose a square with the highest score
    """
    empty_squares = board.get_empty_squares()
    if not empty_squares:
        return None, None
    scores_of_empties = [scores[dummy_i][dummy_j] for (dummy_i, dummy_j) in empty_squares]
    highest = max(scores_of_empties)
    highest_score_squares = [(row, col) for (row, col) in empty_squares if scores[row][col] == highest]
    return random.choice(highest_score_squares)

def mc_move(board, player, trials):
    """
    using Monte Carlo Method to simulate the Tic-Tac-Toe game
    """
    dim = board.get_dim()
    scores = [[0] * dim for dummy_i in range(dim)]
    for dummy_trial in range(trials):
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(scores, cloned_board, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

