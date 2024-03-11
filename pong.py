from shellEngine import *
from threading import Thread
import keyboard as kb
import os


os.system('cls')

screen_width = 225
screen_height = 30

game = Game()
game.geometry(screen_width,screen_height)

game.bgColor = colors[1]

paddle_texture = []
for i in range(round(screen_height/5)):
    paddle_texture.append(('#','#'))


paddle1 = Sprite(paddle_texture)
paddle2 = Sprite(paddle_texture)

paddle1.width = 2
paddle2.width = 2

paddle1.setx(2)
paddle2.setx(screen_width-7)

paddle1.sety(round(screen_height/2-3))
paddle2.sety(round(screen_height/2-3))

ball = Sprite((('@','@','@'),('@','@','@')))

ball.wall_physics = False

ball.velocity = [4,1]

ball.setx(round(screen_width/2))
ball.sety(round(screen_height/2))

score_display = Sprite(['0'])
score_display.setx(screen_width/2)
score_display.sety(screen_height/2)

def gameloop():
    score = 0
    while True:
        t.sleep(0.1)
        ball.setx(ball.velocity[0])
        ball.sety(ball.velocity[1])
        if ball.collides_with(paddle1,paddle2):
            ball.velocity = -ball.velocity[0], ball.velocity[1]
            score += 1
            score_display.texture = [str(score)]
            print(f'Score: {score}')
        elif ball.collides_with('edge'):
            ball.velocity = ball.velocity[0], -ball.velocity[1]
            ball.setx(ball.velocity[0]//2)
            ball.sety(ball.velocity[1]//2)
        
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
    if key == 'w':
        paddle1.sety(-sens)
    if key == 's':
        paddle1.sety(sens)
    if key == 'ylänuoli':
        paddle2.sety(-sens)
    if key == 'alanuoli':
        paddle2.sety(sens)
    game.changed = True
    
kb.on_press(on_press,True)

Thread(target=gameloop).start()

game.run()

os.system('cls')