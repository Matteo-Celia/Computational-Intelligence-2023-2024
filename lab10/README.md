
# LAB10

The goal of this lab is to implement a reinforcement learning algorithm to create an agent able to play Tic-Tac-Toe.

## Reinforcement Learning


## Results

Agent plays 'X':

| Method      | % won | % lost    | % drawn | size of Q-table|
| :---        |    :----:   |          :---: | :---: | ---: |
| Q-learning      | 0.98749   |  0.0   |  0.01251 | 17K
| Monte Carlo   | 0.98989    | 0.0      |0.01011 | 15K

Agent plays 'O':
    
| Method      | % won | % lost    | % drawn | size of Q-table|
| :---        |    :----:   |          :---: | :---: | ---: |
| Q-learning      | 0.7915   |  0.07761   |  0.13089 | 17K
| Monte Carlo   | 0.76846    | 0.12523     | 0.10631 | 15K
  
### Exploiting symemtries

Agent plays 'X':

| Method      | % won | % lost    | % drawn | size of Q-table|
| :---        |    :----:   |          :---: | :---: |---: |
| Q-learning      |0.91273    |  0.01298     | 0.07429 | 13K
| Monte Carlo   | 0.96667   |   0.00985   |   0.02348| 10K

Agent plays 'O':
        
| Method      | % won      | % lost    | % drawn | size of Q-table|
| :---        |    :----:   |          :---: | :---: | ---: |
| Q-learning      | 0.70938   |  0.00794   |  0.28268 | 13K
| Monte Carlo   | 0.6575    | 0.00293    | 0.33957 | 10K