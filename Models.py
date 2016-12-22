import arcade
import time
import math
from threading import Timer,Thread,Event
from random import randint

class Model:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def hit(self, other, hit_size_width, hit_size_height, bar_dir):
        if bar_dir == Bar.DIR_HORIZON :
            return (abs(self.x - other.x) <= hit_size_width) and (abs(self.y - other.y) <= hit_size_height)
        elif bar_dir == Bar.DIR_VERTICAL :
            return (abs(self.x - other.x) <= hit_size_height) and (abs(self.y - other.y) <= hit_size_width)

        
class Bar(Model):
    DIR_VERTICAL = 0
    DIR_HORIZON = 1
    MOVE_LESS = 0
    MOVE_MORE = 1
    BAR_WIDTH = 284
    BAR_HEIGHT = 22
    def __init__(self, world, major_var, direction):
        self.major_var = major_var
        self.minor_var = 100
        self.direction = direction
        if self.direction == Bar.DIR_VERTICAL :
            super().__init__(world, self.major_var, self.minor_var)
            self.distance = self.world.height
        elif self.direction == Bar.DIR_HORIZON :
            super().__init__(world, self.minor_var, self.major_var)
            self.distance = self.world.width
 
    def animate(self, delta):
        self.set_point()
        if self.minor_var >= self.distance - Bar.BAR_WIDTH/2 :
            self.minor_var = self.distance - Bar.BAR_WIDTH/2
        elif self.minor_var <= 0 :
            self.minor_var = 0

    def set_point(self) :
        if self.direction == Bar.DIR_VERTICAL :
            self.x = self.major_var
            self.y = self.minor_var
        elif self.direction == Bar.DIR_HORIZON :
            self.x = self.minor_var
            self.y = self.major_var
            
    def control(self, move_key) :
        if move_key == Bar.MOVE_LESS :
            self.minor_var -= 50
        elif move_key == Bar.MOVE_MORE :
            self.minor_var += 50


class Ball(Model):
    DIR_LEFT = -1
    DIR_RIGHT = 1
    DIR_UP = 1
    DIR_DOWN = -1
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.vx = randint(1, 3)
        self.vy = randint(1, 3)
        self.out = False
        self.dirx = self.random_dir()
        self.diry = self.random_dir()

    def random_dir(self) :
        a = randint(0,2)
        if a == 0 :
            return -1
        return a
    
    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height -1 )

    def animate(self):
        if (self.x > self.world.width) or (self.y > self.world.height) or (self.x < 0) or (self.y < 0):
            self.out = True
        self.x += self.vx
        self.y += self.vy

    def after_hit(self, bar_dir) :
        if bar_dir == Bar.DIR_HORIZON :
            self.vy *= -1
        elif bar_dir == Bar.DIR_VERTICAL :
            self.vx *= -1

        
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.setup()

    def setup(self) :
        self.bar_edge = 10
        self.bar = [Bar(self, self.bar_edge, Bar.DIR_HORIZON),Bar(self, self.bar_edge, Bar.DIR_VERTICAL), Bar(self, self.height - self.bar_edge, Bar.DIR_HORIZON), Bar(self, self.width - self.bar_edge, Bar.DIR_VERTICAL)]
        self.ball = [Ball(self, 400, 400)]
        self.timer_thread = perpetualTimer(1.0, 0)
        self.timer_thread.start()
        self.one_ball_gen = True
        self.game_over = False
        
    def animate(self, delta):
        self.gen_ball()
        for each_ball in self.ball :
            each_ball.animate()
            if each_ball.out :
                del each_ball
                self.game_over = True
                self.timer_thread.cancel()
        for each_bar in self.bar :
            each_bar.animate(delta)
            for each_ball in self.ball :
                if each_bar.hit(each_ball, Bar.BAR_WIDTH/2, Bar.BAR_HEIGHT, each_bar.direction):
                    each_ball.after_hit(each_bar.direction)

    def gen_ball(self):
        if (self.timer_thread.timer % 5 == 0) and self.one_ball_gen :
            self.ball.append(Ball(self, 400, 400))
            self.one_ball_gen = False
        elif (self.timer_thread.timer % 5 == 1) :
            self.one_ball_gen = True

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.S :
            self.bar[0].control(Bar.MOVE_LESS)
        elif key == arcade.key.D :
            self.bar[0].control(Bar.MOVE_MORE)
        elif key == arcade.key.A :
            self.bar[1].control(Bar.MOVE_LESS)
        elif key == arcade.key.Q :
            self.bar[1].control(Bar.MOVE_MORE)
        elif key == arcade.key.W :
            self.bar[2].control(Bar.MOVE_LESS)
        elif key == arcade.key.E :
            self.bar[2].control(Bar.MOVE_MORE)
        elif key == arcade.key.F :
            self.bar[3].control(Bar.MOVE_LESS)
        elif key == arcade.key.R :
            self.bar[3].control(Bar.MOVE_MORE)

class perpetualTimer():
   def __init__(self,t,my_timer):
      self.t=t
      self.timer = my_timer
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.timer += 1
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()
