#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""PlayerMenuItem"""

import logging

import pygame

from i18n.Translations import translate
from game.drawables.Drawable import Drawable
from game.drawables.DrawableUtils import draw_text_in_rect

class PlayerMenuItem(Drawable):
    """A Image"""

    def __init__(self,
                    game_data,
                    player,
                    font,
                    rect,
                    center,
                    width,
                    height,
                    color=(255, 255, 255),
                    color_inactive=(0, 0, 0),
                    rotate=False,
                    rotate_ticks_max=6,
                    active=True,
                    rect_width=5,
                    play_sound_on_activation=False,
                    button_bg_width=64,
                    button_bg_height=64
                ):
        """Initializes the PlayerMenuItem

        :param game_data: The game data
        :param player: The player
        :param font: The font
        :param rect: The rectangle
        :param center: The center of the rect
        :param width: The width
        :param height: The height
        :param color: The color
        :param color_inactive: The color when inactive
        :param rotate: Whether to rotate text
        :param rotate_ticks_max: Rotate ticks max
        :param active: Whether item is active or not
        :param rect_width: The rect width
        :param play_sound_on_activation: Flag whether to play a sound on activation
        :param button_bg_width: Button background width
        :param button_bg_height: Button background height
        """
        logging.debug('Initializing PlayerMenuItem')

        self.game_data = game_data
        self.player = player
        self.game_config = self.game_data.game_config
        self.font = font
        self.rect = rect
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.color_inactive = color_inactive
        self.rotate = rotate
        self.rotate_ticks_max = rotate_ticks_max
        self.active = active
        self.rect_width = rect_width
        self.play_sound_on_activation = play_sound_on_activation
        self.button_bg_width = button_bg_width
        self.button_bg_height = button_bg_height

        self.screen = self.game_config.get('screen')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.image_button_active = pygame.transform.scale(self.game_data.cache.sprite_cache.get('imagebutton.active').convert_alpha(), (self.button_bg_width, self.button_bg_height))
        self.image_button_inactive = pygame.transform.scale(self.game_data.cache.sprite_cache.get('imagebutton.inactive').convert_alpha(), (self.button_bg_width, self.button_bg_height))

        self.text = self.player['name']
        self.image = self.player['image']

        self.tick_current = 0
        self.sound_played = False
        self._show_info = False
        self.text_current = ''
        self.text_current_arr = []

        self._init()

    def _init(self):
        """Initiailizes the object"""
        self.reset_text()

        ljust_val = 50
        self.text_current_arr.append('{}'.format(self.player['name']))
        self.text_current_arr.append(translate('menu.item.player.speed.start').format(self.player['speed_start'][0], self.player['speed_start'][1]).ljust(ljust_val))
        self.text_current_arr.append(translate('menu.item.player.speed.max').format(self.player['speed_max'][0], self.player['speed_max'][1]).ljust(ljust_val))
        self.text_current_arr.append(translate('menu.item.player.speed.increase').format(self.player['speed_increase'][0], self.player['speed_increase'][1]).ljust(ljust_val))
        self.text_current_arr.append(translate('menu.item.player.speed.decrease').format(self.player['speed_decrease']).ljust(ljust_val))
        self.text_current_arr.append(translate('menu.item.player.falling.increase').format(self.player['falling_factor_increase']).ljust(ljust_val))

    def reset_text(self):
        """Resets rotated to saved text"""
        self.text_current = '{}{}'.format(self.text, ' ')

    def set_text(self, text):
        """
        Sets a new text

        :param text: Text to set
        """
        self.text = text
        self.reset_text()

    def show_info(self, _show_info):
        """Whether to show the name or info

        :param show_info: Flag whether to show the name or info
        """
        self._show_info = _show_info
        self.reset_text()

    def loop(self):
        """Updates the PlayerMenuItem"""
        if self.active:
            if self.play_sound_on_activation and not self.sound_played:
                self.game_data.cache.sound_cache.play('menuitem.activate', volume=self.music_volume_bg_menu_effects)
                self.sound_played = True
                pass
            if self.rotate:
                self.tick_current = self.tick_current + 1
                if self.tick_current > self.rotate_ticks_max:
                    self.tick_current = 0
        else:
            self.sound_played = False

    def draw(self):
        """Draws the PlayerMenuItem"""
        if self.rotate and self.active and self.tick_current == 0:
            self.text_current = self.text_current[1:] + self.text_current[0]

        if self.active:
            self.screen.blit(self.image_button_active, self.rect)
        else:
            self.screen.blit(self.image_button_inactive, self.rect)

        _color = self.color if self.active else self.color_inactive
        if self._show_info:
            self.screen.blit(self.image, (
                self.rect[0] + self.button_bg_width / 2 - self.image.get_width() / 2,
                self.rect[1],
                self.image.get_width(),
                self.image.get_height()
            ))

            y_start = -45
            y_increase = 12
            for e in self.text_current_arr:
                draw_text_in_rect(self.screen, e, _color, self.font, (
                    self.rect[0] + 5,
                    self.rect[1] + y_start,
                    self.rect[2] - 10,
                    self.rect[3]
                ), (self.center[0] + 5, self.center[1] + y_start))
                y_start += y_increase
        else:
            self.screen.blit(self.image, (
                self.rect[0] + self.button_bg_width / 2 - self.image.get_width() / 2,
                self.rect[1] + 30,
                self.image.get_width(),
                self.image.get_height()
            ))

            draw_text_in_rect(self.screen, self.text_current, _color, self.font, (
                self.rect[0] + 5,
                self.rect[1],
                self.rect[2] - 10,
                self.rect[3]
            ), self.center)
