import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or

def load_maze(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.strip().split())) for line in f]

def possible_positions(maze):
    return [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == 0]

def percept_at(maze, pos):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    percept = []
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            percept.append(1 if maze[nr][nc] == 1 else 0)
        else:
            percept.append(1) 
    return tuple(percept)  

def build_kb(maze):
    kb = {}
    for pos in possible_positions(maze):
        kb[pos] = percept_at(maze, pos)
    return kb

def draw_maze(maze, screen):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            rect = pg.Rect(j*80, i*80, 80, 80)
            if maze[i][j] == 1:
                pg.draw.rect(screen, (120, 120, 120), rect)
            pg.draw.rect(screen, (0, 0, 255), rect, 2)

def draw_agent(pos, screen):
    pg.draw.rect(screen, (0, 255, 0), (pos[1]*80+5, pos[0]*80+5, 70, 70))

def update_belief(belief, kb, percept):
    return [pos for pos in belief if kb[pos] == percept]

def main():
    maze = load_maze('maze-map.txt')
    kb = build_kb(maze)
    
    pg.init()
    screen = pg.display.set_mode((len(maze[0])*80, len(maze)*80))
    draw_maze(maze, screen)

    current_pos = rnd.choice(possible_positions(maze))
    belief = possible_positions(maze)
    percept_history = []

    running = True
    clock = pg.time.Clock()

    while running:
        screen.fill((255, 255, 255))
        draw_maze(maze, screen)
        draw_agent(current_pos, screen)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                dr, dc = 0, 0
                if event.key in [pg.K_w, pg.K_UP]: dr = -1
                elif event.key in [pg.K_s, pg.K_DOWN]: dr = 1
                elif event.key in [pg.K_a, pg.K_LEFT]: dc = -1
                elif event.key in [pg.K_d, pg.K_RIGHT]: dc = 1

                new_r = current_pos[0] + dr
                new_c = current_pos[1] + dc
                if 0 <= new_r < len(maze) and 0 <= new_c < len(maze[0]) and maze[new_r][new_c] == 0:
                    current_pos = (new_r, new_c)

                    percept = percept_at(maze, current_pos)
                    percept_history.append(percept)

                    belief = update_belief(belief, kb, percept)
                    print(f"Percept: {percept}, Belief size: {len(belief)}")
                    if len(belief) == 1:
                        print(f"You are at position {belief[0]} with 100% certainty!")

        clock.tick(10)

    pg.quit()

if __name__ == '__main__':
    main()
