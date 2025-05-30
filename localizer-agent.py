import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy.logic.inference import satisfiable

with open('maze-map.txt','r') as f:
    maze = [list(map(int,line.split())) for line in f]
first_pos = [rnd.randint(0,len(maze)-1),rnd.randint(0,len(maze[0])-1)]

while maze[first_pos[1]][first_pos[0]] == 1:
    first_pos = [rnd.randint(0, len(maze)-1),rnd.randint(0, len(maze[0])-1)]

pg.init()
disp = pg.display.set_mode((len(maze[0])*80, len(maze)*80))
disp.fill((255,255,255))

symbol_names = [[f"wall_n{i}",f"wall_s{i}",f"wall_w{i}",f"wall_e{i}"] for i in range(len(maze)*len(maze[0]))]
symbol_names = [val for item in symbol_names for val in item]
names_string = " ".join(symbol_names)
d_sym = symbols(names_string)
exp = And(*d_sym)

for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 1:
            pg.draw.rect(disp, (120,120,120), (j*80, i*80, 80, 80))
            pg.draw.rect(disp, (0,0,255), (j*80, i*80, 80, 80),2)
        else:
            pg.draw.rect(disp, (0,0,255), (j*80, i*80, 80, 80),2)
            for k in range(4):
                dr, dc = [-1,1,0,0][k], [0,0,-1,1][k]
                if i+dr >= 0 and i+dr < len(maze) and j+dc >= 0 and j+dc < len(maze[0]):
                    if maze[i+dr][j+dc] == 1:
                        exp.subs({d_sym[(i*len(maze[0])+j)*4+k]:True})

runnig = True
check = False
history = []

while runnig:
    pg.draw.rect(disp, (0, 255, 0),(first_pos[0]*80+5,first_pos[1]*80+5,70,70))
    pg.display.update()
    for event in pg.event.get():
        if not check:
            sens = ''
            for dr,dc in [[-1,0],[1,0],[0,-1],[0,1]]:
                if first_pos[1]+dr >= 0 and first_pos[1]+dr < len(maze) and first_pos[0]+dc >= 0 and first_pos[0]+dc < len(maze[0]):
                    if maze[first_pos[1]+dr][first_pos[0]+dc] == 1:
                        sens += '1'
                    else:
                        sens += '0'
                else:
                    sens += '2'
            check = True
            history.append(sens)
        if event.type == pg.QUIT:
            pg.quit()
            running = False
        if event.type == pg.KEYDOWN:
            pg.draw.rect(disp, (255, 255, 255), (first_pos[0]*80+2, first_pos[1]*80+2, 76, 76))
            if event.key == pg.K_h:
                print(history)
            if event.key in [pg.K_UP,pg.K_w]:
                check = False
                if first_pos[1] > 0 and maze[first_pos[1]-1][first_pos[0]] == 0:
                    first_pos[1] -= 1
            elif event.key in [pg.K_DOWN,pg.K_s]:
                check = False
                if first_pos[1] < len(maze)-1 and maze[first_pos[1]+1][first_pos[0]] == 0:
                    first_pos[1] += 1
            elif event.key in [pg.K_LEFT,pg.K_a]:
                check = False
                if first_pos[0] > 0 and maze[first_pos[1]][first_pos[0]-1] == 0:
                    first_pos[0] -= 1
            elif event.key in [pg.K_RIGHT,pg.K_d]:
                check = False
                if first_pos[0] < len(maze[0])-1 and maze[first_pos[1]][first_pos[0]+1] == 0:
                    first_pos[0] += 1