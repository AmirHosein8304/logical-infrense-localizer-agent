import pygame as pg
import random as rnd
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies
with open('maze-map.txt','r') as f:
    maze = [list(map(int,line.split())) for line in f]
first_pos = [rnd.randint(0,len(maze)-1),rnd.randint(0,len(maze[0])-1)]
while maze[first_pos[1]][first_pos[0]] == 1:
    first_pos = [rnd.randint(0, len(maze)-1),rnd.randint(0, len(maze[0])-1)]
print(first_pos)
pg.init()
disp = pg.display.set_mode((len(maze[0])*80, len(maze)*80))
disp.fill((255,255,255))
for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 1:
            pg.draw.rect(disp, (120,120,120), (j*80, i*80, 80, 80))
            pg.draw.rect(disp, (0,0,255), (j*80, i*80, 80, 80),2)
        else:
            pg.draw.rect(disp, (0,0,255), (j*80, i*80, 80, 80),2)
runnig = True
while runnig:
    pg.draw.rect(disp, (0, 255, 0),(first_pos[0]*80+5,first_pos[1]*80+5,70,70))
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
        if event.type == pg.KEYDOWN:
            pg.draw.rect(disp, (255, 255, 255), (first_pos[0]*80+2, first_pos[1]*80+2, 76, 76))
            if event.key in [pg.K_UP,pg.K_w]:
                if first_pos[1] > 0 and maze[first_pos[1]-1][first_pos[0]] == 0:
                    first_pos[1] -= 1
            elif event.key in [pg.K_DOWN,pg.K_s]:
                if first_pos[1] < len(maze)-1 and maze[first_pos[1]+1][first_pos[0]] == 0:
                    first_pos[1] += 1
            elif event.key in [pg.K_LEFT,pg.K_a]:
                if first_pos[0] > 0 and maze[first_pos[1]][first_pos[0]-1] == 0:
                    first_pos[0] -= 1
            elif event.key in [pg.K_RIGHT,pg.K_d]:
                if first_pos[0] < len(maze[0])-1 and maze[first_pos[1]][first_pos[0]+1] == 0:
                    first_pos[0] += 1