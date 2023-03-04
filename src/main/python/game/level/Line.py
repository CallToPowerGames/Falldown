#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Line"""

import logging

class Line():
    """A line"""

    def __init__(self, game_config, moving=False):
        """Initializes the line

        :param game_config: The game config
        :param moving: Flag whether the line moves
        """
        # logging.info('Initializing line')

        self.game_config = game_config
        self.moving = moving

        self.screen_size = self.game_config.get('screen.size')
        self.segments = []

    def get_startpoint_y(self):
        """Returns the startpoint y

        :return: The startpoint y
        """
        return self.segments[0].startpoint[1] if len(self.segments) > 0 else -1

    def add(self, segment):
        """Adds a segment to the level

        :param segment: The segment to be added
        """
        self.segments.append(segment)

    def loop_visuals(self, dt):
        """Loops only the visual parts of the level

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        for segment in self.segments:
            segment.loop_visuals(dt)

    def loop(self, dt):
        """Updates the line

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        for segment in self.segments:
            segment.loop(dt)

    def draw(self, offset):
        """Draws the level

        :param offset: The offset
        """
        for segment in self.segments:
            x_left_in_screen = (segment.startpoint[0] + segment.width) > offset.x
            x_right_in_screen = (segment.startpoint[0] - offset.x) < self.screen_size[0]
            y_in_screen = (segment.startpoint[1] + segment.height) > offset.y
            if x_left_in_screen and x_right_in_screen and y_in_screen:
                segment.draw(offset)
