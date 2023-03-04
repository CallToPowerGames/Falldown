#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Line"""

import logging

import pygame

from game.drawables.Drawable import Drawable
from game.drawables.DrawableUtils import draw_text_in_rect

class Line(Drawable):
    """A Line"""

    def __init__(self, game_config, start_point, end_point, width=5, color=(255, 255, 255)):
        """Initializes the Line

        :param game_config: The game config
        :param start_point: The starting point
        :param end_point: The ending point
        :param width: The width
        :param color: The color
        """
        logging.debug('Initializing Line')

        self.game_config = game_config
        self.start_point = start_point
        self.end_point = end_point
        self.width = width
        self.color = color

        self.screen = self.game_config.get('screen')

    def loop(self):
        """Updates the Line"""
        pass

    def draw(self):
        """Draws the Line"""
        pygame.draw.line(
            self.screen,
            self.color,
            self.start_point,
            self.end_point,
            self.width
        )
