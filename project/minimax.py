import random
import numpy as np
from game import MyGame,Game, Move, Player
from copy import deepcopy
from collections import defaultdict

#get all possible (legal) moves from the current state
def possible_moves(game:MyGame,player_idx):
    
    moves = []
    equivalence_classes = defaultdict()

    for row in range(5):
        for col in range(5):
            for m in Move:

                game_var = deepcopy(game)
                move= ((row,col),m)

                if game_var.move((row,col),m,player_idx):
                    
                    board=game_var.get_board_hashable()
                    #get the last move corresponding to the same equivalence class since it doesn't change anything 
                    # because after the move the board is set to a "canonic" state
                    equivalence_classes[board]=move
    

    moves= list(equivalence_classes.values())
    return moves

def max_consecutive_symbols(board, s):
    max_count = 0

    # Function to count consecutive symbols in a sequence
    def count_consecutive(sequence):
        nonlocal max_count
        count = 0
        for cell in sequence:
            if cell == s:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0

    # Check rows
    for row in board:
        count_consecutive(row)

    # Check columns
    for col in range(5):
        column = [board[i][col] for i in range(5)]
        count_consecutive(column)

    # Check main diagonal
    main_diag = [board[i][i] for i in range(5)]
    count_consecutive(main_diag)

    # Check secondary diagonal
    sec_diag = [board[i][4 - i] for i in range(5)]
    count_consecutive(sec_diag)

    return max_count


#standard minimax with alpha-beta pruning
def utility(game:Game):
    cw = game.check_winner()
    #max won
    if cw == 0:
        return 1
    #min won
    elif cw == 1:
        return -1
    

def eval_h(game:MyGame):

    #if terminal state return the utility value
    if game.check_winner()>=0:
        return utility(game)
    
    #otherwise (depth is 0) compute a value to estimate the closeness to the goal
    board=game.get_board()
    #count the maximum number of consecutive symbols for max player 
    max_cons_s = max_consecutive_symbols(board,0)
    #count the maximum number of consecutive symbols for min player 
    min_cons_s = max_consecutive_symbols(board,1)
    
    #returns the fraction of maximum consecutive symbols on the board
    return (max_cons_s)//5

    
        

 
def minimax_alpha_beta(game:MyGame, depth, is_max,alpha_p, beta_p, pruning):
    
    if depth == 0 or game.check_winner()>=0:
        
        return eval_h(game), alpha_p,beta_p
    
    alpha=alpha_p
    beta=beta_p
    #player 0 is max player since it plays first 
    if is_max:
        max_eval = float('-inf')
        for move in possible_moves(game,0):
            game_cp=deepcopy(game)
            if game_cp.move(move[0],move[1],0):
                
                eval, alpha, beta = minimax_alpha_beta(game_cp, depth - 1, False,alpha, beta, pruning)
                max_eval = max(max_eval, eval)
                if pruning:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, alpha, beta
    else:
        min_eval = float('inf')
        for move in possible_moves(game,1):
            game_cp=deepcopy(game)
            if game_cp.move(move[0],move[1],1):
                
                eval, alpha, beta = minimax_alpha_beta(game_cp, depth - 1, True, alpha, beta, pruning)
                min_eval = min(min_eval, eval)
                if pruning:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, alpha, beta

def alpha_beta_search(game:MyGame, depth, pruning=False):
    best_move = None
    best_eval_max = float('-inf')
    best_eval_min = float('inf')
    alpha =float('-inf')
    beta =float('inf')
    playeridx = game.get_current_player()
    
    #first player (max)
    if playeridx == 0:
        for move in possible_moves(game,0):
            game_cp=deepcopy(game)
            if game_cp.move(move[0],move[1],0):
                
                eval, alpha, beta = minimax_alpha_beta(game_cp, depth - 1,False,alpha,beta,pruning) 
                if eval > best_eval_max:
                    best_eval_max = eval
                    best_move = move
                    #print("inside update")
                if pruning:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        #print("inside return move")
        return best_move
     #second player (min)
    else:
        for move in possible_moves(game,1):
            game_cp=deepcopy(game)
            if game_cp.move(move[0],move[1],1):
                
                eval, alpha, beta = minimax_alpha_beta(game_cp, depth - 1, True,alpha,beta,pruning)
                if eval < best_eval_min:
                    best_eval_min = eval
                    best_move = move
                if pruning:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return best_move
    

    