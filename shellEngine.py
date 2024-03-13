import contextlib
import time as t
from threading import Thread
from math import ceil
from os import get_terminal_size, system

system('cls')

size = get_terminal_size()

screen_width = 100
screen_height = 20

colors = [' ','░','▒','▓','█']

cap_fps = False

extratext = ''

print_ = print

def print(*args):
    global extratext
    a = [f'{v}' for v in args]
    extratext = ' '.join(a)

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
        
        # Hitboxes (collision)
        self.xrange = self.get_xrange()
        self.yrange = self.get_yrange()
        
    def sety(self,y):
        y = ceil(y)
        if self.wall_physics and (self.y+y > screen_height or self.y+y+self.height > screen_height or self.y+y < 0):
            return
        self.y += y
        self.yrange = self.get_yrange()
        game.changed = True
        
    def setx(self,x):
        x = ceil(x)
        if self.wall_physics and (self.x+x > screen_width or self.x+x+self.width > screen_width or self.x+x < 0):
            return
        self.x += x
        self.xrange = self.get_xrange()
        game.changed = True
        
    def get_xrange(self):
        return range(round(self.x),round(self.x)+self.width)
    
    def get_yrange(self):
        return range(round(self.y),round(self.y)+self.height)
    
    def collides_with(self, *others):
        global extratext
        collisions = []
        for other in others:
            if other == 'edge':
                collisions.append((self.x <= 0 or self.y <= 0) or (self.x+self.width >= screen_width or self.y+self.height >= screen_height))
            else:
                self.setx(0)
                other.setx(0)
                if set(self.xrange) & set(other.xrange) and any(set(self.yrange) & set(other.yrange)):
                    collisions.append(True)
        return any(collisions)
        
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
        self.bgColor = colors[1]
        self._init_display()
        self.running = True
        
    def _init_display(self):
        self.screen = ''
        for _ in range(screen_height):
            for _ in range(screen_width):
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
        color = self.bgColor
        for sprite in sprites:
            if x in sprite.xrange and y in sprite.yrange:
                with contextlib.suppress(Exception):
                    if sprite.texture[y-sprite.y][x-sprite.x] != self.bgColor:
                        color = sprite.texture[y-sprite.y][x-sprite.x]
        return color
    
    def update_display(self):
        print_(back(screen_height+100),end='')
        print('\n'*round(size.lines/8))
        print_(f'FPS: {self.fps:<3} TICK: {self.tick:<10} FRAME: {self.frame:<10} TICK TIME: {self.mspt:<10} {extratext:<10}')
        print_(self.screen,end='')
        self.tick += 1
        
    def run(self):
        global screen_height
        Thread(target=self.loop,daemon=True).start()
        while self.running:
            start = t.perf_counter()
            self.update_display()
            self.screen_renderer()
            end = t.perf_counter()
            # tick time calc
            duration = (end - start)
            self.tick_time = round(duration,5)
            self.mspt_list.append(duration)
            if len(self.mspt_list) > 25: self.mspt_list.pop(1)
            self.mspt = sum(self.mspt_list)/len(self.mspt_list)
            with contextlib.suppress(Exception):
                if cap_fps: t.sleep(0.01 - duration)
            
    def loop(self):
        loop = 0
        while self.running:
            start = t.perf_counter()

            self.fps_list.append(self.fps_per_sec)
            self.fps_per_sec = 0
            self.fps = round(sum(self.fps_list)/len(self.fps_list),2)
            if len(self.fps_list) > 25: self.fps_list.pop(1)
            
            end = t.perf_counter()
            t.sleep(0.1-(end-start))
            loop += 1
    
    def geometry(self,width:int,height:int) -> None:
        global screen_width, screen_height
        screen_width = width
        screen_height = height
        #self._init_display()
        #self.changed = True

if __name__ == '__main__':
    import pong
