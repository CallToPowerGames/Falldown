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

from game.scenes.Scene import Scene
from game.GameState import State
from game.drawables.MenuItem import MenuItem

@unique
class OptionsSceneActiveItem(Enum):
    """The active item"""
    FULLSCREEN = 0
    LANGUAGE = 1
    BACKGROUND = 2
    BACK = 10


class OptionsScene(Scene):
    """Options scene"""

    def __init__(self, state, fps, game):
        super().__init__(state, fps, game)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.cache.font_cache.get('main.xl')
        self.font_l = self.game_data.cache.font_cache.get('main.l')
        self.font_m = self.game_data.cache.font_cache.get('main.m')
        self.font_s = self.game_data.cache.font_cache.get('main.s')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.active_item = OptionsSceneActiveItem.FULLSCREEN

        self.item_logo = None
        self.item_options = None
        self.item_fullscreen = None
        self.item_language = None
        self.item_language_current = None
        self.item_background = None
        self.item_back = None
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

        item_width = 450
        item_height = 80

        # Options
        width = 500
        height = 70
        rect = (self.screen_mid[0] - width / 2, 0 + height / 2, width, height)
        self.item_options = MenuItem(
                                self.game_data,
                                self.font_l,
                                rect,
                                (self.screen_mid[0], self.screen_size[1] / 2 - height * 2),
                                width=width,
                                height=height,
                                color=self.text_color,
                                rect_width=-1,
                                text=self.game_data.i18n.get('menu.options.txt')
                            )
        self.items.append(self.item_options)

        # Fullscreen
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height - 30, width, height)
        self.item_fullscreen = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - height / 2 - 30),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('menu.fullscreen.txt'),
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.item_fullscreen.sound_played = True
        self.items.append(self.item_fullscreen)

        # Language
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - 30, width, height)
        self.item_language = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height / 2 - 30),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('menu.language.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_language)

        # Current language
        width = item_width
        height = item_height
        width_lc = 60
        height_lc = 60
        rect = (self.screen_mid[0] + width / 2 + 5, self.screen_mid[1] - 16, width_lc, height_lc)
        self.item_language_current = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0] + width / 2 + width_lc / 2 + 5, self.screen_mid[1] + height_lc / 2 - 10),
                                    width=width_lc,
                                    height=height_lc,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.language_main,
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_language_current)

        # Background
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] + height - 30, width, height)
        self.item_background = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height + height / 2 - 30),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('menu.background.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_background)

        # Back
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] + height + height / 2 + 10, width, height)
        self.item_back = MenuItem(
                                    self.game_data,
                                    self.font_m,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height + height + 10),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=self.game_data.i18n.get('menu.back.txt'),
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
                                    text=self.game_data.i18n.get('menu.fullscreen.help'),
                                    rotate=True,
                                    rotate_ticks_max=8,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))
        self.item_options.set_text(self.game_data.i18n.get('menu.options.txt'))
        self.item_fullscreen.set_text(self.game_data.i18n.get('menu.fullscreen.txt'))
        self.item_language.set_text(self.game_data.i18n.get('menu.language.txt'))
        self.item_language_current.set_text(self.game_data.i18n.language_main)
        self.item_background.set_text(self.game_data.i18n.get('menu.background.txt'))
        self.item_back.set_text(self.game_data.i18n.get('menu.back.txt'))
        self.item_help.set_text(self.game_data.i18n.get('menu.language.help'))

    def _reset_button_to_init(self, sound_played=False):
        """Resets the buttons to initial activation status"""
        self.item_back.active = False
        self.item_language.active = False
        self.item_background.active = False
        self.item_fullscreen.active = True
        self.active_item = OptionsSceneActiveItem.FULLSCREEN
        self.reset_texts()
        self.item_help.rotate = True
        self.item_help.set_text(self.game_data.i18n.get('menu.fullscreen.help'))
        self.item_fullscreen.sound_played = sound_played

    def _keypress_arrow_up(self):
        if self.active_item == OptionsSceneActiveItem.LANGUAGE:
            self._reset_button_to_init()
        elif self.active_item == OptionsSceneActiveItem.BACKGROUND:
            self.item_back.active = False
            self.item_fullscreen.active = False
            self.item_background.active = False
            self.item_language.active = True
            self.active_item = OptionsSceneActiveItem.LANGUAGE
            self.reset_texts()
            self.item_help.rotate = False
            self.item_help.set_text(self.game_data.i18n.get('menu.language.help'))
        elif self.active_item == OptionsSceneActiveItem.BACK:
            self.item_back.active = False
            self.item_fullscreen.active = False
            self.item_language.active = False
            self.item_background.active = False
            self.item_background.active = True
            self.active_item = OptionsSceneActiveItem.BACKGROUND
            self.reset_texts()
            self.item_help.rotate = True
            self.item_help.set_text(self.game_data.i18n.get('menu.background.help'))

    def _keypress_arrow_down(self):
        if self.active_item == OptionsSceneActiveItem.FULLSCREEN:
            self.item_fullscreen.active = False
            self.item_back.active = False
            self.item_background.active = False
            self.item_language.active = True
            self.active_item = OptionsSceneActiveItem.LANGUAGE
            self.reset_texts()
            self.item_help.rotate = False
            self.item_help.set_text(self.game_data.i18n.get('menu.language.help'))
        elif self.active_item == OptionsSceneActiveItem.LANGUAGE:
            self.item_fullscreen.active = False
            self.item_language.active = False
            self.item_back.active = False
            self.item_background.active = True
            self.active_item = OptionsSceneActiveItem.BACKGROUND
            self.reset_texts()
            self.item_help.rotate = True
            self.item_help.set_text(self.game_data.i18n.get('menu.background.help'))
        elif self.active_item == OptionsSceneActiveItem.BACKGROUND:
            self.item_fullscreen.active = False
            self.item_language.active = False
            self.item_background.active = False
            self.item_back.active = True
            self.active_item = OptionsSceneActiveItem.BACK
            self.reset_texts()
            self.item_help.rotate = False
            self.item_help.set_text(self.game_data.i18n.get('menu.back.help'))

    def loop(self, tick):
        dt = tick / 1000

        self.game_data.background.loop(dt)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(State.MENU)
                elif event.key == pygame.K_UP:
                    self._keypress_arrow_up()
                elif event.key == pygame.K_DOWN:
                    self._keypress_arrow_down()
                elif event.key == pygame.K_RETURN:
                    if self.active_item == OptionsSceneActiveItem.FULLSCREEN:
                        self.game_data.toggle_fullscreen()
                    elif self.active_item == OptionsSceneActiveItem.LANGUAGE:
                        self.game_data.i18n.switch_language()
                        self.game_data.reload_i18n_texts()
                        self.reset_texts()
                    elif self.active_item == OptionsSceneActiveItem.BACKGROUND:
                        self.game_data.game_config.set('background.draw', not self.game_data.game_config.get('background.draw'))
                        self.game_data.background.reload_conf()
                        self.game_data.game_config.save_game_conf()
                    elif self.active_item == OptionsSceneActiveItem.BACK:
                        self._reset_button_to_init(sound_played=True)
                        self.set_state(State.MENU)

        if not self.is_state(State.OPTIONS):
            self.game_data.cache.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            return

    def draw(self):
        """Draws the scene"""
        self.game_data.background.draw()

        for item in self.items:
            item.loop()
            item.draw()
