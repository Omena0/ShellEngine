import time as t
from threading import Thread

screen_height = 20
screen_width = 100

colors = [' ','░','▒','▓','█']

cap_fps = False

def back(num:int=1):return f'\x1b[{num}A'

class Sprite:
    def __init__(self,texture:list):
        self.x = 2
        self.y = 2
        self.width   = len(texture[0])
        self.height  = len(texture)
        self.texture = texture
        self.wall_physics = True
        sprites.add(self)
        
    def sety(self,y):
        if self.wall_physics:
            if self.y+y > screen_height or self.y+y+self.height > screen_height or self.y+y < 0:
                return
        self.y += y
        game.changed = True
        
    def setx(self,x):
        if self.wall_physics:
            if self.x+x > screen_width or self.x+x+self.width > screen_width or self.x+x < 0:
                return
        self.x += x
        game.changed = True
        
    def checkCollision(self,x:int,y:int) -> bool:
        return x in range(self.x,self.x+self.width) and y in range(self.y,self.y+self.height)

sprites:set[Sprite] = set()

class Game:
    def __init__(self):
        global game
        game = self
        self.screen = ''
        self.frame = 0
        self.tick=0
        self.fps = 0
        self.fps_per_sec = 0
        self.fps_list = []
        self.tick_time = 0
        self.mspt = 0
        self.mspt_list = []
        self.changed = True
        self._init_display()
        
    def _init_display(self):
        self.screen = ''
        for i in range(screen_height):
            for i in range(screen_width):
                self.screen += ''
            self.screen += '\n'
    
    def screen_renderer(self):
        self.frame += 1
        self.fps_per_sec += 1
        if not self.changed: return
        self.changed = False
        self.screen = ''
        for y in range(screen_height):
            for x in range(screen_width):
                color = self.render(x,y)
                self.screen += color
            self.screen += '\n'
        
    def render(self,x,y):
        color = colors[1]
        for sprite in sprites:
            if sprite.checkCollision(x,y):
                try: color = sprite.texture[y-sprite.y][x-sprite.x]
                except: pass
        return color
    
    def update_display(self):
        print(back(screen_height+10),end='')
        print(f'FPS: {self.fps:2<} TICK: {self.tick} FRAME: {self.frame} TICK TIME: {self.mspt}')
        print(self.screen,end='')
        self.tick += 1
        
    def run(self):
        global screen_height
        Thread(target=self.loop,daemon=True).start()
        while True:
            start = t.perf_counter()
            self.update_display()
            self.screen_renderer()
            end = t.perf_counter()
            # tick time calc
            duration = (end - start)
            self.tick_time = duration
            self.mspt_list.append(duration)
            if len(self.mspt_list) > 25: self.mspt_list.pop(1)
            self.mspt = sum(self.mspt_list)/len(self.mspt_list)
            try:
                if cap_fps: t.sleep(0.01 - duration)
            except: pass
            
    def loop(self):
        loop = 0
        while True:
            start = t.perf_counter()

            self.fps_list.append(self.fps_per_sec)
            self.fps_per_sec = 0
            self.fps = round(sum(self.fps_list)/len(self.fps_list),2)
            if len(self.fps_list) > 25: self.fps_list.pop(1)
            
            end = t.perf_counter()
            t.sleep(0.1-(end-start))
            loop += 1

