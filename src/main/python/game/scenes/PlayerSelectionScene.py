#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Player selection"""

import logging
from enum import Enum, unique
import random

import pygame

from lib.AppConfig import app_conf_get
from i18n.Translations import translate

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.drawables.MenuItem import MenuItem
from game.drawables.ImageMenuItem import ImageMenuItem
from game.sprites.Spritesheet import Spritesheet

class PlayerSelectionScene(Scene):
    """PlayerSelection scene"""

    def __init__(self, state, fps, game):
        super().__init__(state, fps, game)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.font_cache.get('main.xl')
        self.font_l = self.game_data.font_cache.get('main.l')
        self.font_s = self.game_data.font_cache.get('main.s')
        self.font_xs = self.game_data.font_cache.get('main.xs')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.curr_player_index = 0
        self.last_valid_player_index = self.curr_player_index

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.background = None
        self.items = []
        self.imageitems = []
        self.item_back = None
        self.item_random = None

        self._load_players()
        self._init_items()
        self._update_selection()

    def _load_players(self):
        """Loads the players"""
        logging.debug('Initializing players')
        self.game_data.players = []
        for i in range(0, self.game_data.game_config.get('player.nr')):
            nr_pl = i + 1
            self.game_data.players.append({
                'name': self.game_data.game_config.get('player.name.{}'.format(nr_pl)),
                'size': self.game_data.game_config.get('player.size.{}'.format(nr_pl)),
                'speed_start': self.game_data.game_config.get('player.speed.start.{}'.format(nr_pl)),
                'speed_max': self.game_data.game_config.get('player.speed.max.{}'.format(nr_pl)),
                'speed_increase': self.game_data.game_config.get('player.speed.increase.{}'.format(nr_pl)),
                'speed_decrease': self.game_data.game_config.get('player.speed.decrease.{}'.format(nr_pl)),
                'falling_factor_increase': self.game_data.game_config.get('player.speed.fallingfactor.increase.{}'.format(nr_pl)),
                'rect_inner': self.game_data.game_config.get('player.rect.inner.{}'.format(nr_pl)),
                'orientation_left': self.game_data.game_config.get('player.orientationleft.{}'.format(nr_pl)),
                'idle': {
                    'key': 'sprite.player.idle.{}'.format(nr_pl),
                    'nr_images': self.game_data.game_config.get('player.nrimages.idle.{}'.format(nr_pl))
                },
                'run': {
                    'key': 'sprite.player.run.{}'.format(nr_pl),
                    'nr_images': self.game_data.game_config.get('player.nrimages.run.{}'.format(nr_pl))
                },
                'spreadsheet': None,
                'curr_img_index': 0,
                'image': None
            })

        _img_to_select = 'run'
        for player in self.game_data.players:
            player['spreadsheet'] = Spritesheet(self.game_data.sprite_cache, player[_img_to_select]['key'], size=player['size'], nr_images=player[_img_to_select]['nr_images'], orientation_left=player['orientation_left'])
            player['image'] = player['spreadsheet'].images_left[player['curr_img_index']]

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

        # Player Selection
        width = 500
        height = 70
        rect = (self.screen_mid[0] - width / 2, 0 + height / 2, width, height)
        item_playerselection = MenuItem(
                                self.game_data,
                                self.font_l,
                                rect,
                                (self.screen_mid[0], self.screen_size[1] / 2 - height * 2),
                                width=width,
                                height=height,
                                color=self.text_color,
                                rect_width=-1,
                                text=translate('menu.playerselection.txt')
                            )
        self.items.append(item_playerselection)

        width = 170
        height = 128
        start_width = -1 * width * 2
        start_height = -1 * height / 2
        for i, player in enumerate(self.game_data.players):
            rect = (self.screen_mid[0] + start_width, self.screen_mid[1] - 50 + start_height, width, height)
            item = ImageMenuItem(
                                self.game_data,
                                self.font_xs,
                                rect,
                                (rect[0] + width / 2, rect[1] + height / 2 + 25),
                                width=width,
                                height=height,
                                color=self.text_color,
                                rect_width=-1,
                                text=player['name'],
                                active=False,
                                image=player['image'],
                                play_sound_on_activation=True,
                                button_bg_width=width,
                                button_bg_height=height
                            )
            item.sound_played = True
            start_width += width
            if i == (int(len(self.game_data.players) / 2) - 1):
                start_width = -1 * width * 2
                start_height += height
            self.imageitems.append(item)

        # Random
        width = 300
        height = 65
        rect = (self.screen_mid[0] - width - 20, self.screen_mid[1] + height + 85, width, height)
        self.item_random = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0] - width / 2 - 20, self.screen_mid[1] + height + height / 2 + 90),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.random.txt'),
                                    active=False,
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.items.append(self.item_random)

        # Back
        width = 300
        height = 65
        rect = (self.screen_mid[0] + 20, self.screen_mid[1] + height + 85, width, height)
        self.item_back = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0] + width / 2 + 20, self.screen_mid[1] + height + height / 2 + 90),
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
                                    text=translate('menu.playerselection.help'),
                                    rotate=True,
                                    rotate_ticks_max=6,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def _update_selection(self, suppress_sound=False):
        self.item_back.active = self.curr_player_index == -2
        self.item_random.active = self.curr_player_index == -1

        for i, imageitem in enumerate(self.imageitems):
            imageitem.active = self.curr_player_index == i
            if suppress_sound:
                imageitem.sound_played = True

        if self.curr_player_index < -1:
            self.item_help.set_text(translate('menu.back.help'))
            self.item_help.rotate = False
        elif self.curr_player_index == -1:
            self.item_help.set_text(translate('menu.random.help'))
            self.item_help.rotate = False
        else:
            self.item_help.set_text(translate('menu.playerselection.help'))
            self.item_help.rotate = True

    def _keypress_arrow_up(self):
        # Logic only works for 8 players
        if self.curr_player_index < 0:
            if self.curr_player_index == -1:
                if self.last_valid_player_index >= 4 and self.last_valid_player_index <= 5:
                    self.curr_player_index = self.last_valid_player_index
                else:
                    self.curr_player_index = 5
            else:
                if self.last_valid_player_index >= 6 and self.last_valid_player_index <= 7:
                    self.curr_player_index = self.last_valid_player_index
                else:
                    self.curr_player_index = 6
        elif self.curr_player_index == 4:
            self.curr_player_index = 0
        elif self.curr_player_index == 5:
            self.curr_player_index = 1
        elif self.curr_player_index == 6:
            self.curr_player_index = 2
        elif self.curr_player_index == 7:
            self.curr_player_index = 3

        self._update_selection()

    def _keypress_arrow_down(self):
        # Logic only works for 8 players
        if self.curr_player_index >= 4 and self.curr_player_index <= 5:
            self.last_valid_player_index = self.curr_player_index
            self.curr_player_index = -1
        if self.curr_player_index >= 6 and self.curr_player_index <= 7:
            self.last_valid_player_index = self.curr_player_index
            self.curr_player_index = -2
        elif self.curr_player_index == 0:
            self.curr_player_index = 4
        elif self.curr_player_index == 1:
            self.curr_player_index = 5
        elif self.curr_player_index == 2:
            self.curr_player_index = 6
        elif self.curr_player_index == 3:
            self.curr_player_index = 7

        self._update_selection()

    def _keypress_arrow_left(self):
        # Logic only works for 8 players
        if self.curr_player_index == -2:
            self.curr_player_index = -1
        elif self.curr_player_index > 0:
            self.curr_player_index -= 1

        self._update_selection()

    def _keypress_arrow_right(self):
        # Logic only works for 8 players
        if self.curr_player_index == -1:
            self.curr_player_index = -2
        elif self.curr_player_index >= 0 and self.curr_player_index != 7:
            self.curr_player_index += 1

        self._update_selection()

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
                elif event.key == pygame.K_UP:
                    self._keypress_arrow_up()
                elif event.key == pygame.K_DOWN:
                    self._keypress_arrow_down()
                elif event.key == pygame.K_LEFT:
                    self._keypress_arrow_left()
                elif event.key == pygame.K_RIGHT:
                    self._keypress_arrow_right()
                elif event.key == pygame.K_RETURN:
                    if self.curr_player_index < -1:
                        self.set_state(State.MENU)
                    else:
                        self.game_data.scene_menu.stop_music()
                        if self.curr_player_index == -1:
                            self.game_data.player_index = random.randint(0, len(self.game_data.players) - 1)
                        else:
                            self.game_data.player_index = self.curr_player_index
                        self.game_data.check_reset_game()
                        self.set_state(State.GAME)

        if not self.is_state(State.PLAYERSELECTION):
            if self.is_state(State.MENU):
                self.curr_player_index = 0
                self._update_selection(suppress_sound=True)
            self.game_data.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            return
        else:
            self.game_data.scene_menu.start_music()

        if self.curr_player_index >= 0:
            imageitem = self.imageitems[self.curr_player_index]
            player = self.game_data.players[self.curr_player_index]
            player['curr_img_index'] += 1
            if player['curr_img_index'] >= len(player['spreadsheet'].images_left):
                player['curr_img_index'] = 0
            player['image'] = player['spreadsheet'].images_left[player['curr_img_index']]
            imageitem.image = player['image']

    def draw(self):
        """Draws the scene"""
        self.background.draw()

        for item in self.items:
            item.loop()
            item.draw()

        for imageitem in self.imageitems:
            imageitem.loop()
            imageitem.draw()
