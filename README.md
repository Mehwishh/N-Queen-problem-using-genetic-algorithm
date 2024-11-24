# N-Queen problem using genetic algorithm
This project implements a genetic algorithm to solve the N-Queens problem using Tkinter for visualization. The genetic algorithm continuously evolves a population of candidate solutions until an optimal arrangement of queens is found, where no two queens threaten each other.

## N-Queens Problem

The N-Queens problem involves placing N queens on an N×N chessboard such that no two queens can attack each other. This means no two queens can be in the same row, column, or diagonal. The goal is to find a configuration of queens that satisfies this condition.

## Features

- **Genetic Algorithm**: Uses selection, crossover, and mutation to evolve a population of potential solutions.
- **Interactive GUI**: A simple interface where users can specify the number of queens and start the solver.
- **Chessboard Visualization**: Displays the current state of the board in each generation, highlighting the positions of the queens.

## Rules of the Algorithm

1. **Chromosome Representation**: A chromosome is a list of integers representing the positions of queens in columns.
   - Example: `[3, 1, 2, 4]` means a 4×4 board where queens are placed at rows 3, 1, 2, and 4 of columns 1, 2, 3, and 4 respectively.

2. **Fitness Function**: The fitness of a solution is determined by the number of queen collisions:
   - **Horizontal Collisions**: Queens placed in the same row.
   - **Diagonal Collisions**: Queens placed on the same diagonal.
   - The algorithm seeks to minimize these collisions.

3. **Selection**: Chromosomes are selected using roulette wheel selection, giving more fit chromosomes a higher chance of reproduction.

4. **Crossover**: A one-point crossover method is used to combine the genetic material of two parents, generating new offspring.

5. **Mutation**: Mutation is applied with a small probability (3%) to introduce variation into the population by randomly changing the position of a queen.

6. **Termination**: The algorithm stops when a solution is found, or the user manually stops the solver.

## Requirements

- Python 3.x
- Tkinter (usually included with Python, if not, you can install it via `pip install tk`)

## How to Run the Application

1. Clone this repository or download the files.
2. Open a terminal or command prompt and navigate to the project folder.
3. Run the `N-queen.py` script.

```bash
python N-queen.py
