import pyglet
from pyglet.gl import *
from pyglet.window import Window

pyglet.resource.path = ['resources']
pyglet.resource.reindex()
pyglet.resource.add_font('MONOFONT.TTF')


class GameWindow(Window):

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.title_label = pyglet.text.Label(text='Tetris',
                                             font_name='Monofonto',
                                             font_size=26,
                                             x=400, y=580,
                                             anchor_x='center',
                                             anchor_y='center',
                                             batch=self.batch)
        self.clock_display = pyglet.clock.ClockDisplay(color=(.8, .8, .8, .8))
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        pyglet.gl.glClearColor(0.2, 0.2, 0.2, 1.0)

    def on_draw(self):
        self.clear()
        self.draw_background()
        self.draw_block(160, 160, color=(0.5, 0.8, 0, 1))
        self.batch.draw()
        self.clock_display.draw()

    def update(self, delta):
        pass

    def draw_block(self, x, y, size=20, color=(1, 1, 1, 1)):
        colors = color * 4
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (x, y,
                                x+size, y,
                                x+size, y+size,
                                x, y+size)),
                       ('c4f', colors))

        dark_colors = tuple(map(lambda _c: _c*0.8, color)) * 4
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (x, y,
                                x+size, y,
                                x+size, y+size*0.1,
                                x, y+size*0.1)),
                       ('c4f', dark_colors))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (x+size*0.9, y,
                                x+size, y,
                                x+size, y+size,
                                x+size*0.9, y+size)),
                       ('c4f', dark_colors))

        light_colors = tuple(map(lambda _c: _c*1.2, color)) * 4
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (x, y,
                                x+size*0.1, y,
                                x+size*0.1, y+size,
                                x, y+size)),
                       ('c4f', light_colors))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (x, y+size*0.9,
                                x+size*0.9, y+size*0.9,
                                x+size*0.9, y+size,
                                x, y+size)),
                       ('c4f', light_colors))

    def draw_background(self):
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (120, 120,
                                110, 120,
                                110, 110,
                                120, 110)),
                       ('c4f', (1, 0, 0, 1,
                                0, 1, 0, 1,
                                0, 0, 1, 1,
                                1, 1, 1, 1)))
