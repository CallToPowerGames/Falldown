#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Cloud"""

import logging
import random

import pygame

from game.GameState import State
from game.Direction import Direction
from game.sprites.Spritesheet import Spritesheet

class Cloud(pygame.sprite.Sprite):
    """A cloud"""

    def __init__(self, game_data, image, startpoint, size, speed_min, speed_max):
        """Initializes the cloud

        :param game_data: The game data
        :param image: The image
        :param startpoint: The startpoint
        :param size: The size
        :param speed_min: The min speed
        :param speed_max: max The speed
        """
        super().__init__()

        # logging.debug('Initializing cloud')

        self.game_data = game_data

        self.screen = self.game_data.game_config.get('screen')

        self.image = image
        self.startpoint = startpoint
        self.size = size

        self.rect = self.image.get_rect(midbottom=self.startpoint)
        self.speed = random.randint(speed_min, speed_max)

    def get_curr_x(self):
        return self.startpoint[0]

    def loop(self, dt):
        self.startpoint = [self.startpoint[0] - (self.speed * dt + 1), self.startpoint[1]]

    def draw(self, offset=pygame.math.Vector2(0, 0)):
        """Draws the background"""
        self.screen.blit(self.image,
            pygame.Rect(
                self.startpoint[0] - offset.x,
                self.startpoint[1] - offset.y,
                self.size[0],
                self.size[1]
            )
        )
