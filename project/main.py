import random
import numpy as np
from game import Game,MyGame, Move, Player
from tqdm.auto import tqdm
from minimax import alpha_beta_search,possible_moves
from RL import MC_agent
from canonize import canonize

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'MyGame') -> tuple[tuple[int, int], Move]:

        moves=possible_moves(game,game.get_current_player())
        
        move = random.choice(moves)
        
        return move[0], move[1]
        
#minimax with alpha beta pruning
class MinimaxPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'MyGame') -> tuple[tuple[int, int], Move]:
        move = alpha_beta_search(game,3)
        
        return move[0],move[1]
    
    
#reinforcement learning with monte carlo
class RLMCPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.agent= MC_agent(sym=True)

        
    def train(self):
        if not self.agent.Q:
            self.agent.train()
        #print(len(self.agent.Q))

    def make_move(self, game: 'MyGame') -> tuple[tuple[int, int], Move]:
        
        move = self.agent.get_move(game)
        return move[0],move[1]

def eval_games():
    games= 100
    won=0
    lost=0
    draw=0
    player1 = RLMCPlayer()
    player2 = RandomPlayer()
    
    for _ in tqdm(range(games)):
        g = MyGame(canonize=True)
        winner = g.play(player1, player2)
        #g.print()
       
        if winner==0:
            won+=1
        elif winner==1:
            lost+=1
        else:
            draw+=1
        print(f"Won:{won}, Lost: {lost},Drawn: {draw}")
    print(f"Won:{won}, Lost: {lost},Drawn: {draw}")

if __name__ == '__main__':
    
    #if it needs to train RLMC do:
    #rl = RLMCPlayer()
    #rl.train()
    eval_games()