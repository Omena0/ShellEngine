from shellEngine import *
import keyboard as kb
import random as r
import numpy as np
# ShellEngine: import time as t
# ShellEngine: from threading import Thread

# Maze solving example
# By Omena0

def createMaze(dim:int) -> list:
    # Create a grid filled with walls
    maze =np.ones((dim*2+1, dim*2+1))

    # Define the starting point
    x, y = (0, 0)
    maze[2*x+1, 2*y+1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        r.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] == 1:
                maze[2*nx+1, 2*ny+1] = 0
                maze[2*x+1+dx, 2*y+1+dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
            
    # Create an entrance and an exit
    maze[1, 0] = 0
    maze[-2, -1] = 0

    return maze.tolist()

c = True
last_size = os.get_terminal_size()

def keypress(key:kb.KeyboardEvent):
    global c, screen_height, last_size
    key = key.name
    if key == 'c':
        if c: c = False
        else: c = True
        return
    if os.get_terminal_size() != last_size:
        last_size = os.get_terminal_size()
        screen_height = os.get_terminal_size()[1]-2
        init()
        return
    if game.screen.splitlines()[-2][-1] == '$':
        init()
    t.sleep(r.randrange(1,100)/1000) # Make game inconsistent on purpose
    try:
        match key:
            case 'w':
                if c:
                    while True:
                        if game.screen.splitlines()[player.y-1][player.x] != colors[2]: return
                        player.sety(-1)
                else:
                    if game.screen.splitlines()[player.y-1][player.x] != colors[2]: return
                    player.sety(-1)
            case 'a': 
                if c:
                    while True:
                        if game.screen.splitlines()[player.y][player.x-1] != colors[2]: return
                        player.setx(-1)
                else:
                    for _ in range(2):
                        if game.screen.splitlines()[player.y][player.x-1] != colors[2]: return
                        player.setx(-1)
            case 's': 
                if c:
                    while True:
                        if game.screen.splitlines()[player.y+1][player.x] != colors[2]: return
                        player.sety(1)
                else:
                    if game.screen.splitlines()[player.y+1][player.x] != colors[2]: return
                    player.sety(1)
            case 'd': 
                if c:
                    while True:
                        if game.screen.splitlines()[player.y][player.x+1] != colors[2]: return
                        player.setx(1)
                else:
                    for _ in range(2):
                        if game.screen.splitlines()[player.y][player.x+1] != colors[2]: return
                        player.setx(1)
    except Exception: pass
    if key in {'w','a','s','d'}:
        game.changed = True

game = Game()
game.bgColor = colors[2]

maze = Sprite([['']])
maze.wall_physics = False

player = Sprite([['$']])
player.wall_physics = False

def init():
    os.system('cls')
    player.x = 0
    player.y = 1
    _maze = [str(i)\
        .replace('1.0',colors[4]*2).replace(' ','').replace('0.0',colors[2]*2).replace('[','').replace(']','').replace(',','')\
            for i in [i for i in createMaze(round(screen_height/2)-1)]]
    maze.texture = _maze
    maze.width   = len(_maze[0])
    maze.height  = len(_maze)
    game.geometry(maze.width,maze.height)
    game.changed = True

init()

kb.on_press(keypress)

game.run()