#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Options"""

import logging
from enum import Enum, unique

import pygame

from lib.AppConfig import app_conf_get
from i18n.Translations import translate

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.drawables.MenuItem import MenuItem

@unique
class OptionsSceneActiveItem(Enum):
    """The active item"""
    FULLSCREEN = 0
    BACK = 10


class OptionsScene(Scene):
    """Options scene"""

    def __init__(self, state, fps, game):
        super().__init__(state, fps, game)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.font_cache.get('main.xl')
        self.font_l = self.game_data.font_cache.get('main.l')
        self.font_s = self.game_data.font_cache.get('main.s')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.line_width = self.game_data.game_config.get('line.width')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.active_item = OptionsSceneActiveItem.FULLSCREEN
        self.background = None
        self.items = []
        self.item_fullscreen = None
        self.item_back = None
        self.item_help = None

        self._init_items()

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        self.background = Background(self.game_data)

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
                                    text=translate('game.name'),
                                    banner=True
                                )
        self.items.append(item_logo)

        item_width = 520
        item_height = 80
        gap = 2

        # Options
        width = 500
        height = 70
        rect = (self.screen_mid[0] - width / 2, 0 + height / 2, width, height)
        item_options = MenuItem(
                                self.game_data,
                                self.font_l,
                                rect,
                                (self.screen_mid[0], self.screen_size[1] / 2 - height * 2),
                                width=width,
                                height=height,
                                color=self.text_color,
                                rect_width=-1,
                                text=translate('menu.options.txt')
                            )
        self.items.append(item_options)

        # Fullscreen
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height + gap, width, height)
        self.item_fullscreen = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - height / 2 + gap * 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.fullscreen.txt'),
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.item_fullscreen.sound_played = True
        self.items.append(self.item_fullscreen)

        # Back
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1], width, height)
        self.item_back = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height / 2 + gap * 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.back.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_back)

        # Help
        width = self.screen_size[0] - 20
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_size[1] - height - 10, width, height)
        self.item_help = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_help,
                                    text=translate('menu.fullscreen.help'),
                                    rotate=True,
                                    rotate_ticks_max=8,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def _reset_texts(self):
        """Resets the texts to original position"""
        self.item_fullscreen.reset_text()
        self.item_back.reset_text()
        self.item_help.reset_text()

    def _reset_button_to_init(self, sound_played=False):
        """Resets the buttons to initial activation status"""
        self.item_back.active = False
        self.item_fullscreen.active = True
        self.active_item = OptionsSceneActiveItem.FULLSCREEN
        self._reset_texts()
        self.item_help.rotate = True
        self.item_help.set_text(translate('menu.fullscreen.help'))
        self.item_fullscreen.sound_played = sound_played

    def _keypress_arrow_up(self):
        if self.active_item == OptionsSceneActiveItem.BACK:
            self._reset_button_to_init()

    def _keypress_arrow_down(self):
        if self.active_item == OptionsSceneActiveItem.FULLSCREEN:
            self.item_fullscreen.active = False
            self.item_back.active = True
            self.active_item = OptionsSceneActiveItem.BACK
            self._reset_texts()
            self.item_help.rotate = False
            self.item_help.set_text(translate('menu.back.help'))

    def loop(self, tick):
        dt = tick / 1000

        self.background.loop(dt)

        # Handle "global" events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(State.MENU)
                elif event.key == pygame.K_f:
                    self.game_data.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    self._keypress_arrow_up()
                elif event.key == pygame.K_DOWN:
                    self._keypress_arrow_down()
                elif event.key == pygame.K_RETURN:
                    if self.active_item == OptionsSceneActiveItem.BACK:
                        self._reset_button_to_init(sound_played=True)
                        self.set_state(State.MENU)
                    else:
                        self.game_data.toggle_fullscreen()

        if not self.is_state(State.OPTIONS):
            self.game_data.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            return

    def draw(self):
        """Draws the scene"""
        self.background.draw()

        for item in self.items:
            item.loop()
            item.draw()
