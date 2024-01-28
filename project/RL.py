import numpy as np 
import pickle 
from collections import namedtuple, defaultdict
from itertools import combinations
from random import choice, random
from tqdm.auto import tqdm
from copy import deepcopy
from game import Game,MyGame, Move
from minimax import possible_moves
from canonize import canonize
import os



class MC_agent(object):

    def __init__(self,sym=False) -> None:
        #upload saved Q if any
          
        self.sym=sym
        if self.sym:
            file_path = 'project/Q_table_MC_sym.pkl'
        else:
            file_path = 'project/Q_table_MC.pkl'

        if os.path.exists(file_path):
            
            with open(file_path, 'rb') as file: 
                 
                self.Q = pickle.load(file) 
  
        else:
            self.Q = defaultdict(float)


    def play(self,on_policy=False):
        max_moves=30
        
        g=MyGame(canonize=self.sym)
        trajectory = list()

        for _ in range(max_moves):

            if on_policy:
                state=g.get_board_hashable()
                filtered={key: value for key, value in self.Q.items() if key[0] == state}
                if filtered:
                    ply0 = max(filtered,key=filtered.get)[1]
                else:
                    ply0 = choice(possible_moves(g,0))
            else:
                ply0 = choice(possible_moves(g,0))
            
            trajectory.append(tuple((g.get_board_hashable(),deepcopy(ply0),0))) 
            g.move(ply0[0],ply0[1],0)


            if  g.check_winner()>=0:
                trajectory.append(tuple((g.get_board_hashable(),None,1)))
                break

            ply1 = choice(possible_moves(g,1))
            trajectory.append(tuple((g.get_board_hashable(),deepcopy(ply1),1)))
            g.move(ply1[0],ply1[1],1)

            

            if g.check_winner()>=0:
                trajectory.append(tuple((g.get_board_hashable(),None,0)))
                break

        return trajectory, g.check_winner()
    
    def get_reward(self,winner):
        if winner == 0:
            return 1
        elif winner == 1:
            return -1
        else:
            return 0
        
    def train(self,on_policy = False):
        num_iterations=50_000
        N = defaultdict(int)

        for _ in tqdm(range(num_iterations)):
            
            trajectory, final_game_state = self.play()
            
            final_reward = self.get_reward(final_game_state)

            for state_action in trajectory:
            
                # Update N-values (visit count for state-action pairs)
                N[state_action] += 1

                # Update Q-value using incremental update rule
                self.Q[state_action] += (1 / N[state_action]) * (final_reward - self.Q[state_action])
        #save table
        if self.sym:
            file_path='project/Q_table_MC_sym.pkl'
        else:
            file_path='project/Q_table_MC.pkl'

        with open(file_path, 'wb') as file: 
      
            # Call load method to deserialze 
            pickle.dump(self.Q,file)

    def get_move(self,game:MyGame):

        state=game.get_board_hashable()
        
        player=game.get_current_player()
        filtered={key: value for key, value in self.Q.items() if key[0] == state and key[2] == player}
        
        if filtered and player==0:
            action = deepcopy(max(filtered,key=filtered.get)[1])
            
        elif filtered and player==1:
            action = deepcopy(min(filtered,key=filtered.get)[1])
        else:
            action = choice(possible_moves(game,player))
            
        return action
        