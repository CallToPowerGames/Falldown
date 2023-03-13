#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - GameOver"""

import logging

import pygame

from game.drawables.DrawableUtils import draw_text_in_rect
from game.scenes.Scene import Scene
from game.GameState import State
from game.drawables.MenuItem import MenuItem

class GameOverScene(Scene):
    """GameOver scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.cache.font_cache.get('main.xl')
        self.font_m = self.game_data.cache.font_cache.get('main.m')
        self.font_s = self.game_data.cache.font_cache.get('main.s')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color_score = self.game_data.game_config.get('text.color.score')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.text_color_help = self.game_data.game_config.get('text.color.help')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.item_logo = None
        self.item_score = None
        self.item_gameover = None
        self.item_help = None
        self.highscore_db = []
        self.saved_highscore = False

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

        # Score
        width = 500
        height = 100
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height - height / 2, width, height)
        self.item_score = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - height),
                                    width=width,
                                    height=height,
                                    color=self.text_color_score,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('scene.gameover.score').format(self.game_data.score),
                                    banner=True
                                )
        self.items.append(self.item_score)

        # GameOver
        width = 400
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height / 2, width, height)
        self.item_gameover = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + 5),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('scene.gameover.gameover'),
                                    button_none=True
                                )
        self.items.append(self.item_gameover)

        # Help
        width = self.screen_size[0] - 20
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_size[1] - height - 10, width, height)
        self.item_help = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_help,
                                    text=self.game_data.i18n.get('scene.gameover.help'),
                                    rotate=True,
                                    rotate_ticks_max=6,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))
        self.item_score.set_text(self.game_data.i18n.get('scene.gameover.score').format(self.game_data.score))
        self.item_gameover.set_text(self.game_data.i18n.get('scene.gameover.gameover'))
        self.item_help.set_text(self.game_data.i18n.get('scene.gameover.help'))

    def loop(self, tick):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(State.MENU)
                if event.key == pygame.K_RETURN:
                    self.set_state(State.MENU)

        if not self.is_state(State.GAMEOVER):
            self.game_data.scene_game.stop_music()
            self.saved_highscore = False
            self.game_data.background.reset(initialize_background_level=True)
            return

        if not self.saved_highscore:
            if self.game_data.score > 0:
                self.game_data.highscore.add_entry(self.game_data.player_info['name_key'], self.game_data.score)
            else:
                logging.info('Score not high enough, not saving...')
            self.saved_highscore = True

        self.game_data.scene_game.loop_visuals(tick)

    def draw(self):
        self.game_data.scene_game.draw(show_score=False, show_fps=False)

        self.item_score.set_text(self.game_data.i18n.get('scene.pause.score').format(self.game_data.score))

        for item in self.items:
            item.loop()
            item.draw()
