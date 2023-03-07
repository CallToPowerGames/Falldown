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

    def __init__(self, game_config, images, spritesheet_propeller, spritesheet_clear_linesegment, spritesheet_clear_all, startpoint, width, height, moving=False, clear_linesegment=False, clear_all=False):
        """Initializes the segment

        :param game_config: The game config
        :param images: The images (left, mid, right)
        :param spritesheet_propeller: The propeller spritesheet
        :param spritesheet_clear_linesegment: The clear line spritesheet
        :param spritesheet_clear_all: The clear all spritesheet
        :param startpoint: The start point
        :param width: The width
        :param height: The height
        :param moving: Flag whether the line moves
        :param clear_linesegment: Flag whether has element to clear the line
        :param clear_all: Flag whether has element to clear all lines
        """
        # logging.debug('Initializing segment')

        self.game_config = game_config
        self.images = images
        self.spritesheet_propeller = spritesheet_propeller
        self.spritesheet_clear_linesegment = spritesheet_clear_linesegment
        self.spritesheet_clear_all = spritesheet_clear_all
        self.startpoint = startpoint
        self.width = width
        self.height = height
        self.moving = moving
        self.clear_linesegment = clear_linesegment
        self.clear_all = clear_all

        self.debug_show = self.game_config.get('debug.show')
        self.screen = self.game_config.get('screen')
        self.move_speed = self.game_config.get('level.segments.move.speed')
        self.move_max = self.game_config.get('level.segments.move.max')

        self.image_propeller = None
        self.curr_img_propeller = 0
        self.curr_update_propeller = 0
        self.update_propeller = 3

        self.image_clear_linesegment = None
        self.curr_img_clear_linesegment = 0
        self.curr_update_clear_linesegment = 0
        self.update_clear_linesegment = 4

        self.image_clear_all = None
        self.curr_img_clear_all = 0
        self.curr_update_clear_all = 0
        self.update_clear_all = 5

        self.operator = 1
        self.curr_speed = 0

        self._init()

    def _init(self):
        """Initializes the segment"""
        logging.debug("Initializing the segment")
        self.image_propeller = self.spritesheet_propeller.images_left[self.curr_img_propeller]
        self.image_clear_linesegment = self.spritesheet_clear_linesegment.images_left[self.curr_img_clear_linesegment]
        self.image_clear_all = self.spritesheet_clear_all.images_left[self.curr_img_clear_all]

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

    def rotate_img_center(self, image, angle):
        """Rotate a square (!) image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        return rot_image

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

        if self.curr_update_clear_linesegment > self.update_clear_linesegment:
            self.curr_update_clear_linesegment = 0
            self.image_clear_linesegment = self.spritesheet_clear_linesegment.images_left[self.curr_img_clear_linesegment]
            self.curr_img_clear_linesegment += 1
            if self.curr_img_clear_linesegment >= len(self.spritesheet_clear_linesegment.images_left):
                self.curr_img_clear_linesegment = 0
        else:
            self.curr_update_clear_linesegment += 1
        

        if self.curr_update_clear_all > self.update_clear_all:
            self.curr_update_clear_all = 0
            self.image_clear_all = self.spritesheet_clear_all.images_left[self.curr_img_clear_all]
            self.curr_img_clear_all += 1
            if self.curr_img_clear_all >= len(self.spritesheet_clear_all.images_left):
                self.curr_img_clear_all = 0
        else:
            self.curr_update_clear_all += 1

    def rot_center(self, image, angle, x, y):
        
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

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

        if self.clear_linesegment:
            pass
        elif self.clear_all:
            pass

    def get_clear_linesegment_rect(self, offset):
        """Returns a rect for the clear line object

        :param offset: The offset
        """
        return pygame.Rect(
                    self.startpoint[0] + (self.width / 2) - (self.image_clear_linesegment.get_width() / 2) - offset.x,
                    self.startpoint[1] + (self.images[0].get_height() / 2) - self.image_clear_linesegment.get_height() - 2 - offset.y,
                    self.image_clear_linesegment.get_width(),
                    self.image_clear_linesegment.get_height()
                )

    def get_clear_all_rect(self, offset):
        """Returns a rect for the clear all object

        :param offset: The offset
        """
        return pygame.Rect(
                    self.startpoint[0] + (self.width / 2) - (self.image_clear_all.get_width() / 2) - offset.x,
                    self.startpoint[1] + (self.images[0].get_height() / 2) - self.image_clear_all.get_height() - 5 - offset.y,
                    self.image_clear_all.get_width(),
                    self.image_clear_all.get_height()
                )

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

        if self.clear_linesegment:
            rect = self.get_clear_linesegment_rect(offset)
            if self.debug_show:
                pygame.draw.rect(self.screen, (200, 50, 50), rect, width=1)
            self.screen.blit(self.image_clear_linesegment, rect)
        elif self.clear_all:
            rect = self.get_clear_all_rect(offset)
            if self.debug_show:
                pygame.draw.rect(self.screen, (200, 50, 50), rect, width=1)
            self.screen.blit(self.image_clear_all, rect)
