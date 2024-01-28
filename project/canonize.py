import numpy as np
from copy import deepcopy

def get_game_metrics(board):

    metrics=[0,0,1,1]
    flattened_board = board.flatten()
    
    # Find indices where values are equal to 0
    zero_indices = np.where(flattened_board == 0)[0]
    one_indeces = np.where(flattened_board == 1)[0]
    # Calculate the sum of indices plus 1 for zeros
    metrics[0] = np.sum(zero_indices + 1)
    metrics[1] = np.sum(one_indeces + 1)
    metrics[2] = np.multiply.reduce(zero_indices + 1)
    metrics[3] = np.multiply.reduce(one_indeces + 1)
    return metrics

#ctrl+k+c/u
def rotate_90_clockwise(board):
    # Transpose the board
    transposed_board = [[board[j][i] for j in range(5)] for i in range(5)]
    # Reverse each row to achieve 90-degree clockwise rotation
    rotated_board = [row[::-1] for row in transposed_board]
    return np.array(rotated_board)

def mirror_horizontal(board):
    return np.array([row[::-1] for row in board])

def mirror_vertical(board):
    return np.array(board[::-1])

def get_board_hashable(board):
        return tuple(map(tuple,deepcopy(board)))

#get canonic form for the state considering symmetries and rotations
def canonize(state):
    
    eq_list=[]
    
    
    # Check rotations (90-degree increments)
    eq_list.append(state)
    for _ in range(4):
        state = rotate_90_clockwise(state)  # Perform 90-degree rotation
        eq_list.append(state)

    
    s=mirror_vertical(state)
    eq_list.append(s) #equivalent.add(get_board_hashable(s))

    for _ in range(4):
        s = rotate_90_clockwise(s)  # Perform 90-degree rotation
        eq_list.append(s)

    equivalent= np.unique(np.array(eq_list),axis=0)
    

    metrics_dict={}

    for i in range(len(equivalent)):
        metrics_dict[i]=get_game_metrics(equivalent[i])
        
    base_case_idx = list(dict(sorted(metrics_dict.items(), key=lambda x: x[1])).keys())[0]

    return np.array(equivalent[base_case_idx])