import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or , Implies

def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]

maze = load_maze('maze-map.txt')


def Logic_maker(old, current, action):

    old_sym = symbols(f"Pos_{old[0]}_{old[1]}")
    action_sym = symbols(f"Action_{action}")
    new_sym = symbols(f"Pos_{current[0]}_{current[1]}")
    
    logic_expr = Implies(And(old_sym, action_sym), new_sym)
    return logic_expr


def get_percept(maze, r, c):
    # Format: (W, E, S, N)
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    percept = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            percept.append(1 if maze[nr][nc] == 1 else 0)
        else:
            percept.append(1)  
    return tuple(percept)

def expected_percept(maze, r, c):
    return get_percept(maze, r, c)


def final_pos_guesser(maze, knowledge_base):
    rows, cols = len(maze), len(maze[0])
    possible_starts = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == 0]
    valid_final_positions = set()

    for start in possible_starts:
        pos = start
        valid = True
        for expr in knowledge_base:
            # Parse expression: (Pos_r_c & Action_X) → Pos_r2_c2
            if not isinstance(expr.args[0], And):
                valid = False
                break
            
            premise = expr.args[0]  # And(Pos_r_c, Action_X)
            conclusion = expr.args[1]  # Pos_r2_c2

            # Extract old_pos and action from premise
            old_symbol = premise.args[0]
            action_symbol = premise.args[1]

            # Match current simulated position and intended transition
            expected_old = f"Pos_{pos[0]}_{pos[1]}"
            if str(old_symbol) != expected_old:
                valid = False
                break

            # Extract target from conclusion
            next_pos_parts = str(conclusion).split("_")
            new_r = int(next_pos_parts[1])
            new_c = int(next_pos_parts[2])
            pos = (new_r, new_c)

            # Check that we don’t walk into walls
            if not (0 <= pos[0] < rows and 0 <= pos[1] < cols and maze[pos[0]][pos[1]] == 0):
                valid = False
                break

        if valid:
            valid_final_positions.add(pos)

    return valid_final_positions


cell_size = 80
pg.init()
disp = pg.display.set_mode((len(maze[0]) * cell_size, len(maze) * cell_size))
pg.display.set_caption("Logic-Based Localization Agent")

agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]
while maze[agent_pos[1]][agent_pos[0]] == 1:
    agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]
percept = get_percept(maze, agent_pos[1], agent_pos[0])
old_pos = tuple(percept)

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
                    action = "W"
                    moved = True
            elif event.key in [pg.K_s, pg.K_DOWN]:
                if agent_pos[1] < len(maze) - 1 and maze[agent_pos[1] + 1][agent_pos[0]] == 0:
                    agent_pos[1] += 1
                    action = "S"
                    moved = True
            elif event.key in [pg.K_a, pg.K_LEFT]:
                if agent_pos[0] > 0 and maze[agent_pos[1]][agent_pos[0] - 1] == 0:
                    agent_pos[0] -= 1
                    action = "A"
                    moved = True
            elif event.key in [pg.K_d, pg.K_RIGHT]:
                if agent_pos[0] < len(maze[0]) - 1 and maze[agent_pos[1]][agent_pos[0] + 1] == 0:
                    agent_pos[0] += 1
                    action = "D"
                    moved = True

            if moved:
                new_pos = get_percept(maze, agent_pos[1], agent_pos[0])
                logic_expr = Logic_maker(old_pos, new_pos, action)
                percept_history.append(logic_expr)
                old_pos = new_pos
                timestep += 1

    clock.tick(10)

pg.quit()

print("True final position:", tuple(agent_pos))
print("Belief state:", final_pos_guesser(maze, percept_history))
