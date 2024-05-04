from shellEngine import *
import keyboard as kb
import random as r

screen_width = 40
screen_height = 20

game = Game()
game.geometry(screen_width,screen_height)

player = []
player.append(Sprite([[block(3,'green'),block(3,'green')]]))
player[0].setx(20)
player[0].sety(10)
player[0].p = 0

length = 1

apple = []
for i in range(2):
    a = Sprite([[block(3,'red'),block(3,'red')]])
    a.wall_physics = False
    apple.append(a)

def move_apple(num):
    apple[num].x = r.randint(0,screen_width//2)*2
    apple[num].y = r.randint(0,screen_height)
    apple[num].setx(0)
    apple[num].sety(0)
    game.changed = True

for i in range(len(apple)): move_apple(i)

def move(dir:int):
    global length
    positions = set()
    for i in player:
        i.p += 1
        if i.p > length:
            player.remove(i)
            sprites.remove(i)
            del i
            continue
        positions.add((i.x,i.y))
    
    if len(positions) < len(player):
        game.running = False
        print_('You Died!')
        return

    player.insert(0,Sprite([[block(3,'green'),block(3,'green')]]))
    player[0].p = 0

    if dir == 0: # up
        player[0].setx(player[1].x)
        player[0].sety(player[1].y-1)
    if dir == 1: # left
        player[0].setx(player[1].x-2)
        player[0].sety(player[1].y)
    if dir == 2: # down
        player[0].setx(player[1].x)
        player[0].sety(player[1].y+1)
    if dir == 3: # right
        player[0].setx(player[1].x+2)
        player[0].sety(player[1].y)
    
    for i,a in enumerate(apple):
        if a.x == player[0].x and a.y == player[0].y:
            move_apple(i)
            length += 1

def on_press(key:kb.KeyboardEvent):
    key = key.name
    if key == 'w':
        move(0)
        game.changed = True
    elif key == 'a':
        move(1)
        game.changed = True
    elif key == 's':
        move(2)
        game.changed = True
    elif key == 'd':
        move(3)
        game.changed = True
    
    elif key == 'q':
        game.running = False

kb.on_press(on_press,True)

game.run()