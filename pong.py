from shellEngine import *
from threading import Thread
import keyboard as kb
import os

os.system('cls')

game = Game()

game.bgColor = ' '

game._init_display()

paddle_texture = (
    ('#'),
    ('#'),
    ('#'),
    ('#'),
    ('#'),
    ('#')
)

paddle1 = Sprite(paddle_texture)
paddle2 = Sprite(paddle_texture)

paddle1.setx(2)
paddle2.setx(screen_width-7)

paddle1.sety(round(screen_height/2-3))
paddle2.sety(round(screen_height/2-3))

ball = Sprite((('#')))

ball.setx(round(screen_width/2))
ball.sety(round(screen_height/2))

def gameloop():
    while True:
        ...


def on_press(key):
    key = key.name
    if key == 'w':
        paddle1.sety(-2)
    if key == 's':
        paddle1.sety(2)
    if key == 'i':
        paddle2.sety(-2)
    if key == 'k':
        paddle2.sety(2)
    game.changed = True
    
kb.on_press(on_press,True)


game.run()