from shellEngine import *

import os
import sys
import random as r
import keyboard as kb
import time as t
from threading import Thread

# Flappy bird example using shellEngine
# Example by Omena0

game = Game()

cap_fps = False

def gameloop():
    loop = 0
    while True:
        player.sety(1)
        
        for pillar in pillars:
            pillar.setx(-1)

            if player.x in pillar.xrange() and player.y in pillar.yrange():
                if player.y in range(pillar.y+22,pillar.y+27): pass
                else:
                    game.screen = '\n'*screen_height
                    sys.tracebacklimit = -100
                    print('!!! You died! Killing program.. !!!'+' '*100)
                    while True:
                        os.kill(0,0)
                    
                    

            if pillar.x < -5:
                pillar.x = screen_width
                pillar.y = r.randrange(10)-20
        
        t.sleep(0.16)
        loop += 1

def on_press(char:kb.KeyboardEvent):
    char = char.name
    a.changed = True
    if char == 'w':
        Thread(target=jump,daemon=True).start()

def jump():
    for i in range(round(screen_height/4)):
        player.sety(-1)
        t.sleep(0.15*(i/5))
    
print('\n'*50)

a = Game()

player_texture = [
    colors[3]*3,
    colors[3]*3
]

pillar_texture = []

for i in range(round(screen_height)):
    pillar_texture.append(colors[1]+colors[3]*4+colors[1])
    
pillar_texture.append(colors[4]*6)
for i in range(round(screen_height/4)+1):
    pillar_texture.append(colors[1]*6)
pillar_texture.append(colors[4]*6)

for i in range(round(screen_height)):
    pillar_texture.append(colors[1]+colors[3]*4+colors[1])


pillars = []

for i in range(5):
    i += 1
    pillar = Sprite(pillar_texture)

    pillar.x = 20*i+20
    pillar.y = r.randrange(10)-20
    pillar.wall_physics = False
    pillars.append(pillar)

player = Sprite(player_texture)

player.x = 15

kb.on_press(on_press)

Thread(target=gameloop,daemon=True).start()

a.run()


    