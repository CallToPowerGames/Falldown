#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Level"""

import logging
import random

import pygame

from game.level.Line import Line
from game.level.Segment import Segment
from game.sprites.Spritesheet import Spritesheet

class Level():
    """The level"""

    def __init__(self, game_data):
        """Initializes the level

        :param game_data: The game data
        """
        logging.info('Initializing level')

        self.game_data = game_data

        self.screen_size = self.game_data.game_config.get('screen.size')
        self.min_x = self.game_data.game_config.get('offset.max.left') * self.game_data.game_config.get('level.generator.modifier')
        self.max_x = self.game_data.game_config.get('offset.max.right') * self.game_data.game_config.get('level.generator.modifier')
        self.gap_min = self.game_data.game_config.get('level.segments.gap.min')
        self.gap_add_max = self.game_data.game_config.get('level.segments.gap.add.max')
        self.segment_height = self.game_data.game_config.get('level.segments.height')
        self.gap_vert_min = self.game_data.game_config.get('level.segments.gap.vert.min')
        self.gap_vert_add_max = self.game_data.game_config.get('level.segments.gap.vert.add.max')
        self.line_moving_probability = self.game_data.game_config.get('level.line.moving.probability')
        self.segments_width_min = self.game_data.game_config.get('level.segments.width.min')
        self.segments_width_max = self.game_data.game_config.get('level.segments.width.max')
        self.segment_img_left_size = self.game_data.game_config.get('level.segment.img.left.size')
        self.segment_img_left_startpoint = self.game_data.game_config.get('level.segment.img.left.startpoint')
        self.segment_img_mid_size = self.game_data.game_config.get('level.segment.img.mid.size')
        self.segment_img_mid_startpoint = self.game_data.game_config.get('level.segment.img.mid.startpoint')
        self.segment_img_right_size = self.game_data.game_config.get('level.segment.img.right.size')
        self.segment_img_right_startpoint = self.game_data.game_config.get('level.segment.img.right.startpoint')
        self.segment_img_propeller_size = self.game_data.game_config.get('level.segment.img.propeller.size')
        self.segment_img_propeller_startpoint = self.game_data.game_config.get('level.segment.img.propeller.startpoint')
        self.collision_detection_correction_left = self.game_data.game_config.get('level.collision.detection.correction.left')
        self.collision_detection_correction_right = self.game_data.game_config.get('level.collision.detection.correction.right')
        self.collision_detection_correction_bottom = self.game_data.game_config.get('level.collision.detection.correction.bottom')

        self.spritesheet_segment_left = Spritesheet(self.game_data.sprite_cache, 'level.segment', size=self.segment_img_left_size, nr_images=1, startpoint=self.segment_img_left_startpoint, generate_sides=False)
        self.spritesheet_segment_mid = Spritesheet(self.game_data.sprite_cache, 'level.segment', size=self.segment_img_mid_size, nr_images=1, startpoint=self.segment_img_mid_startpoint, generate_sides=False)
        self.spritesheet_segment_right = Spritesheet(self.game_data.sprite_cache, 'level.segment', size=self.segment_img_right_size, nr_images=1, startpoint=self.segment_img_right_startpoint, generate_sides=False)
        self.spritesheet_segment_propeller = Spritesheet(self.game_data.sprite_cache, 'level.segment.propeller', size=self.segment_img_propeller_size, nr_images=4, startpoint=self.segment_img_propeller_startpoint, generate_sides=False)

        self.image_segment_right = None
        self.image_segment_mid = None
        self.image_segment_left = None

        self._lines = []
        self.last_y = -1

        self._init()

    def _init(self):
        """Initializes the level"""
        logging.debug("Initializing the level")
        self.image_segment_right = self.spritesheet_segment_right.images_left[0]
        self.image_segment_mid = self.spritesheet_segment_mid.images_left[0]
        self.image_segment_left = self.spritesheet_segment_left.images_left[0]

    def reset(self):
        """Resets the level"""
        self._lines = []
        self.last_y = -1

    def size(self):
        """Returns the current level size (number of lines)

        :return: the current level size (number of lines)
        """
        return len(self._lines)

    def add(self, line):
        """Adds a line to the level

        :param line: The line to be added
        """
        self._lines.append(line)

    def get(self, index):
        """Returns a line at index

        :param index: The index
        :return: Line at index
        """
        return self._lines[index]

    def clean(self, offset_y):
        """Cleans the level, removes all lines much above the offset

        :param offset_y: The offset
        """
        self._lines = [line for line in self._lines if line.get_startpoint_y() >= offset_y]

    def generate_new_line(self):
        """Generates a new line
        
        :return: The new line
        """
        moving = random.randint(0, 100) < self.line_moving_probability
        line = Line(self.game_data.game_config, moving=moving)

        if self.last_y < 0:
            self.last_y = 100
        else:
            self.last_y += self.segment_height + self.gap_vert_min + random.randint(0, self.gap_vert_add_max)
        startpoint_last = (self.min_x, self.last_y)
        width_last = 0

        cnt = 0
        reached_end = False
        while not reached_end:
            cnt += 1
            startpoint = (
                startpoint_last[0] + width_last + self.gap_min + random.randint(0, self.gap_add_max),
                startpoint_last[1]
            )
            width = random.randint(self.segments_width_min, self.segments_width_max)
            height = self.segment_height
            images_segment = [self.image_segment_left, self.image_segment_mid, self.image_segment_right]
            segment = Segment(self.game_data.game_config, images_segment, self.spritesheet_segment_propeller, startpoint, width, height, moving=moving)
            line.add(segment)
            startpoint_last = startpoint
            width_last = width
            reached_end = (cnt > 1000) or (abs(self.min_x) + self.max_x - (startpoint_last[0] + width_last + self.gap_min + self.gap_add_max) <= 0)
        self.add(line)

        return line

    def collides_with(self, player, dt, velocity, keys, offset):
        """Checks whether a level segment collides with the player

        :param player: The player
        :param dt: Tick rate, milliseconds between each call to 'tick'
        :param velocity: Calculated velocity
        :param keys: The keys
        :param offset: The offset
        :return: Tuple of <collides with a segment> and corrections/information:
                 <CollidesBottom>, <CollidesLeft>, <CollidesRight>, <SegmentTopY>, <SegmentRightX>, <SegmentLeftX>, <StandsOnMovingSegment>, <SegmentSpeed>
        """
        plus_right = velocity[0] if player.is_moving() else 0
        minus_left = velocity[0] if player.is_moving() else 0
        plus_bottom = velocity[1] if player.falling else 0
        plus_right_corrected = plus_right + self.collision_detection_correction_right
        plus_left_corrected = minus_left + self.collision_detection_correction_left
        plus_bottom_corrected = plus_bottom + self.collision_detection_correction_bottom

        # Return values
        collides_bottom = False
        collides_left = False
        collides_right = False
        segment_top_y = 0
        segment_right_x = 0
        segment_left_x = 0
        stands_on_moving_segment = False
        segment_speed = 0

        player_rect = player.get_rect()
        for line in self._lines:
            for segment in line.segments:
                segment_startpoint_with_offset = segment.get_startpoint_with_offset(offset)
                segment_next_startpoint_with_offset = segment.get_next_startpoint_with_offset(dt, offset)

                # check collisions only if segment is on screen
                x_left_in_screen = (segment.startpoint[0] + segment.width) > offset[0]
                x_right_in_screen = segment_startpoint_with_offset[0] < self.screen_size[0]
                if x_left_in_screen and x_right_in_screen:
                    segment_x = segment_next_startpoint_with_offset[0]
                    segment_y = segment_next_startpoint_with_offset[1]

                    segment_x_right = segment_x + segment.width
                    segment_y_bottom = segment_y + segment.height

                    player_right = player_rect.x + player_rect.width + plus_right
                    player_left = player_rect.x - minus_left
                    player_bottom = player_rect.y + player_rect.height + plus_bottom
                    player_top = player_rect.y

                    inside_x_range = player_right >= segment_x and player_left <= segment_x_right
                    inside_y_range = player_bottom >= (segment_y - self.collision_detection_correction_bottom) and player_top <= (segment_y_bottom + self.collision_detection_correction_bottom)

                    on_x_left = player_left <= segment_x_right and (player_left + plus_left_corrected) >= segment_x_right and not player.is_going_right()
                    on_x_right = player_right >= segment_x and (player_right - plus_right_corrected) <= segment_x and not player.is_going_left()
                    on_y = player_bottom >= (segment_y - self.collision_detection_correction_bottom) and (player_bottom - plus_bottom_corrected) <= (segment_y + self.collision_detection_correction_bottom)

                    if inside_y_range and inside_x_range:
                        if on_x_left:
                            collides_left = True
                            segment_right_x = segment_x_right
                        if on_x_right:
                            collides_right = True
                            segment_left_x = segment_x
                        if on_y:
                            collides_bottom = True
                            segment_top_y = segment_startpoint_with_offset[1]
                            if line.moving:
                                stands_on_moving_segment = True
                                segment_speed = segment.get_speed()

                        return collides_bottom, collides_left, collides_right, segment_top_y, segment_right_x, segment_left_x, stands_on_moving_segment, segment_speed

        return collides_bottom, collides_left, collides_right, segment_top_y, segment_right_x, segment_left_x, stands_on_moving_segment, segment_speed

    def loop_visuals(self, dt):
        """Loops only the visual parts of the level

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        for line in self._lines:
            line.loop_visuals(dt)

    def loop(self, dt):
        """Updates the level

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        for line in self._lines:
            line.loop(dt)

    def draw(self, offset):
        """Draws the level

        :param offset: The offset
        """
        for li in range(0, self.size()):
            self.get(li).draw(offset)
