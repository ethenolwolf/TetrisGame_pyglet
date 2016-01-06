import pyglet
from pyglet.window import Window


class GameWindow(Window):

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.clock_display = pyglet.clock.ClockDisplay(color=(.8, .8, .8, .8))
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        pyglet.gl.glClearColor(0.2, 0.2, 0.2, 1.0)

    def on_draw(self):
        self.clear()
        self.clock_display.draw()

    def update(self, delta):
        pass
