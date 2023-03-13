#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Exit"""

import logging

import pygame

from game.drawables.DrawableUtils import draw_text_in_rect

from game.scenes.Scene import Scene
from game.GameState import State
from game.drawables.MenuItem import MenuItem

class ExitScene(Scene):
    """Exit scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.cache.font_cache.get('main.xl')
        self.font_m = self.game_data.cache.font_cache.get('main.m')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.item_logo = None
        self.item_exit = None

        self.draw_background_level = True

        self._init_items()

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        # Logo
        width = 650
        height = 150
        rect = (self.screen_mid[0] - width / 2, 0, width, height)
        self.item_logo = MenuItem(
                                    self.game_data,
                                    self.font_xl,
                                    rect,
                                    (self.screen_mid[0], height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('game.name'),
                                    banner=True
                                )
        self.items.append(self.item_logo)

        # Exit
        width = 250
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height / 2, width, height)
        self.item_exit = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + 5),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('scene.exit.txt'),
                                    button=True
                                )
        self.items.append(self.item_exit)

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))
        self.item_exit.set_text('{} '.format(self.game_data.i18n.get('scene.exit.txt')))

    def loop(self, tick):
        dt = tick / 1000

        self.game_data.background.loop(dt, iterate_offset=True)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_data._exit_full()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_data._exit_full()

        if not self.is_state(State.EXIT):
            return

    def draw(self):
        self.game_data.background.draw(draw_background_level=self.draw_background_level)

        for item in self.items:
            item.loop()
            item.draw()
