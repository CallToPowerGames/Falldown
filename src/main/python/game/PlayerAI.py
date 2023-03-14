#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Player AI"""

import logging
import random

import pygame

from game.Direction import Direction

class PlayerAI():
    """The player AI"""

    def __init__(self, game_data, player, level, camera):
        """Initializes the Player AI

        :param game_data: The game data
        :param player: The player
        :param level: The level
        :param camera: The camera
        """
        logging.debug('Initializing player AI')

        self.game_data = game_data
        self.player = player
        self.level = level
        self.camera = camera

        self.offset_max_left = self.game_data.game_config.get('offset.max.left')
        self.offset_max_right = self.game_data.game_config.get('offset.max.right')

        self.current_direction = Direction.LEFT
        self.is_falling = False

        self.keys_pressed = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }

    def loop(self):
        """Loops the AI

        :return the keys pressed
        """
        last_direction = self.current_direction

        do_pause = False
        if self.player.falling:
            if not self.is_falling:
                self.is_falling = True
                if random.random() < 0.8:
                    if self.current_direction == Direction.LEFT:
                        self.current_direction = Direction.RIGHT
                    else:
                        self.current_direction = Direction.LEFT
                do_pause = True
        else:
            self.is_falling = False

        if do_pause:
            self.keys_pressed[pygame.K_RIGHT] = False
            self.keys_pressed[pygame.K_LEFT] = False
            return self.keys_pressed

        if self.current_direction == Direction.LEFT:
            if self.camera.offset.x > self.offset_max_left:
                self.keys_pressed[pygame.K_RIGHT] = False
                self.keys_pressed[pygame.K_LEFT] = True
            else:
                self.current_direction = Direction.RIGHT
        elif self.current_direction == Direction.RIGHT:
            if self.camera.offset.x < self.offset_max_right:
                self.keys_pressed[pygame.K_LEFT] = False
                self.keys_pressed[pygame.K_RIGHT] = True
            else:
                self.current_direction = Direction.LEFT

        return self.keys_pressed
