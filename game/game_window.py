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
                                             x=self.width/2, y=self.height-20,
                                             anchor_x='center',
                                             anchor_y='center',
                                             batch=self.batch)

        self.block_size = self.width / 40
        font = pyglet.font.load(name='Monofonto', size=16)
        self.clock_display = pyglet.clock.ClockDisplay(font=font,
                                                       color=(.8, .8, .8, .8))
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        pyglet.gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        self.make_background()

    def on_draw(self):
        self.clear()
        self.draw_block(160, 160, color=(0.5, 0.8, 0, 1))
        self.batch.draw()
        self.clock_display.draw()

    def update(self, delta):
        pass

    def draw_block(self, x, y, color=(1, 1, 1, 1)):
        size = self.block_size
        colors = color * 4
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x, y,
                                      x+size, y,
                                      x+size, y+size,
                                      x, y+size)),
                             ('c4f', colors))

        dark_colors = tuple(map(lambda _c: _c*0.8, color)) * 4
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x, y,
                                      x+size, y,
                                      x+size, y+size*0.1,
                                      x, y+size*0.1)),
                             ('c4f', dark_colors))
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x+size*0.9, y,
                                      x+size, y,
                                      x+size, y+size,
                                      x+size*0.9, y+size)),
                             ('c4f', dark_colors))

        light_colors = tuple(map(lambda _c: _c*1.2, color)) * 4
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x, y,
                                      x+size*0.1, y,
                                      x+size*0.1, y+size,
                                      x, y+size)),
                             ('c4f', light_colors))
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x, y+size*0.9,
                                      x+size*0.9, y+size*0.9,
                                      x+size*0.9, y+size,
                                      x, y+size)),
                             ('c4f', light_colors))

    def make_background(self):
        left = self.width / 2 - self.block_size * 6
        right = self.width / 2 + self.block_size * 6
        bottom = self.height / 2 - self.block_size * 11
        top = self.height / 2 + self.block_size * 11

        color = (0.5, 0.5, 0.5, 1) * 4
        dark_color = (0.4, 0.4, 0.4, 1) * 4
        light_color = (0.6, 0.6, 0.6, 1) * 4

        # left wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                left+self.block_size, bottom,
                                left+self.block_size, top,
                                left, top)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                left+self.block_size, bottom,
                                left+self.block_size, bottom+self.block_size*0.1,
                                left, bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left+self.block_size*0.9, bottom,
                                left+self.block_size, bottom,
                                left+self.block_size, top,
                                left+self.block_size*0.9, top)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, top-self.block_size*0.1,
                                left+self.block_size, top-self.block_size*0.1,
                                left+self.block_size, top,
                                left, top)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                left+self.block_size*0.1, bottom,
                                left+self.block_size*0.1, top,
                                left, top)),
                       ('c4f', light_color))

        # right wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size, bottom,
                                right, bottom,
                                right, top,
                                right-self.block_size, top)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size, bottom,
                                right, bottom,
                                right, bottom+self.block_size*0.1,
                                right-self.block_size, bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size*0.1, bottom,
                                right, bottom,
                                right, top,
                                right-self.block_size*0.1, top)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size, top-self.block_size*0.1,
                                right, top-self.block_size*0.1,
                                right, top,
                                right-self.block_size, top)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size, bottom,
                                right-self.block_size*0.9, bottom,
                                right-self.block_size*0.9, top,
                                right-self.block_size, top)),
                       ('c4f', light_color))

        # bottom wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                right, bottom,
                                right, bottom+self.block_size,
                                left, bottom+self.block_size)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                right, bottom,
                                right, bottom+self.block_size*0.1,
                                left, bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (right-self.block_size*0.1, bottom,
                                right, bottom,
                                right, bottom+self.block_size,
                                right-self.block_size*0.1, bottom+self.block_size)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left+self.block_size*0.9, bottom+self.block_size*0.9,
                                right-self.block_size*0.9, bottom+self.block_size*0.9,
                                right-self.block_size*0.9, bottom+self.block_size,
                                left+self.block_size*0.9, bottom+self.block_size)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (left, bottom,
                                left+self.block_size*0.1, bottom,
                                left+self.block_size*0.1, bottom+self.block_size,
                                left, bottom+self.block_size)),
                       ('c4f', light_color))
