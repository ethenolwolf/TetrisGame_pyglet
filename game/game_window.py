import pyglet
from pyglet.gl import *
from pyglet.window import Window

pyglet.resource.path = ['resources']
pyglet.resource.reindex()
pyglet.resource.add_font('MONOFONT.TTF')


WHITE = (0.9, 0.9, 0.9, 1.0)
BLACK = (0.2, 0.2, 0.2, 1.0)
RED = (1.0, 0.5, 0.5, 1.0)
GREEN = (0.5, 1.0, 0.5, 1.0)
BLUE = (0.5, 0.5, 1.0, 1.0)
YELLOW = (0.8, 0.8, 0.5, 1.0)
GREY = (0.7, 0.7, 0.7, 1.0)
DARK_GREY = (0.5, 0.5, 0.5, 1.0)


def int_color(float_color):
    return tuple(map(lambda c: int(c*255), float_color))


def lighten_color(float_color):
    return tuple(map(lambda c: c*1.2, float_color))


def darken_color(float_color):
    return tuple(map(lambda c: c*0.8, float_color))


class GameWindow(Window):

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.title_label = pyglet.text.Label(text='Tetris',
                                             font_name='Monofonto',
                                             font_size=26,
                                             color=int_color(WHITE),
                                             x=self.width/2, y=self.height-20,
                                             anchor_x='center',
                                             anchor_y='center',
                                             batch=self.batch)

        self.block_size = self.width / 40
        # board info
        self.left = self.width / 2 - self.block_size * 6
        self.right = self.width / 2 + self.block_size * 6
        self.bottom = self.height / 2 - self.block_size * 11
        self.top = self.height / 2 + self.block_size * 11

        font = pyglet.font.load(name='Monofonto', size=16)
        self.clock_display = pyglet.clock.ClockDisplay(font=font,
                                                       color=(.8, .8, .8, .8))
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        pyglet.gl.glClearColor(*BLACK)
        self.make_background()

    def update_board_info(self, width, height):
        self.width = width
        self.height = height
        self.block_size = width / 40
        self.left = self.width / 2 - self.block_size * 6
        self.right = self.width / 2 + self.block_size * 6
        self.bottom = self.height / 2 - self.block_size * 11
        self.top = self.height / 2 + self.block_size * 11

    def on_draw(self):
        self.clear()
        self.draw_block(1, 1, color=RED)
        self.batch.draw()
        self.clock_display.draw()

    def update(self, delta):
        pass

    def draw_block(self, pos_x, pos_y, color=WHITE):
        size = self.block_size
        x = self.left + (pos_x + 1) * size
        y = self.bottom + (pos_y + 1) * size
        colors = color * 4
        dark_colors = darken_color(color) * 4
        light_colors = lighten_color(color) * 4

        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', (x, y,
                                      x+size, y,
                                      x+size, y+size,
                                      x, y+size)),
                             ('c4f', colors))
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
        color = DARK_GREY * 4
        dark_color = darken_color(DARK_GREY) * 4
        light_color = lighten_color(DARK_GREY) * 4

        # left wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.left+self.block_size, self.bottom,
                                self.left+self.block_size, self.top,
                                self.left, self.top)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.left+self.block_size, self.bottom,
                                self.left+self.block_size, self.bottom+self.block_size*0.1,
                                self.left, self.bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left+self.block_size*0.9, self.bottom,
                                self.left+self.block_size, self.bottom,
                                self.left+self.block_size, self.top,
                                self.left+self.block_size*0.9, self.top)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.top-self.block_size*0.1,
                                self.left+self.block_size, self.top-self.block_size*0.1,
                                self.left+self.block_size, self.top,
                                self.left, self.top)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.left+self.block_size*0.1, self.bottom,
                                self.left+self.block_size*0.1, self.top,
                                self.left, self.top)),
                       ('c4f', light_color))

        # right wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size, self.bottom,
                                self.right, self.bottom,
                                self.right, self.top,
                                self.right-self.block_size, self.top)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size, self.bottom,
                                self.right, self.bottom,
                                self.right, self.bottom+self.block_size*0.1,
                                self.right-self.block_size, self.bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size*0.1, self.bottom,
                                self.right, self.bottom,
                                self.right, self.top,
                                self.right-self.block_size*0.1, self.top)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size, self.top-self.block_size*0.1,
                                self.right, self.top-self.block_size*0.1,
                                self.right, self.top,
                                self.right-self.block_size, self.top)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size, self.bottom,
                                self.right-self.block_size*0.9, self.bottom,
                                self.right-self.block_size*0.9, self.top,
                                self.right-self.block_size, self.top)),
                       ('c4f', light_color))

        # bottom wall
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.right, self.bottom,
                                self.right, self.bottom+self.block_size,
                                self.left, self.bottom+self.block_size)),
                       ('c4f', color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.right, self.bottom,
                                self.right, self.bottom+self.block_size*0.1,
                                self.left, self.bottom+self.block_size*0.1)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.right-self.block_size*0.1, self.bottom,
                                self.right, self.bottom,
                                self.right, self.bottom+self.block_size,
                                self.right-self.block_size*0.1, self.bottom+self.block_size)),
                       ('c4f', dark_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left+self.block_size*0.9, self.bottom+self.block_size*0.9,
                                self.right-self.block_size*0.9, self.bottom+self.block_size*0.9,
                                self.right-self.block_size*0.9, self.bottom+self.block_size,
                                self.left+self.block_size*0.9, self.bottom+self.block_size)),
                       ('c4f', light_color))
        self.batch.add(4, GL_QUADS, None,
                       ('v2f', (self.left, self.bottom,
                                self.left+self.block_size*0.1, self.bottom,
                                self.left+self.block_size*0.1, self.bottom+self.block_size,
                                self.left, self.bottom+self.block_size)),
                       ('c4f', light_color))
