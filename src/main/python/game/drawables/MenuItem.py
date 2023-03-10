#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""MenuItem"""

import logging

import pygame

from game.drawables.Drawable import Drawable
from game.drawables.DrawableUtils import draw_text_in_rect

class MenuItem(Drawable):
    """A MenuItem"""

    def __init__(self,
                    game_data,
                    font,
                    rect,
                    center,
                    width,
                    height,
                    color=(255, 255, 255),
                    color_inactive=(0, 0, 0),
                    text='',
                    rotate=False,
                    rotate_ticks_max=6,
                    active=True,
                    rect_width=5,
                    play_sound_on_activation=False,
                    button_none=False,
                    button=False,
                    banner=False
                ):
        """Initializes the MenuItem

        :param game_data: The game data
        :param font: The font
        :param rect: The rectangle
        :param center: The center of the rect
        :param width: The width
        :param height: The height
        :param color: The color
        :param color_inactive: The color when inactive
        :param text: The text
        :param rotate: Whether to rotate text
        :param rotate_ticks_max: Rotate ticks max
        :param active: Whether item is active or not
        :param rect_width: The rect width
        :param play_sound_on_activation: Flag whether to play a sound on activation
        :param button_none: Whether to draw a button none
        :param button: Whether to draw a button
        :param banner: Whether to draw a banner
        """
        logging.debug('Initializing MenuItem')

        self.game_data = game_data
        self.game_config = self.game_data.game_config
        self.font = font
        self.rect = rect
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.color_inactive = color_inactive
        self.text = text
        self.rotate = rotate
        self.rotate_ticks_max = rotate_ticks_max
        self.active = active
        self.rect_width = rect_width
        self.play_sound_on_activation = play_sound_on_activation
        self.button_none = button_none
        self.button = button
        self.banner = banner

        self.screen = self.game_config.get('screen')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        if self.button_none:
            self.image_button_none = pygame.transform.scale(self.game_data.cache.sprite_cache.get('button.none').convert_alpha(), (self.width, self.height))
        if self.button:
            self.image_button_active = pygame.transform.scale(self.game_data.cache.sprite_cache.get('button.active').convert_alpha(), (self.width, self.height))
            self.image_button_inactive = pygame.transform.scale(self.game_data.cache.sprite_cache.get('button.inactive').convert_alpha(), (self.width, self.height))
        elif self.banner:
            self.image_banner = pygame.transform.scale(self.game_data.cache.sprite_cache.get('banner').convert_alpha(), (self.width, self.height))

        self.tick_current = 0
        self.sound_played = False

        self.text_current = '{}{}'.format(self.text, ' ')

    def reset_text(self):
        """Resets rotated to saved text"""
        self.text_current = '{}{}'.format(self.text, ' ')

    def set_text(self, text):
        """
        Sets a new text

        :param text: Text to set
        """
        self.text = text
        self.text_current = '{}{}'.format(self.text, ' ')

    def loop(self):
        """Updates the MenuItem"""
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

    def draw(self, alpha=255):
        """Draws the MenuItem

        :param alpha: The alpha value
        """
        if self.rotate and self.active and self.tick_current == 0:
            self.text_current = self.text_current[1:] + self.text_current[0]

        if self.button_none:
            if alpha < 255:
                self.image_button_none.set_alpha(alpha)
            self.screen.blit(self.image_button_none, self.rect)
        if self.button:
            if alpha < 255:
                self.image_button_active.set_alpha(alpha)
            self.screen.blit(self.image_button_active if self.active else self.image_button_inactive, self.rect)
        if self.banner:
            if alpha < 255:
                self.image_banner.set_alpha(alpha)
            self.screen.blit(self.image_banner, self.rect)

        _color = self.color if self.active else self.color_inactive
        corr = 20
        draw_text_in_rect(self.screen, self.text_current, _color, self.font, (
            self.rect[0] + corr,
            self.rect[1],
            self.rect[2] - corr,
            self.rect[3]
        ), self.center, alpha=alpha)
