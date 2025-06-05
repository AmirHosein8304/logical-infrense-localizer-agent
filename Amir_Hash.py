import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Implies
import tkinter as tk

def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]

maze = load_maze('maze-map.txt')

def update_tkinter_belief_state(belief_set):
    if not belief_set:
        text_to_display = "Belief State: Empty or Agent is trapped."
    else:
        positions_str = " | ".join(map(str, sorted(list(belief_set))))
        text_to_display = f"Possible Final Positions (Belief State):\n{positions_str}"
    belief_state_label.config(text=text_to_display)
    left_pannel.update()

def update_tkinter_history(shown_p_h):
    shown_p_h = [",".join(map(str, shown_p_h[i:i+2])) for i in range(0, len(shown_p_h), 2)]
    text_to_display = " | ".join(shown_p_h)
    history_label.config(text=f"History:\n{text_to_display}")
    right_pannel.update()
    

def Logic_maker(old_percept, new_percept, action):
    old_sym = symbols(f"Percept_{''.join(map(str, old_percept))}")
    action_sym = symbols(f"Action_{action}")
    new_sym = symbols(f"Percept_{''.join(map(str, new_percept))}")
    
    return Implies(And(old_sym, action_sym), new_sym)


def get_percept(maze, r, c):
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    percept = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            percept.append(1 if maze[nr][nc] == 1 else 0)
        else:
            percept.append(1)  
    return tuple(percept)

def final_pos_guesser(maze, knowledge_base):
    rows, cols = len(maze), len(maze[0])
    valid_final_positions = set()

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 1:
                continue

            pos = (c, r)
            percept = get_percept(maze, r, c)
            valid = True

            for expr in knowledge_base:
                premise = expr.args[0]
                conclusion = expr.args[1]
                old_sym = None
                action_sym = None
                for sym in premise.args:
                    name = str(sym)
                    if name.startswith("Percept_"):
                        old_sym = sym
                    elif name.startswith("Action_"):
                        action_sym = sym
                if old_sym is None or action_sym is None:
                    valid = False
                    break
                expected_old_sym = "Percept_" + "".join(map(str, percept))
                if str(old_sym) != expected_old_sym:
                    valid = False
                    break
                action = str(action_sym).split("_", 1)[1]
                c2, r2 = pos
                if action == "W":
                    r2 -= 1
                elif action == "S":
                    r2 += 1
                elif action == "A":
                    c2 -= 1
                elif action == "D":
                    c2 += 1
                if not (0 <= r2 < rows and 0 <= c2 < cols and maze[r2][c2] == 0):
                    valid = False
                    break
                percept = get_percept(maze, r2, c2)
                expected_new_sym = "Percept_" + "".join(map(str, percept))
                if str(conclusion) != expected_new_sym:
                    valid = False
                    break
                pos = (c2, r2)
            if valid:
                valid_final_positions.add(pos)
    return valid_final_positions

left_pannel = tk.Tk()
left_pannel.title("Belief State Panel")
left_pannel.geometry("400x300")
belief_state_label = tk.Label(left_pannel, text="Belief State will appear here.", wraplength=380, justify="left", font=("Arial", 10))
belief_state_label.pack(pady=10, padx=10)
right_pannel = tk.Tk()
right_pannel.title("History Panel")
right_pannel.geometry("400x300")
history_label = tk.Label(right_pannel, text="History will appear here.", wraplength=380, justify="left", font=("Arial", 10))
history_label.pack(pady=10, padx=10)

pg.init()
disp = pg.display.set_mode((len(maze[0]) * 80, len(maze) * 80))
pg.display.set_caption("Logic-Based Localization Agent")

agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]
while maze[agent_pos[1]][agent_pos[0]] == 1:
    agent_pos = [rnd.randint(0, len(maze[0])-1), rnd.randint(0, len(maze)-1)]
percept = get_percept(maze, agent_pos[1], agent_pos[0])
old_pos = tuple(percept)

percept_history = []
shown_p_h = [get_percept(maze, agent_pos[0], agent_pos[1]), "No action done!"]
timestep = 0
running = True
clock = pg.time.Clock()
update_tkinter_belief_state(final_pos_guesser(maze, percept_history))
update_tkinter_history(shown_p_h)

while running and timestep < 10:
    disp.fill((255, 255, 255))

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            color = (120, 120, 120) if maze[i][j] == 1 else (255, 255, 255)
            pg.draw.rect(disp, color, (j * 80, i * 80, 80, 80))
            pg.draw.rect(disp, (0, 0, 255), (j * 80, i * 80, 80, 80), 2)

    pg.draw.rect(disp, (0, 255, 0), (agent_pos[0] * 80 + 5, agent_pos[1] * 80 + 5, 70, 70))
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
                update_tkinter_belief_state(final_pos_guesser(maze, percept_history))
                update_tkinter_history(shown_p_h)
                new_pos = get_percept(maze, agent_pos[1], agent_pos[0])
                shown_act = ""
                if action == "W":
                    shown_act = "Up"
                elif action == "S":
                    shown_act = "Down"
                elif action == "A":
                    shown_act = "Left"
                else:
                    shown_act = "Right"
                shown_p_h.extend([new_pos,shown_act])
                logic_expr = Logic_maker(old_pos, new_pos, action)
                percept_history.append(logic_expr)
                old_pos = new_pos
                timestep += 1

    clock.tick(10)

pg.quit()

update_tkinter_belief_state(final_pos_guesser(maze, percept_history))
update_tkinter_history(shown_p_h)
left_pannel.mainloop()
right_pannel.mainloop()

