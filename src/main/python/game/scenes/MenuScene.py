#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Menu"""

import logging
import random
from enum import Enum, unique

import pygame

from lib.AppConfig import app_conf_get
from i18n.Translations import translate

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.drawables.MenuItem import MenuItem

@unique
class MenuSceneActiveItem(Enum):
    """The active item"""
    START = 0
    OPTIONS = 1
    HIGHSCORE = 2
    QUIT = 10


class MenuScene(Scene):
    """Menu scene"""

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
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu = self.game_data.game_config.get('music.volume.background.menu')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')
        self.menu_music = self.game_data.game_config.get('menu.music')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.playing_music = False
        self.curr_bg_music = ''
        self.active_item = MenuSceneActiveItem.START
        self.background = None
        self.items = []
        self.item_startgame = None
        self.item_options = None
        self.item_quitgame = None
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

        # By
        width = 500
        height = 70
        rect = (self.screen_mid[0] - width / 2, 0 - height / 2, width, height)
        item_by = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], height * 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_inactive,
                                    rect_width=-1,
                                    text=translate('game.by').format(app_conf_get('author'))
                                )
        self.items.append(item_by)

        # Version
        width = 500
        height = 60
        rect = (self.screen_mid[0] - width / 2, height + 40, width, height)
        item_version = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height * 2 + 20),
                                    width=width,
                                    height=height,
                                    color=self.text_color_inactive,
                                    rect_width=-1,
                                    text=translate('game.version').format(app_conf_get('version'))
                                )
        self.items.append(item_version)

        item_width = 450
        item_height = 80
        gap = 2

        # Start game
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height - 60 + gap, width, height)
        self.item_startgame = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - height / 2 - 60 + gap * 3),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.start_game.txt'),
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.item_startgame.sound_played = True
        self.items.append(self.item_startgame)

        # Highscore menu
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] - height / 2 - 20, width, height)
        self.item_highscore = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] - 20),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.highscore.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_highscore)

        # Options menu
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] + height / 2 - 20, width, height)
        self.item_options = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height - 20),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.options.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_options)

        # Quit game
        width = item_width
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] + height + 20 - gap, width, height)
        self.item_quitgame = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height + height / 2 + 20 - gap / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.quit_game.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_quitgame)

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
                                    text=translate('menu.start_game.help'),
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def _reset_texts(self):
        """Resets the texts to original position"""
        self.item_startgame.reset_text()
        self.item_highscore.reset_text()
        self.item_options.reset_text()
        self.item_quitgame.reset_text()

    def _keypress_arrow_up(self):
        if self.active_item == MenuSceneActiveItem.HIGHSCORE:
            self.item_quitgame.active = False
            self.item_options.active = False
            self.item_highscore.active = False
            self.item_startgame.active = True
            self.active_item = MenuSceneActiveItem.START
            self._reset_texts()
            self.item_help.set_text(translate('menu.start_game.help'))
        elif self.active_item == MenuSceneActiveItem.OPTIONS:
            self.item_quitgame.active = False
            self.item_options.active = False
            self.item_startgame.active = False
            self.item_highscore.active = True
            self.active_item = MenuSceneActiveItem.HIGHSCORE
            self._reset_texts()
            self.item_help.set_text(translate('menu.highscore.help'))
        elif self.active_item == MenuSceneActiveItem.QUIT:
            self.item_quitgame.active = False
            self.item_startgame.active = False
            self.item_highscore.active = False
            self.item_options.active = True
            self.active_item = MenuSceneActiveItem.OPTIONS
            self._reset_texts()
            self.item_help.set_text(translate('menu.options.help'))

    def _keypress_arrow_down(self):
        if self.active_item == MenuSceneActiveItem.START:
            self.item_startgame.active = False
            self.item_quitgame.active = False
            self.item_options.active = False
            self.item_highscore.active = True
            self.active_item = MenuSceneActiveItem.HIGHSCORE
            self._reset_texts()
            self.item_help.set_text(translate('menu.highscore.help'))
        elif self.active_item == MenuSceneActiveItem.HIGHSCORE:
            self.item_startgame.active = False
            self.item_highscore.active = False
            self.item_quitgame.active = False
            self.item_options.active = True
            self.active_item = MenuSceneActiveItem.OPTIONS
            self._reset_texts()
            self.item_help.set_text(translate('menu.options.help'))
        elif self.active_item == MenuSceneActiveItem.OPTIONS:
            self.item_startgame.active = False
            self.item_highscore.active = False
            self.item_options.active = False
            self.item_quitgame.active = True
            self.active_item = MenuSceneActiveItem.QUIT
            self._reset_texts()
            self.item_help.set_text(translate('menu.quit_game.help'))

    def start_music(self):
        if not self.playing_music:
            self.playing_music = True
            self.curr_bg_music = random.choice(self.menu_music)
            self.game_data.sound_cache.load_music(self.curr_bg_music)
            self.game_data.sound_cache.play_music(loops=-1, volume=self.music_volume_bg_menu)

    def stop_music(self):
        self.game_data.sound_cache.stop_music()
        self.playing_music = False

    def loop(self, tick):
        dt = tick / 1000

        self.background.loop(dt)

        # Handle "global" events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()
                elif event.key == pygame.K_UP:
                    self._keypress_arrow_up()
                elif event.key == pygame.K_DOWN:
                    self._keypress_arrow_down()
                elif event.key == pygame.K_RETURN:
                    if self.active_item == MenuSceneActiveItem.HIGHSCORE:
                        self._reset_texts()
                        self.set_state(State.HIGHSCORE)
                    elif self.active_item == MenuSceneActiveItem.OPTIONS:
                        self._reset_texts()
                        self.set_state(State.OPTIONS)
                    elif self.active_item == MenuSceneActiveItem.QUIT:
                        self.exit()
                    else:
                        self.set_state(State.PLAYERSELECTION)

        if not self.is_state(State.MENU):
            self.game_data.sound_cache.play('menuitem.activate', volume=self.music_volume_bg_menu_effects)
            if not (self.is_state(State.OPTIONS) or self.is_state(State.HIGHSCORE) or self.is_state(State.PLAYERSELECTION)):
                self.stop_music()
            return
        else:
            self.start_music()

    def draw(self):
        """Draws the scene"""
        self.background.draw()

        for item in self.items:
            item.loop()
            item.draw()
