#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Segment"""

import logging

import pygame

class Segment():
    """A segment"""

    def __init__(self, game_config, images, spritesheet_propeller, startpoint, width, height, moving=False):
        """Initializes the segment

        :param game_config: The game config
        :param images: The images (left, mid, right)
        :param spritesheet_propeller: The propeller spritesheet
        :param startpoint: The start point
        :param width: The width
        :param height: The height
        :param moving: Flag whether the line moves
        """
        # logging.debug('Initializing segment')

        self.game_config = game_config
        self.startpoint = startpoint
        self.width = width
        self.height = height
        self.moving = moving
        self.images = images
        self.spritesheet_propeller = spritesheet_propeller

        self.debug_show = self.game_config.get('debug.show')
        self.screen = self.game_config.get('screen')
        self.move_speed = self.game_config.get('level.segments.move.speed')
        self.move_max = self.game_config.get('level.segments.move.max')

        self.image_propeller = None
        self.curr_img_propeller = 0

        self.curr_update_propeller = 0
        self.update_propeller = 3

        self.operator = 1
        self.curr_speed = 0

        self._init()

    def _init(self):
        """Initializes the segment"""
        logging.debug("Initializing the level")
        self.image_propeller = self.spritesheet_propeller.images_left[self.curr_img_propeller]

    def __str__(self):
        """toString"""
        return 'Segment[startpoint={}, width={}, height={}]'.format(self.startpoint, self.width, self.height)

    def get_startpoint_with_offset(self, offset):
        """Returns the startpoint including the given offset

        :param offset: The offset
        :return: The startpoint including the given offset
        """
        return [self.startpoint[0] - offset[0], self.startpoint[1] - offset[1]]

    def get_speed(self):
        """Returns the speed. Does not change any variables.

        :return: The speed
        """
        return self.curr_speed

    def get_next_startpoint(self, dt):
        """Returns the next startpoint

        :param dt: Tick rate, milliseconds between each call to 'tick'
        :return: The next startpoint
        """
        if self.moving:
            operator = self.operator
            if abs(self.curr_speed) >= self.move_max:
                operator *= -1
            curr_speed = self.curr_speed + self.move_speed * operator
            return [self.startpoint[0] + curr_speed * dt, self.startpoint[1]]
        else:
            return [self.startpoint[0], self.startpoint[1]]

    def get_next_startpoint_with_offset(self, dt, offset):
        """Returns the next startpoint including the given offset

        :param dt: Tick rate, milliseconds between each call to 'tick'
        :param offset: The offset
        :return: The next startpoint including the given offset
        """
        startpoint = self.get_next_startpoint(dt)
        return [startpoint[0] - offset[0], startpoint[1] - offset[1]]

    def loop_visuals(self, dt):
        """Loops only the visual parts of the level

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        if self.curr_update_propeller > self.update_propeller:
            self.curr_update_propeller = 0
            self.image_propeller = self.spritesheet_propeller.images_left[self.curr_img_propeller]
            self.curr_img_propeller += 1
            if self.curr_img_propeller >= len(self.spritesheet_propeller.images_left):
                self.curr_img_propeller = 0
        else:
            self.curr_update_propeller += 1

    def loop(self, dt):
        """Updates the line

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        self.loop_visuals(dt)

        if self.moving:
            if abs(self.curr_speed) >= self.move_max:
                self.operator *= -1
            self.curr_speed = self.curr_speed + self.move_speed * self.operator
            self.startpoint = [self.startpoint[0] + self.curr_speed * dt, self.startpoint[1]]

    def draw(self, offset):
        """Draws the segment

        :param offset: The offset
        """
        self.screen.blit(self.images[0],
            pygame.Rect(
                self.startpoint[0] - offset.x,
                self.startpoint[1] - offset.y,
                self.images[0].get_width(),
                self.images[0].get_height()
            )
        )

        segment_width = self.images[0].get_width()
        max_size = self.width - self.images[2].get_width()
        while (segment_width + self.images[1].get_width()) <= max_size:
            self.screen.blit(self.images[1], 
                pygame.Rect(
                        self.startpoint[0] + segment_width - offset.x,
                        self.startpoint[1] - offset.y,
                        self.images[1].get_width(),
                        self.images[1].get_height()
                    )
                )
            segment_width += self.images[1].get_width()
        rect = pygame.Rect(
                    self.startpoint[0] + segment_width - offset.x,
                    self.startpoint[1] - offset.y,
                    max_size - segment_width,
                    self.images[1].get_height()
                )
        self.screen.blit(self.images[1], rect) # , rect

        self.screen.blit(self.images[2], 
            pygame.Rect(
                self.startpoint[0] + self.width - self.images[2].get_width() - offset.x,
                self.startpoint[1] - offset.y,
                self.images[2].get_width(),
                self.images[2].get_height()
            )
        )

        self.screen.blit(self.image_propeller, 
            pygame.Rect(
                self.startpoint[0] + (self.width / 2) - (self.image_propeller.get_width() / 2) - offset.x,
                self.startpoint[1] + (self.images[0].get_height() / 2) + self.image_propeller.get_height() - offset.y,
                self.image_propeller.get_width(),
                self.image_propeller.get_height(),
            )
        )
