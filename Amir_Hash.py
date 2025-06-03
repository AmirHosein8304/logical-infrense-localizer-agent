import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or , Implies

def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]

maze = load_maze('maze-map.txt')


def Logic_maker(old_percept, new_percept, action):
    old_sym = symbols(f"Percept_{''.join(map(str, old_percept))}")
    action_sym = symbols(f"Action_{action}")
    new_sym = symbols(f"Percept_{''.join(map(str, new_percept))}")
    
    return Implies(And(old_sym, action_sym), new_sym)


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
    valid_final_positions = set()

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                continue  # skip walls

            pos = (r, c)
            percept = get_percept(maze, r, c)
            valid = True

            for expr in knowledge_base:
                premise = expr.args[0]  # an And(...)
                conclusion = expr.args[1]  # a Percept_YYYY

                # Extract old_sym (Percept_....) and action_sym (Action_...) from premise.args
                old_sym = None
                action_sym = None
                for sym in premise.args:
                    name = str(sym)
                    if name.startswith("Percept_"):
                        old_sym = sym
                    elif name.startswith("Action_"):
                        action_sym = sym

                # If we didn’t find exactly one Percept_ and one Action_, bail out
                if old_sym is None or action_sym is None:
                    valid = False
                    break

                # 1) Check that the current percept matches old_sym
                expected_old_sym = "Percept_" + "".join(map(str, percept))
                if str(old_sym) != expected_old_sym:
                    valid = False
                    break

                # 2) Extract the action string (e.g. "W" from "Action_W")
                action = str(action_sym).split("_", 1)[1]

                # 3) Simulate the move on (r,c)
                r2, c2 = pos
                if action == "W":
                    r2 -= 1
                elif action == "S":
                    r2 += 1
                elif action == "A":
                    c2 -= 1
                elif action == "D":
                    c2 += 1

                # 4) If that new cell is invalid (out of bounds or a wall), no good
                if not (0 <= r2 < rows and 0 <= c2 < cols and maze[r2][c2] == 0):
                    valid = False
                    break

                # 5) Compute the new percept at (r2,c2)
                percept = get_percept(maze, r2, c2)
                expected_new_sym = "Percept_" + "".join(map(str, percept))
                # 6) Check that matches conclusion
                if str(conclusion) != expected_new_sym:
                    valid = False
                    break

                # 7) Move on to the next step
                pos = (r2, c2)

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
