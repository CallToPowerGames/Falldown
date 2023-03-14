#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Player"""

import logging
import random

import pygame

from game.GameState import State
from game.Direction import Direction
from game.sprites.Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    """The player"""

    def __init__(self, game_data, player_info):
        """Initializes the Player

        :param game_data: The game data
        :param player_info: The player info
        """
        super().__init__()

        logging.debug('Initializing player')

        self.game_data = game_data
        self.player_info = player_info

        self.screen = self.game_data.game_config.get('screen')
        self.size = self.player_info['size']
        self.speed_start = self.player_info['speed_start']
        self.speed = [self.speed_start[0], self.speed_start[1]]
        self.speed_max = self.player_info['speed_max']
        self.speed_increase = self.player_info['speed_increase']
        self.speed_decrease = self.player_info['speed_decrease']
        self.falling_factor_increase = self.player_info['falling_factor_increase']
        self.rect_inner = self.player_info['rect_inner']
        self.debug_show = self.game_data.game_config.get('debug.show')

        self.spritesheet_idle = Spritesheet(self.game_data.cache.sprite_cache, self.player_info['idle']['key'], size=self.player_info['size'], nr_images=self.player_info['idle']['nr_images'], orientation_left=self.player_info['orientation_left'])
        self.spritesheet_run = Spritesheet(self.game_data.cache.sprite_cache, self.player_info['run']['key'], size=self.player_info['size'], nr_images=self.player_info['run']['nr_images'], orientation_left=self.player_info['orientation_left'])
        self.curr_img_index = 0
        self.image = None

        self.current_key = None
        self._direction_til_stop = None
        self.falling_factor = 1
        self.falling = False
        self.last_direction_pressed = None
        self.last_direction = None
        self.position_midbottom = None

    def init(self, position_midbottom=(0, 0)):
        """Initializes the player"""
        self.position_midbottom = position_midbottom
        self.position_original = (self.position_midbottom[0], self.position_midbottom[1])
        self.position = (self.position_original[0], self.position_original[1])

        self.curr_img_index = 0
        self.image = self.spritesheet_idle.images_left[self.curr_img_index]
        self.position = (self.position_original[0], self.position_original[1])
        self.rect = self.image.get_rect(midbottom=self.position)

        self.last_direction = Direction.LEFT

        logging.info('Starting with player "{}"'.format(self.player_info['name']))

    def get_rect(self):
        """Returns the calculated rect

        :return: Calculated rect
        """
        return pygame.Rect(
                    self.rect.x + self.rect_inner[0],
                    self.rect.y + self.rect_inner[1],
                    self.rect.width - self.rect_inner[0] * 2,
                    self.rect.height - self.rect_inner[1] * 2
               )

    def _get_direction_pressed(self):
        """Returns the wanted direction

        :return: Wanted direction
        """
        if self.current_key and self.current_key == pygame.K_LEFT:
            return Direction.LEFT
        if self.current_key and self.current_key == pygame.K_RIGHT:
            return Direction.RIGHT

        return None

    def _speed_nearly_start_speed(self):
        """Checks whether the speed is nearly the start speed

        :return: Flag whether the speed is nearly the start speed
        """
        is_start_speed = self.speed[0] == self.speed_start[0]
        is_near_l = self.speed[0] >= self.speed_start[0] - self.speed_increase[0] / 2
        is_near_m = self.speed[0] <= self.speed_start[0] + self.speed_increase[0] / 2
        return is_start_speed or (is_near_l and is_near_m)

    def can_go_left(self):
        """Checks whether player can go left

        :return: Flag whether player can go left
        """
        direction_left_possible = self._direction_til_stop == Direction.LEFT
        return self._speed_nearly_start_speed() or direction_left_possible

    def can_go_right(self):
        """Checks whether player can go right

        :return: Flag whether player can go right
        """
        direction_right_possible = self._direction_til_stop == Direction.RIGHT
        return self._speed_nearly_start_speed() or direction_right_possible

    def is_going_left(self):
        """Checks whether the player is going left

        :return: Flag whether the player is going left
        """
        return self._direction_til_stop == Direction.LEFT

    def is_going_right(self):
        """Checks whether the player is going right

        :return: Flag whether the player is going right
        """
        return self._direction_til_stop == Direction.RIGHT

    def is_sliding(self):
        """Checks whether the player is sliding

        :return: Flag whether the player is sliding
        """
        direction_pressed = self._get_direction_pressed()
        return not self._speed_nearly_start_speed() and (not direction_pressed or (direction_pressed and self._direction_til_stop != direction_pressed))

    def reset_speed_x(self):
        """Resets the speed on x coordinate"""
        self.speed = [self.speed_start[0], self.speed[1]]
        self._direction_til_stop = None

    def half_speed_x(self):
        """Resets the speed on x coordinate"""
        new_speed = int(self.speed[0] / 2)
        if new_speed < self.speed_start[0]:
            new_speed = self.speed_start[0]
            self._direction_til_stop = None
        self.speed = [new_speed, self.speed[1]]

    def reset_speed_y(self):
        """Resets the speed on y coordinate"""
        self.speed = [self.speed[0], self.speed_start[1]]
        self.falling_factor = 1
        self.falling = False

    def is_falling(self):
        """Returns whether the player is falling

        :return: Flag whether the player is falling
        """
        return self.falling

    def is_moving(self):
        """Returns whether the player is moving

        :return: Flag whether the player is moving
        """
        return self._direction_til_stop != None

    def get_velocity(self, dt):
        """Returns the velocity

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        # Speed left/right
        if self.last_direction_pressed != None:
            self.last_direction = self.last_direction_pressed

        self.last_direction_pressed = self._get_direction_pressed()

        if self.current_key:
            if not self._direction_til_stop:
                self._direction_til_stop = self.last_direction_pressed
                self.curr_img_index = 0

        if not self.current_key and not self.is_moving() and not self.is_falling():
            return [0, 0]

        if self.current_key and self.last_direction_pressed == self._direction_til_stop:
            self.speed[0] += self.speed_increase[0]
        else:
            self.speed[0] -= self.speed_decrease

        if self.speed[0] < self.speed_start[0]:
            self.speed[0] = self.speed_start[0]
        if self.speed[0] > self.speed_max[0]:
            self.speed[0] = self.speed_max[0]

        if self._speed_nearly_start_speed():
            self._direction_til_stop = self.last_direction_pressed
            self.speed[0] = self.speed_start[0]
            self.curr_img_index = 0

        # Speed down
        if self.is_falling():
            self.speed[1] += self.speed_increase[1] * self.falling_factor
            self.falling_factor += self.falling_factor_increase

        if self.speed[1] > self.speed_max[1]:
            self.speed[1] = self.speed_max[1]

        return [
            self.speed[0] * dt,
            self.speed[1] * dt
        ]

    def update_sprite(self):
        """Updates the sprite"""
        _len = 0
        if self.is_sliding():
            if self._get_direction_pressed() == Direction.LEFT and self.is_going_right():
                _len = len(self.spritesheet_run.images_left)
                _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                self.image = self.spritesheet_run.images_left[_curr_img_index_safe]
            elif self._get_direction_pressed() == Direction.RIGHT and self.is_going_left():
                _len = len(self.spritesheet_run.images_right)
                _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                self.image = self.spritesheet_run.images_right[_curr_img_index_safe]
            else:
                if self.last_direction == Direction.RIGHT:
                    _len = len(self.spritesheet_idle.images_right)
                    _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                    self.image = self.spritesheet_idle.images_right[_curr_img_index_safe]
                else:
                    _len = len(self.spritesheet_idle.images_left)
                    _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                    self.image = self.spritesheet_idle.images_left[_curr_img_index_safe]
        else:
            if self.is_going_left():
                _len = len(self.spritesheet_run.images_left)
                _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                self.image = self.spritesheet_run.images_left[_curr_img_index_safe]
            elif self.is_going_right():
                _len = len(self.spritesheet_run.images_right)
                _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                self.image = self.spritesheet_run.images_right[_curr_img_index_safe]
            else:
                if self.last_direction == Direction.RIGHT:
                    _len = len(self.spritesheet_idle.images_right)
                    _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                    self.image = self.spritesheet_idle.images_right[_curr_img_index_safe]
                else:
                    _len = len(self.spritesheet_idle.images_left)
                    _curr_img_index_safe = self.curr_img_index if self.curr_img_index < _len else 0
                    self.image = self.spritesheet_idle.images_left[_curr_img_index_safe]

        self.curr_img_index += 1
        if self.curr_img_index >= _len:
            self.curr_img_index = 0

    def draw(self):
        """Draws the player"""
        self.screen.blit(self.image, (self.rect.topleft[0], self.rect.topleft[1] + self.rect_inner[1]))

        if self.debug_show:
            pygame.draw.rect(
                self.screen,
                (200, 50, 50),
                self.get_rect(),
                width=1
            )

            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                self.rect,
                width=1
            )
