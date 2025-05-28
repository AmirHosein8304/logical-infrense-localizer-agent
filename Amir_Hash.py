from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy.logic.inference import satisfiable

def load_maze(filename):
    maze = []
    with open(filename, 'r') as f:
        for line in f:
            row = [int(cell) for cell in line.strip()] 
            maze.append(row)
    return maze

def get_free_positions(maze):
    positions = []
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0:
                positions.append((r, c))
    return positions

def next_Location_in_Maze(Maze,movement,current_loc):
    row, col = current_loc
    if movement == 'w':
        row -= 1
    elif movement == 's':
        row += 1
    elif movement == 'a':
        col -= 1
    elif movement == 'd':
        col += 1
    if row < 0 or row >= len(Maze) or col < 0 or col >= len(Maze[0]):
        return None
    if Maze[row][col] == 1:
        return None
    return (row, col)

def get_possible_movements(Maze, current_loc):
    movements = []
    for movement in ['w', 's', 'a', 'd']:
        next_loc = next_Location_in_Maze(Maze, movement, current_loc)
        if next_loc is not None:
            movements.append(movement)
    return movements

def surounding(Maze, current_loc):
    row, col = current_loc
    surroundings = {}
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < len(Maze) and 0 <= c < len(Maze[0]):
            if (dr,dc) == (0,1):
                surroundings['right'] = Maze[r][c]
            if (dr, dc) == (0, -1):
                surroundings['left'] = Maze[r][c]
            if (dr, dc) == (1, 0):
                surroundings['down'] = Maze[r][c]
            if (dr, dc) == (-1, 0):
                surroundings['up'] = Maze[r][c]

def Knowledge_Base(Maze, current_loc, action, surroundings):
    # 0 is free space 1 is wall
    Knowledge_Base = []
    row, col = current_loc




