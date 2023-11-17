
# LAB2 - ES

In this lab the objective is to develop an expert system able to play the nim game (misère game, the one who take sthe last stone(s) loses) following some rules (included the nim sum) and, an evolved agent able to find the best strategy among a set of different strategies. 

## Expert System

The expert system devoped follows a set of rules among which there is the nim sum rule defined as follows:

Let X be the nim-sum of all the heap sizes. Find a heap where the nim-sum of X and heap-size is less than the heap-size; the winning strategy is to play in such a heap, reducing that heap to the nim-sum of its original size with X [definition taken from Wikipedia: https://en.wikipedia.org/wiki/Nim#Mathematical_theory].

For misère game the strategy changes a bit only in the end-game.

## Evolved Agent

The evolutionary strategy implemented is a (1 + λ) ES with self-adaptation of the parameter sigma which drives the normal gaussian distribution used to tweak the list of float values (weights) hence using gaussian mutation.

- The genotype is given by a list of weights each corresponding to a strategy. 

- The fitness function is obtained by making the strategies play against the strategy "gabriele". A variation of the fitness is obtained by making the selected strategy play against all other strategies an equal number of games. The value of the fitness is given by the number of wins of the used strategy divided by the total number of games.

For each call of the fitness function the strategies play 100 games. At each turn of the evolved agent, the move to be selected is the one realted to the maximum sum of weights where each weight is relative to the strategy which chose that move. It basically uses a weighted voting system to choose the best move where each weight is related to a strategy.

The number of generations is defined inversely proportional to λ (the offspring size). At each generation λ individuals are generated through the gaussian mutation of the parent. Then they are evaluated using the fitness function and then the best is selected. The fittest individual between the parent and the fittest children is selected as parent for the next generation.

The adaptive rate is defined as 1/100 of the total number of generations. Every 100 generations sigma is upadted as following (one-out-of-five rule has been used):

- If the number of offspring with better fitness than their parent in the last 100 generations is lower than 1/5 decrease the variance (hence favouring exploitation over exploration).

- If the number of offspring with better fitness than their parent in the last 100 generations is greater than 1/5 increase the variance (hence favouring exploration over exploitation).

Once the best set of weights is obtained at the end of the training, the evolved agent is tested by using the same weighted voting system used for training. Note: the weights might be negative, hence before using them for the voting system they are shifted to make them greater than or equal than zero.