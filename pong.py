from shellEngine import *
from threading import Thread
import keyboard as kb
import random as r
import os


screen_width = 100
screen_height = 20

game = Game()
game.geometry(screen_width,screen_height)

texture = [
    [
        block(4,'white')
    ] for _ in range(round(screen_height/5))
]

paddle1 = Sprite(texture)
paddle2 = Sprite(texture)

paddle1.setx(2)
paddle2.setx(screen_width-7)

paddle1.sety(round(screen_height/2-3))
paddle2.sety(round(screen_height/2-3))

ball = Sprite((
    (
        block(4,'red'),
        block(4,'red'),
        block(4,'red')
    ),
    (
        block(4,'red'),
        block(4,'red'),
        block(4,'red')
    )
))

ball.wall_physics = False

ball.velocity = r.choice([[4,1],[4,-1],[-4,1],[-4,-1]])

ball.setx(round(screen_width//2))
ball.sety(round(screen_height//2))

def gameloop():  # sourcery skip: extract-duplicate-method
    score = 0
    while True:
        delay = round(0.1*(150-score)/100,4)
        if score: t.sleep(delay)
        else: t.sleep(0.2)
        print(f'Score: {score} Speed: {delay}')
        ball.setx(ball.velocity[0]//2)
        ball.sety(ball.velocity[1])

        if ball.collides_with(paddle1,paddle2):
            ball.velocity = -ball.velocity[0], ball.velocity[1]
            score += 1

        elif ball.y+ball.height >= screen_height or ball.y < 0:
            ball.velocity = ball.velocity[0], -ball.velocity[1]
            ball.setx(ball.velocity[0]//2)
            ball.sety(ball.velocity[1])
        
        ball.setx(ball.velocity[0]//2)
        
        if ball.collides_with(paddle1,paddle2):
            ball.velocity = -ball.velocity[0], ball.velocity[1]
            score += 1

        elif ball.y+ball.height >= screen_height or ball.y < 0:
            ball.velocity = ball.velocity[0], -ball.velocity[1]
            ball.setx(ball.velocity[0]//2)
            ball.sety(ball.velocity[1])
        
        if ball.x < 0:
            game.running = False
            os.system('cls')
            t.sleep(0.1)
            print_('\nPLAYER 2 WINS\n')
            break
        elif ball.x > screen_width:
            game.running = False
            os.system('cls')
            t.sleep(0.1)
            print_('\nPLAYER 1 WINS\n')
            break

sens = 3

def on_press(key):
    key = key.name
    for _ in range(sens):
        if key == 'w':
            paddle1.sety(-1)
        elif key == 's':
            paddle1.sety(1)
        elif key == 'ylänuoli':
            paddle2.sety(-1)
        elif key == 'alanuoli':
            paddle2.sety(1)
    game.changed = True
    
kb.on_press(on_press,True)

Thread(target=gameloop,daemon=True).start()

game.run()