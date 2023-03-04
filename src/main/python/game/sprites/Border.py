#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Border"""

import logging

import pygame

from game.sprites.Spritesheet import Spritesheet

class Border(pygame.sprite.Sprite):
    """The border"""

    def __init__(self, game_data):
        """Initializes the border

        :param game_data: The game data
        """
        super().__init__()

        logging.debug('Initializing border')

        self.game_data = game_data

        self.screen = self.game_data.game_config.get('screen')
        self.offset_max_left = self.game_data.game_config.get('offset.max.left')
        self.offset_max_right = self.game_data.game_config.get('offset.max.right')
        self.offset_max_up = self.game_data.game_config.get('offset.max.up')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.camera_borders = self.game_data.game_config.get('camera.borders')
        self.border_color = self.game_data.game_config.get('border.color')
        self.border_size = self.game_data.game_config.get('level.border.img.size')

        self.spritesheet_border = Spritesheet(self.game_data.sprite_cache, 'level.border', self.border_size, 1, generate_sides=False)

        self.image_border = None

        self._init()

    def _init(self):
        """Initializes the border"""
        logging.debug("Initializing the border")

        self.image_border = self.spritesheet_border.images_left[0]

    def draw(self, offset):
        """Draws the border

        :param offset: The offset
        """
        if abs(self.offset_max_left - offset.x) < self.camera_borders['left']:
            # Left border
            pygame.draw.rect(
                self.screen,
                self.border_color,
                pygame.Rect(
                    self.offset_max_left - offset.x,
                    self.offset_max_up,
                    self.camera_borders['left'],
                    self.screen_size[1]
                ),
                width=0
            )
            startpoint_y = 0
            while (startpoint_y + self.image_border.get_height()) <= offset.y:
                startpoint_y += self.image_border.get_height()
            curr_y = startpoint_y - offset.y
            for i in range(int(self.screen_size[1] / self.image_border.get_height()) + 2):
                curr_x = self.offset_max_left + self.camera_borders['left'] - self.image_border.get_width() - offset.x
                while (curr_x + self.image_border.get_width()) >= self.offset_max_left - offset.x:
                    self.screen.blit(self.image_border,
                        pygame.Rect(
                            curr_x,
                            curr_y,
                            self.image_border.get_width(),
                            self.image_border.get_height()
                        )
                    )
                    curr_x -= self.image_border.get_width()
                curr_y += self.image_border.get_height()

        if abs(self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x) < (self.screen_size[0] + self.camera_borders['left'] - self.camera_borders['right']):
            # Right border
            pygame.draw.rect(
                self.screen,
                self.border_color,
                pygame.Rect(
                    self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x,
                    self.offset_max_up,
                    self.camera_borders['right'],
                    self.screen_size[1]
                ),
                width=0
            )
            startpoint_y = 0
            while (startpoint_y + self.image_border.get_height()) <= offset.y:
                startpoint_y += self.image_border.get_height()
            curr_y = startpoint_y - offset.y
            for i in range(int(self.screen_size[1] / self.image_border.get_height()) + 2):
                curr_x = self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x
                while curr_x <= (self.offset_max_right + (self.image_border.get_width() / 2)):
                    self.screen.blit(self.image_border,
                        pygame.Rect(
                            curr_x,
                            curr_y,
                            self.image_border.get_width(),
                            self.image_border.get_height()
                        )
                    )
                    curr_x += self.image_border.get_width()
                curr_y += self.image_border.get_height()
