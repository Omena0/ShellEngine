import keyboard as kb
import time as t
import random as r
from threading import Thread

lines = 15

colors = [' ','░','▒','▓','█']

sprites = []

def back(num:int=1):
    """Return char to go back lines in terminal

    Args:
        num (int): Num of lines. Defaults to 1.

    Returns:
        str: Char
    """
    return f'\x1b[{num}A'

class Sprite:
    def __init__(self,width:int,height:int,texture:list):
        self.x = 10
        self.y = 10
        self.width   = width
        self.height  = height
        self.texture = texture
        self.speed = 2
        sprites.append(self)

class Game:
    def __init__(self):
        self.screen = ''
        self.frame = 0
        self.screen_frame=0
        self.fps = 0
        self.fps_per_sec = 0
        self.fps_list = []
        self.tick_time = 0
        self.mspt = 0
        self.mspt_list = []
        self._init_display()
        kb.on_press(self.kb)
        
    def _init_display(self):
        self.screen = ''
        for i in range(lines):
            for i in range(100):
                self.screen += ''
            self.screen += '\n'
    
    def screen_renderer(self):
        self.screen = ''
        for y in range(lines):
            for x in range(100):
                # Rendering code and shit
                color = self.render(x,y)
                self.screen += color
            self.screen += '\n'
        self.frame += 1
        self.fps_per_sec += 1
        
    def render(self,x,y):
        color = colors[1]
        for sprite in sprites:
            xrange = range(sprite.x, sprite.x+sprite.width)
            yrange = range(sprite.y, sprite.y+sprite.height)
            if x in xrange:
                if y in yrange:
                    color = sprite.texture[y-sprite.y-1][x-sprite.x-1]
        return color
    
    def update_display(self):
        print(back(lines+10),end='')
        print(f'FPS: {self.fps:2<} FRAME: {self.screen_frame} RENDER_FRAME: {self.frame} MSPT: {self.mspt}')
        self.screen_renderer()
        print('\n'+self.screen,end='')
        self.screen_frame += 1
        
    def run(self):
        global lines
        render = True
        Thread(target=self.loop,daemon=True).start()
        while True:
            start = t.time_ns()
            if render: self.update_display()
            end = t.time_ns()
            # MSPT CALC
            duration = (end - start)/1_000_000_000
            self.tick_time = duration
            self.mspt_list.append(duration)
            if len(self.mspt_list) > 100: self.mspt_list.pop(1)
            self.mspt = sum(self.mspt_list)/len(self.mspt_list)
            try:
                #t.sleep(0 - duration)
                render = True
            except: render = False
            
    def loop(self):
        while True:
            start = t.time()

            self.fps_list.append(self.fps_per_sec)
            self.fps_per_sec = 0
            self.fps = round(sum(self.fps_list)/len(self.fps_list),2)
            if len(self.fps_list) > 100: self.fps_list.pop(1)

            end = t.time()
            t.sleep(0.1-(end-start))
            
    def kb(self,char:kb.KeyboardEvent):
        char = char.name
        if char == 'w':
            test.y -= test.speed
        if char == 'a':
            test.x -= test.speed*2
        if char == 's':
            test.y += test.speed
        if char == 'd':
            test.x += test.speed*2
        

print('\n'*50)

a = Game()

texture = [
    ['aa'],
    ['bb']
]

test = Sprite(2,2,texture)

a.run()


    
    