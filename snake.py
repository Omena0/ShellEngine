from threading import Thread
from shellEngine import *
import keyboard as kb
import random as r
import time as t

screen_width = 50
screen_height = 20

game = Game()
game.geometry(screen_width,screen_height)

print('Score: 0')

player = [Sprite([[block(3,'green'),block(3,'green')]])]
player[0].setx(20)
player[0].sety(10)
player[0].p = 0

length = 1

apple = []
for _ in range(2):
    a = Sprite([[block(3,'red'),block(3,'red')]])
    a.wall_physics = False
    apple.append(a)

def move_apple(num):
    apple[num].x = r.randint(0,(screen_width-1)//2)*2
    apple[num].y = r.randint(0,screen_height-1)
    apple[num].setx(0)
    apple[num].sety(0)
    game.changed = True

for i in range(len(apple)): move_apple(i)

def move(dir:int):
    global length, extratext
    positions = set()
    for i in player:
        i.p += 1
        if i.p > length:
            player.remove(i)
            sprites.remove(i)
            continue
        positions.add((i.x,i.y))
    
    # Player check
    if len(positions) < len(player):
        game.running = False
        print_('You Died!')
        return

    player.insert(0,Sprite([[block(3,'green'),block(3,'green')]]))
    player[0].p = 0

    if dir == 0: # up
        player[0].setx(player[1].x)
        player[0].sety(player[1].y-1)
    elif dir == 1: # left
        player[0].setx(player[1].x-2)
        player[0].sety(player[1].y)
    elif dir == 2: # down
        player[0].setx(player[1].x)
        player[0].sety(player[1].y+1)
    elif dir == 3: # right
        player[0].setx(player[1].x+2)
        player[0].sety(player[1].y)
    
    # Apple check
    for i,a in enumerate(apple):
        if (a.x,a.y) in positions:
            move_apple(i)
            print(f'Score: {length}')
            length += 1

queue = []
def on_press(key:kb.KeyboardEvent):
    global direction
    key = key.name
    if key == 'w':
        queue.append(0)
    elif key == 'a':
        queue.append(1)
    elif key == 's':
        queue.append(2)
    elif key == 'd':
        queue.append(3)
    
    elif key == 'q':
        game.running = False

direction = 0
last = 0
def gameloop():
    global last
    while game.running:
        start = t.perf_counter()
        if queue: last = queue.pop(0)
        move(last)
        game.changed = True
        end = t.perf_counter()
        duration = end-start
        t.sleep(max(max(0.2-length/120,0.1)-duration,0))

kb.on_press(on_press,True)

Thread(target=gameloop,daemon=True).start()

game.run()