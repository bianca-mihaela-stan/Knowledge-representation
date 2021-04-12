## Features
- [x] Input files are given in the command line, through a path to a designated directory. Same for the output directory and the number of solutions. The command line also specifies the tiomeout.
```
python m.py Inputs Outputs 10 60
```
- [x] Parsing the input file.
- [x] Generating successors.
- [x] Calculating the cost for a move as 1 + (N-K)/N, where N is the number of characters of the type we are removing and K is the number of characters we are removing through this move. 
- [x] Testing to check if the goal state was reached.
- [x] 4 heuristics:
  - [x] **obvious heuristc**: 
  ```
  h = 1 if state is non terminal
  h = 0 if state is terminal
  ```
  - [x] **first heuristic**: this heuristic takes advantage of the fact that the cost of every move ranges between \[1,2)
  ```
  h = number of characters in the current state
  ```
  - [x] **second heuristic**: this heuristic works because it gives a cost in between the first heuristic and the cost of removing each individual xone on its own.
  ```
  h = 1 - K/N, where N is the number of characters of the type we are removing and K is the number of characters we are removing through this move. 
  ```
  - [x] **invalid heuristic**: this heuristic assumes that we remove each zone on its won, without moving the characters    
  ```
  h = 1 + (N-K)/N,  where N is the number of characters of the type we are removing and K is the number of characters we are removing through this move. 
  ```
- [x] input files: 
  - [x] a file with no solutions:
  - [x] a file where the initial state is also final
  - [x] a file with small solution lengths
  - [x] a file that timeouts an algorithm
  - [x] at least one of these files should result in a subobtimal result for the invalid heuristic
  ```
  input4.in
  second heuristic costs: 4.5 4.5 4.5 4.5 4.5 4.5 4.75 4.75 4.75 5.75
  invalid heuristic costs: 4.5 5.75 6.25 6.25 6.25 4.5 4.5 6.0 6.0 6.0
  ```
- [x] for each solution output:
  - [ ] id of every node in solution
  - [x] solution length
  - [x] cost  
  - [x] time needed to find the solution
  - [x] maximum number of nodes generated at any point in time
  - [x] total number of nodes generated 
- [x] validations:
  - [ ] checking if input data is correct
  - [x] checking if a state could result in a goal state or not
- [x] table


| algorithm | solution length | cost | time | maximum number of nodes | total number of nodes
| - | - | - | - | - | - |
| uniform cost search | 4 | 3 | 0.003 | 5 | 9 |
| A* - obvious heuristic | 4 | 3 | 0.003 | 5 | 7 |
| A* - first heuristic | 4 | 3 | 0.004 | 5 | 6 |
| A* - second heuristic | | | | | |
| A* - invalid heuristic | | | | | |
| optimized A* - obvious heuristic | 4 | 3 | 0.003 | 10 | 9 |
| optimized A* - first heuristic | 4 | 3 | 0.003 | 10 | 9 |
| optimized A* - second heuristic | | | | | |
| optimized A* - invalid heuristic | | | | | |
| iterative deepening A* - obvious heuristic | 4 | 3 | 0.006 | 6 | 18 |
| iterative deepening A* - first heuristic | | | | | |
| iterative deepening A* - second heuristic | | | | | |
| iterative deepening A* - invalid heuristic | | | | | |





- [ ] 
