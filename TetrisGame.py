#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyglet
from game.game_window import GameWindow


def main():
    game_window = GameWindow(800, 600)
    game_window.set_caption('Tetris Game')
    pyglet.app.run()


if __name__ == '__main__':
    main()
