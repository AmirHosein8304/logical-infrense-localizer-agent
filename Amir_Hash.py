from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy.logic.inference import satisfiable

def load_maze(filename):
    maze = []
    with open(filename, 'r') as f:
        for line in f:
            print(row)
            row = [int(cell) for cell in line.split()]
            maze.append(row)
    return maze

print(load_maze('Maze.txt'))
