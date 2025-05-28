import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or

# ========== Maze Loading ==========
def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]

maze = load_maze('maze-map.txt')

# ========== Helper Functions ==========
def get_percept(maze, r, c):
    # Format: (W, E, S, N)
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    percept = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            percept.append(1 if maze[nr][nc] == 1 else 0)
        else:
            percept.append(1)  # Outside the maze is a wall
    return tuple(percept)

def expected_percept(maze, r, c):
    return get_percept(maze, r, c)

# ========== Belief State Update ==========
def get_consistent_positions(maze, percept_history):
    rows, cols = len(maze), len(maze[0])
    belief = set((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0)

    for t, percept in enumerate(percept_history):
        new_belief = set()
        for r, c in belief:
            if expected_percept(maze, r, c) == percept:
                new_belief.add((r, c))
        belief = new_belief
    return belief

# ========== Pygame Setup ==========
cell_size = 80
pg.init()
disp = pg.display.set_mode((len(maze[0]) * cell_size, len(maze) * cell_size))
pg.display.set_caption("Logic-Based Localization Agent")

# ========== Initial Position ==========
agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]
while maze[agent_pos[1]][agent_pos[0]] == 1:
    agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]

# ========== Main Loop ==========
percept_history = []
timestep = 0
max_steps = 10
running = True
clock = pg.time.Clock()

while running and timestep < max_steps:
    disp.fill((255, 255, 255))

    # Draw maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            color = (120, 120, 120) if maze[i][j] == 1 else (255, 255, 255)
            pg.draw.rect(disp, color, (j * cell_size, i * cell_size, cell_size, cell_size))
            pg.draw.rect(disp, (0, 0, 255), (j * cell_size, i * cell_size, cell_size, cell_size), 2)

    # Draw belief state
    belief = get_consistent_positions(maze, percept_history)
    for r, c in belief:
        pg.draw.rect(disp, (200, 255, 200), (c * cell_size + 10, r * cell_size + 10, 60, 60))

    # Draw agent
    pg.draw.rect(disp, (0, 255, 0), (agent_pos[0] * cell_size + 5, agent_pos[1] * cell_size + 5, 70, 70))

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            moved = False
            if event.key in [pg.K_w, pg.K_UP]:
                if agent_pos[1] > 0 and maze[agent_pos[1] - 1][agent_pos[0]] == 0:
                    agent_pos[1] -= 1
                    moved = True
            elif event.key in [pg.K_s, pg.K_DOWN]:
                if agent_pos[1] < len(maze) - 1 and maze[agent_pos[1] + 1][agent_pos[0]] == 0:
                    agent_pos[1] += 1
                    moved = True
            elif event.key in [pg.K_a, pg.K_LEFT]:
                if agent_pos[0] > 0 and maze[agent_pos[1]][agent_pos[0] - 1] == 0:
                    agent_pos[0] -= 1
                    moved = True
            elif event.key in [pg.K_d, pg.K_RIGHT]:
                if agent_pos[0] < len(maze[0]) - 1 and maze[agent_pos[1]][agent_pos[0] + 1] == 0:
                    agent_pos[0] += 1
                    moved = True

            if moved:
                percept = get_percept(maze, agent_pos[1], agent_pos[0])
                percept_history.append(percept)
                timestep += 1

    clock.tick(10)

pg.quit()

print("True final position:", tuple(agent_pos))
print("Belief state:", get_consistent_positions(maze, percept_history))
