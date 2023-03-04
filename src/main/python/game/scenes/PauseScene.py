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

from i18n.Translations import translate

from game.drawables.DrawableUtils import draw_text_in_rect

from game.scenes.Scene import Scene
from game.GameState import State
from game.drawables.MenuItem import MenuItem

class PauseScene(Scene):
    """Pause scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.font_cache.get('main.xl')
        self.font_l = self.game_data.font_cache.get('main.l')
        self.font_s = self.game_data.font_cache.get('main.s')
        self.text_color_score = self.game_data.game_config.get('text.color.score')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.items = []
        self.item_score = None
        self.item_score = None

        self._init_items()

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        # Logo
        width = 650
        height = 150
        rect = (self.screen_mid[0] - width / 2, 0, width, height)
        item_logo = MenuItem(
                                    self.game_data,
                                    self.font_xl,
                                    rect,
                                    (self.screen_mid[0], height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=translate('game.name')
                                )
        self.items.append(item_logo)

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
                                    text=translate('scene.pause.score').format(self.game_data.score),
                                    banner=True
                                )
        self.items.append(self.item_score)

        # Pause
        width = 250
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height / 2, width, height)
        item_pause = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + 5),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('scene.pause.pause'),
                                    button_none=True
                                )
        self.items.append(item_pause)

        # Help
        width = self.screen_size[0] - 20
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_size[1] - height - 10, width, height)
        item_help = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_help,
                                    text=translate('scene.pause.help'),
                                    button_none=True
                                )
        self.items.append(item_help)

    def loop(self, tick):
        # Handle "global" events
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
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()

        if not self.is_state(State.PAUSE):
            self.game_data.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            return

        self.game_data.scene_game.loop_visuals(tick)

    def draw(self):
        self.game_data.scene_game.draw(show_score=False, show_fps=False)

        self.item_score.set_text(translate('scene.pause.score').format(self.game_data.score))

        for item in self.items:
            item.loop()
            item.draw()
