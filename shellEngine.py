from os import get_terminal_size, system
from termcolor import colored
from threading import Thread
from math import ceil
import contextlib
import time as t
import sys

system('cls')

size = get_terminal_size()

screen_width = 100
screen_height = 20

blocks = [' ','░','▒','▓','█']

cap_fps = False

extratext = ''

print_ = sys.stdout.write

def print(*args):
    global extratext
    a = [f'{v}' for v in args]
    extratext = ' '.join(a)

def back(num:int=1):return f'\x1b[{num}A'

def block(thickness,*args, **kwargs) -> str:
    if args or kwargs:
        return colored(blocks[thickness],*args,**kwargs)
    else:
        return blocks[thickness]

class Sprite:
    def __init__(self,texture:list):
        self.x = 0
        self.y = 0
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
        return set(range(round(self.x),round(self.x)+self.width))

    def get_yrange(self):
        return set(range(round(self.y),round(self.y)+self.height))

    def collides_with(self, *others):
        for other in others:
            if other == 'edge':
                collides = (self.x <= 0 or self.y <= 0) or (self.x+self.width >= screen_width or self.y+self.height >= screen_height)
                if collides: return True

            elif any(self.xrange & other.xrange) and any(self.yrange & other.yrange):
                return True

sprites:set[Sprite] = set()

class Game:
    def __init__(self):
        global game
        game = self
        self.screen = ''
        self.frame = 0
        self.fps = 0
        self.fps_ = 0
        self.fps_list = []
        self.changed = True
        self.bgColor = block(4,'black')
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
        self.fps_ += 1
        if not self.changed: return
        self.screen = ''
        for y in range(screen_height):
            for x in range(screen_width):
                color = self.shader(x,y)
                self.screen += color
            self.screen += '\n'

    def shader(self,x,y):
        for sprite in sprites:
            if x in sprite.xrange and y in sprite.yrange:
                with contextlib.suppress(Exception):
                    return sprite.texture[y-sprite.y][x-sprite.x]
        return self.bgColor

    def run(self):
        global screen_height, extratext
        Thread(target=self.fps_thread).start()
        while self.running:
            # Render
            start = t.perf_counter()
            self.screen_renderer()
            end = t.perf_counter()
            print((end-start)*1000)

            # Update screen
            self.changed = False
            print_(back(screen_height*10))
            print_(f'\rFPS: {self.fps:<5} FRAME: {self.frame:<10} {extratext}\n\r')
            print_(self.screen)
            sys.stdout.flush()

    def fps_thread(self):
        while self.running:
            start = t.perf_counter()

            self.fps_list.append(self.fps_)
            self.fps_ = 0
            self.fps = round(sum(self.fps_list)/len(self.fps_list),2)
            if len(self.fps_list) > 25: self.fps_list.pop(1)

            end = t.perf_counter()
            with contextlib.suppress(Exception):
                t.sleep(1-(end-start))

    def geometry(self,width:int,height:int) -> None:
        global screen_width, screen_height
        screen_width = width
        screen_height = height
        self._init_display()
        self.changed = True

