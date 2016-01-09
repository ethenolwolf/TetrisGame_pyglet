# -*- coding: utf-8 -*-
import random
import pyglet
from pyglet.gl import *
from pyglet.image import ImagePattern, ImageData
from pyglet.window import Window
from pyglet.window import key

pyglet.resource.path = ['resources']
pyglet.resource.reindex()
pyglet.resource.add_font('MONOFONT.TTF')


BLACK = (0.2, 0.2, 0.2, 1.0)      # color 0
RED = (1.0, 0.5, 0.5, 1.0)        # color 1
GREEN = (0.5, 1.0, 0.5, 1.0)      # color 2
BLUE = (0.5, 0.5, 1.0, 1.0)       # color 3
YELLOW = (0.8, 0.8, 0.5, 1.0)     # color 4
GREY = (0.7, 0.7, 0.7, 1.0)       # color 5
DARK_GREY = (0.5, 0.5, 0.5, 1.0)  # color 6
WHITE = (0.9, 0.9, 0.9, 1.0)      # color 7

COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, GREY, DARK_GREY, WHITE]

# ''' SHAPE coordinate
# -1, 1  0, 1  1, 1  2, 1
# -1, 0  0, 0  1, 0  2, 0
# -1,-1  0,-1  1,-1  2,-1
# -1,-2  0,-2  1,-2  2,-2
# '''

SHAPES = [
    ((-1, 0), (0, 0), (1, 0), (2, 0)),    # horizontal bar
    ((0, 0), (1, 0), (0, -1), (1, -1)),   # square box
    ((-1, 0), (0, 0), (1, 0), (0, -1)),   # T
    ((0, 1), (0, 0), (0, -1), (1, -1)),   # L
    ((1, 1), (1, 0), (1, -1), (0, -1)),   # reverse L
    ((1, 1), (1, 0), (0, 0), (0, -1)),    # N
    ((0, 1), (0, 0), (1, 0), (1, -1)),    # reverse N
]


def int_color(float_color):
    return tuple(map(lambda c: int(c*255), float_color))


def lighten_color(float_color):
    return tuple(map(lambda c: min(c*1.2, 1.0), float_color))


def darken_color(float_color):
    return tuple(map(lambda c: c*0.8, float_color))


class BlockImagePattern(ImagePattern):
    def __init__(self, color):
        self.color = int_color(color)
        self.light_color = int_color(lighten_color(color))
        self.dark_color = int_color(darken_color(color))

    def create_image(self, width, height):
        data = b''
        for i in range(width * height):
            pos_x = i % width
            pos_y = i // width
            if pos_x / width <= 0.08:
                data += bytes(self.light_color)
            elif pos_y / height <= 0.08:
                data += bytes(self.dark_color)
            elif pos_y / height >= 0.92:
                data += bytes(self.light_color)
            elif pos_x / width >= 0.92:
                data += bytes(self.dark_color)
            else:
                data += bytes(self.color)
        return ImageData(width, height, 'RGBA', data)


class GameWindow(Window):

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.title_label = pyglet.text.Label(text='Tetris',
                                             font_name='Monofonto',
                                             font_size=32,
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

        self.BLOCK_IMAGES = [
            pyglet.image.create(int(self.block_size), int(self.block_size),
                                BlockImagePattern(color)) for color in COLORS
        ]

        self.board = [0 for _ in range(10 * 20)]

        font = pyglet.font.load(name='Monofonto', size=16)
        self.clock_display = pyglet.clock.ClockDisplay(font=font,
                                                       color=(.8, .8, .8, .8))
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        pyglet.gl.glClearColor(*BLACK)
        self.make_background()

        self.player_start_pos = (4, 18)
        self.player_pos = [4, 18]
        self.player_shape = list(SHAPES[random.randint(0, 6)])
        self.player_color = random.randint(1, 4)

        self.next_shape = random.randint(0, 6)
        self.next_color = random.randint(1, 4)

        self.count_down = 2
        self.state_time = self.count_down

        self.game_over = False
        self.game_over_animation_count = 0

        self.player_control = True
        self.full_lines = []
        self.full_line_anim_x = 0
        self.full_line_anim_y = 0

        self.high_score = 0
        self.target_score = 0
        self.score = 0
        self.basic_score = 100
        self.full_line_score = 1000
        self.score_add_step = 10
        self.score_label = pyglet.text.Label('Score: 0',
                                             font_name='Monofonto',
                                             font_size=20,
                                             color=int_color(WHITE),
                                             x=self.right+self.block_size*2,
                                             y=self.bottom+self.block_size*22.5,
                                             batch=self.batch)
        self.high_score_label = pyglet.text.Label('High Score: {}'.format(self.high_score),
                                                  font_name='Monofonto',
                                                  font_size=20,
                                                  color=int_color(WHITE),
                                                  x=self.right+self.block_size*2,
                                                  y=self.bottom+self.block_size*24,
                                                  batch=self.batch)
        self.show_game_over_label = False
        self.game_over_label = pyglet.text.Label('Game Over',
                                                 font_name='Monofonto',
                                                 font_size=32,
                                                 color=int_color(WHITE),
                                                 x=self.width/2,
                                                 y=self.height/2,
                                                 anchor_x='center',
                                                 anchor_y='center')
        self.restart_label = pyglet.text.Label('press Enter to restart',
                                               font_name='Monofonto',
                                               font_size=20,
                                               color=int_color(WHITE),
                                               x=self.width/2,
                                               y=self.height/2-32,
                                               anchor_x='center',
                                               anchor_y='center')

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
        self.draw_board()
        self.draw_next_shape()

        if self.full_lines:
            self.player_control = False
            self.remove_full_line_animation()

        if self.player_control:
            self.draw_player()
        self.batch.draw()
        if self.show_game_over_label:
            self.game_over_label.draw()
            self.restart_label.draw()
        self.clock_display.draw()

    def update(self, delta):
        if self.score < self.target_score:
            self.score += self.score_add_step
            self.score = min(self.score, self.target_score)
            self.update_score_label()

        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.text = 'High Score: {}'.format(self.high_score)

        if self.game_over:
            self.do_game_over_animation()
            return

        self.state_time -= delta
        if self.state_time <= 0:
            self.check_down()

    def update_score_label(self):
        self.score_label.text = 'Score: {}'.format(self.score)

    def restart(self):
        self.game_over = False
        self.show_game_over_label = False
        self.player_control = True
        self.game_over_animation_count = 0
        if self.target_score > self.high_score:
            self.high_score = self.target_score
        self.target_score = 0
        self.score = 0
        self.update_score_label()
        self.board = [0 for _ in range(10 * 20)]
        self.next_shape = random.randint(0, 6)
        self.next_color = random.randint(1, 4)
        self.next_player()

    def do_game_over_animation(self):
        if self.game_over_animation_count < 10 * 20:
            for i in range(10):
                if self.board[self.game_over_animation_count] != 0:
                    self.board[self.game_over_animation_count] = 6  # dark grey
                self.game_over_animation_count += 1
        else:
            self.show_game_over_label = True

    def on_key_press(self, symbol, modifiers):
        if self.player_control:
            if symbol == key.LEFT:
                self.check_left()
            if symbol == key.RIGHT:
                self.check_right()
            if symbol == key.DOWN:
                self.check_down()
            if symbol == key.UP:
                self.check_rotate()
            if symbol == key.SPACE:
                self.direct_down()

        if symbol == key.ENTER:
            if self.game_over:
                self.restart()

    def check_game_over(self):
        for cell in self.board[-10:]:
            if cell != 0:
                self.player_control = False
                self.game_over_animation_count = 0
                self.game_over = True
                break

    def check_rotate(self):
        tmp_next = []
        for pos in self.player_shape:
            tmp_next.append((pos[1] * -1, pos[0] - 1))
        can_rotate = True
        for pos in tmp_next:
            if (self.player_pos[0] + pos[0]) < 0 \
                    or (self.player_pos[0] + pos[0]) > 9 \
                    or (self.player_pos[1] + pos[1]) < 0 \
                    or self.board[(self.player_pos[0] + pos[0]) +
                                  (self.player_pos[1] + pos[1]) * 10] != 0:
                can_rotate = False
                break
        if can_rotate:
            self.player_shape = tmp_next

    def check_left(self):
        can_move = True
        for pos in self.player_shape:
            next_x = self.player_pos[0] + pos[0] - 1
            if next_x < 0:
                can_move = False
                break
            next_y = self.player_pos[1] + pos[1]
            if self.board[next_x + next_y * 10] != 0:
                can_move = False
                break
        if can_move:
            self.player_pos[0] -= 1

    def check_right(self):
        can_move = True
        for pos in self.player_shape:
            next_x = self.player_pos[0] + pos[0] + 1
            if next_x > 9:
                can_move = False
                break
            next_y = self.player_pos[1] + pos[1]
            if self.board[next_x + next_y * 10] != 0:
                can_move = False
                break
        if can_move:
            self.player_pos[0] += 1

    def check_down(self):
        hit = False
        for pos in self.player_shape:
            next_y = self.player_pos[1] + pos[1] - 1
            if next_y < 0:
                hit = True
            elif self.board[(self.player_pos[0]+pos[0]) + next_y*10] != 0:
                hit = True

        if not hit:
            self.player_pos[1] -= 1
        else:
            min_y = self.player_pos[1]
            max_y = self.player_pos[1]
            for pos in self.player_shape:
                x = self.player_pos[0] + pos[0]
                y = self.player_pos[1] + pos[1]
                self.board[y * 10 + x] = self.player_color
                min_y = min(min_y, y)
                max_y = max(max_y, y)
            self.target_score += self.basic_score
            self.check_full_lines(min_y, max_y)
            self.next_player()
        self.state_time = self.count_down
        self.check_game_over()
        return hit

    def direct_down(self):
        while not self.check_down():
            pass

    def remove_full_line_animation(self):
        # y = self.full_lines[0]
        # for x in range(10):
        #     self.board[x + y * 10] = 0
        # del self.full_lines[0]
        if self.full_line_anim_y < len(self.full_lines):
            line_y = self.full_lines[self.full_line_anim_y]
            self.board[self.full_line_anim_x + line_y * 10] = 0
            self.full_line_anim_x += 1
            if self.full_line_anim_x > 9:
                self.full_line_anim_x = 0
                self.full_line_anim_y += 1
                # add score
                self.target_score += self.full_line_score
        else:
            for num, line in enumerate(self.full_lines):
                current_line = line - num
                for y in range(current_line, 19):
                    for x in range(10):
                        self.board[x + y * 10] = self.board[x + (y + 1) * 10]
            self.player_control = True
            self.full_line_anim_x = 0
            self.full_line_anim_y = 0
            self.full_lines = []

    def check_full_lines(self, min_y, max_y):
        for y in range(min_y, max_y+1):
            full_line = True
            for x in range(10):
                if self.board[x + y * 10] == 0:
                    full_line = False
                    break
            if full_line:
                self.full_lines.append(y)
        self.full_lines.sort()

        for y in self.full_lines:
            for x in range(10):
                self.board[x + y * 10] = 5  # mark grey

    def next_player(self):
        self.player_pos = list(self.player_start_pos)
        self.player_shape = list(SHAPES[self.next_shape])
        self.player_color = self.next_color
        self.next_shape = random.randint(0, 6)
        self.next_color = random.randint(1, 4)
        for pos in self.player_shape:
            pos_x = self.player_pos[0] + pos[0]
            pos_y = self.player_pos[1] + pos[1]
            if self.board[pos_x + pos_y * 10] != 0:
                for new_pos in self.player_shape:
                    self.board[(self.player_pos[0]+new_pos[0])+(self.player_pos[1]+new_pos[1])*10] = self.player_color
                self.game_over = True
                break

    def draw_player(self):
        if self.game_over:
            return
        for pos in self.player_shape:
            x = self.left + (self.player_pos[0] + pos[0] + 1) * self.block_size
            y = self.bottom + (self.player_pos[1] + pos[1] + 1) * self.block_size
            self.BLOCK_IMAGES[self.player_color].blit(x, y)

    def draw_next_shape(self):
        left = self.right + self.block_size * 4
        bottom = self.bottom + self.block_size * 19
        for pos in SHAPES[self.next_shape]:
            x = left + pos[0] * self.block_size
            y = bottom + pos[1] * self.block_size
            self.BLOCK_IMAGES[self.next_color].blit(x, y)

    def draw_board(self):
        size = self.block_size
        for i, v in enumerate(self.board):
            if v == 0:
                continue
            pos_x = i % 10
            pos_y = i // 10
            x = self.left + (pos_x + 1) * size
            y = self.bottom + (pos_y + 1) * size
            self.BLOCK_IMAGES[v].blit(x, y)

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
