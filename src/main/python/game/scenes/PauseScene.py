#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Pause"""

import logging

import pygame

from game.scenes.Scene import Scene
from game.GameState import State
from game.drawables.MenuItem import MenuItem

class PauseScene(Scene):
    """Pause scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.cache.font_cache.get('main.xl')
        self.font_l = self.game_data.cache.font_cache.get('main.l')
        self.font_m = self.game_data.cache.font_cache.get('main.m')
        self.font_s = self.game_data.cache.font_cache.get('main.s')
        self.text_color_score = self.game_data.game_config.get('text.color.score')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.item_logo = None
        self.item_score = None
        self.item_pause = None
        self.item_help = None

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
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - height),
                                    width=width,
                                    height=height,
                                    color=self.text_color_score,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('scene.pause.score').format(self.game_data.score),
                                    banner=True
                                )
        self.items.append(self.item_score)

        # Pause
        width = 250
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height / 2, width, height)
        self.item_pause = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + 5),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('scene.pause.pause'),
                                    button_none=True
                                )
        self.items.append(self.item_pause)

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
                                    text=self.game_data.i18n.get('scene.pause.help'),
                                    rotate=True,
                                    rotate_ticks_max=6,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))
        self.item_score.set_text(self.game_data.i18n.get('scene.pause.score').format(self.game_data.score))
        self.item_pause.set_text(self.game_data.i18n.get('scene.pause.pause'))
        self.item_help.set_text(self.game_data.i18n.get('scene.pause.help'))

    def loop(self, tick):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_data.scene_game.stop_music()
                    self.game_data.scene_game.camera.stop()
                    self.set_state(State.PLAYERSELECTION)
                elif event.key == pygame.K_SPACE:
                    self.set_state(State.GAME)

        if not self.is_state(State.PAUSE):
            self.game_data.cache.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            if not self.is_state(State.GAME):
                self.game_data.background.reset(initialize_background_level=True)
            return

        self.game_data.scene_game.loop_visuals(tick)

    def draw(self):
        self.game_data.scene_game.draw(show_score=False, show_fps=False)

        self.item_score.set_text(self.game_data.i18n.get('scene.pause.score').format(self.game_data.score))

        for item in self.items:
            item.loop()
            item.draw()
