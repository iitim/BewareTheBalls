import arcade
from Models import World, Bar
 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()

#################### MAIN SCREEN ####################
        
class BewareTheBalls(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(width, height)
        self.setup()

    def setup(self) :
        self.ball_sprite = [ModelSprite('images/ball.png',model=self.world.ball[0])]
        self.bar_sprite = []
        self.bar_sprite.append(ModelSprite('images/bar_H.png',model=self.world.bar[0]))
        self.bar_sprite.append(ModelSprite('images/bar_V.png',model=self.world.bar[1]))
        self.bar_sprite.append(ModelSprite('images/bar_H.png',model=self.world.bar[2]))
        self.bar_sprite.append(ModelSprite('images/bar_V.png',model=self.world.bar[3]))

    def add_ball_sprite(self) :
        if not self.world.game_over :
            if len(self.world.ball) >len(self.ball_sprite):
                self.ball_sprite.append(ModelSprite('images/ball.png',model=self.world.ball[len(self.world.ball)-1]))
 
    def on_draw(self):
        arcade.start_render()
        if self.world.game_over :
            arcade.draw_text("You can save the balls for " + str(self.world.timer_thread.timer) + " seconds",
                                130, self.height/2 + 30,
                                arcade.color.BLACK, 20)
            arcade.draw_text("Press ENTER to restart",
                                130, self.height/2 - 30,
                                arcade.color.BLACK, 30)
        else :
            for each_ball_sprite in self.ball_sprite :
                each_ball_sprite.draw()
            for each_bar_sprite in  self.bar_sprite :
                each_bar_sprite.draw()

            arcade.draw_text(str(self.world.timer_thread.timer),
                             self.width - 30, self.height - 30,
                             arcade.color.RED, 20)
        
 
    def animate(self, delta):
        if not self.world.game_over :
            self.add_ball_sprite()
            self.world.animate(delta)

    def on_key_press(self, key, key_modifiers):
        if self.world.game_over and key == arcade.key.ENTER :
            self.world.setup()
            self.setup()
            self.world.game_over = False
        elif not self.world.game_over :
            self.world.on_key_press(key, key_modifiers)

    def get_max_time(self) :
        if self.world.game_over :
            return self.world.timer_thread.timer


#################### START ####################
            
 
if __name__ == '__main__':
    window = BewareTheBalls(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
