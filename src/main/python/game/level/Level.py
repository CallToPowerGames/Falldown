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
from game.CollisionInfo import CollisionInfo

class Level():
    """The level"""

    def __init__(self, game_data):
        """Initializes the level

        :param game_data: The game data
        """
        logging.info('Initializing level')

        self.game_data = game_data

        self.screen_size = self.game_data.game_config.get('screen.size')
        self.level_generator_modifier = self.game_data.game_config.get('level.generator.modifier')
        self.min_x = self.game_data.game_config.get('offset.max.left') * self.level_generator_modifier
        self.max_x = self.game_data.game_config.get('offset.max.right') * self.level_generator_modifier
        self.gap_min = self.game_data.game_config.get('level.segments.gap.min')
        self.gap_add_max = self.game_data.game_config.get('level.segments.gap.add.max')
        self.segment_height = self.game_data.game_config.get('level.segments.height')
        self.gap_vert_min = self.game_data.game_config.get('level.segments.gap.vert.min')
        self.gap_vert_add_max = self.game_data.game_config.get('level.segments.gap.vert.add.max')
        self.line_moving_probability = self.game_data.game_config.get('level.line.moving.probability')
        self.clear_linesegment_probability = self.game_data.game_config.get('level.line.clear.linesegment.probability')
        self.clear_all_probability = self.game_data.game_config.get('level.line.clear.all.probability')
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
        self.segment_img_clear_linesegment_size = self.game_data.game_config.get('level.segment.img.clear.linesegment.size')
        self.segment_img_clear_linesegment_startpoint = self.game_data.game_config.get('level.segment.img.clear.linesegment.startpoint')
        self.segment_img_clear_all_size = self.game_data.game_config.get('level.segment.img.clear.all.size')
        self.segment_img_clear_all_startpoint = self.game_data.game_config.get('level.segment.img.clear.all.startpoint')
        self.collision_detection_correction_left = self.game_data.game_config.get('level.collision.detection.correction.left')
        self.collision_detection_correction_right = self.game_data.game_config.get('level.collision.detection.correction.right')
        self.collision_detection_correction_bottom = self.game_data.game_config.get('level.collision.detection.correction.bottom')

        self.spritesheet_segment_left = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment', size=self.segment_img_left_size, nr_images=1, startpoint=self.segment_img_left_startpoint, generate_sides=False)
        self.spritesheet_segment_mid = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment', size=self.segment_img_mid_size, nr_images=1, startpoint=self.segment_img_mid_startpoint, generate_sides=False)
        self.spritesheet_segment_right = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment', size=self.segment_img_right_size, nr_images=1, startpoint=self.segment_img_right_startpoint, generate_sides=False)
        self.spritesheet_segment_propeller = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment.propeller', size=self.segment_img_propeller_size, nr_images=4, startpoint=self.segment_img_propeller_startpoint, generate_sides=False)
        self.spritesheet_segment_clear_linesegment = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment.clear.line', size=self.segment_img_clear_linesegment_size, nr_images=21, startpoint=self.segment_img_clear_linesegment_startpoint, generate_sides=False)
        self.spritesheet_segment_clear_all = Spritesheet(self.game_data.cache.sprite_cache, 'level.segment.clear.all', size=self.segment_img_clear_all_size, nr_images=15, startpoint=self.segment_img_clear_all_startpoint, generate_sides=False)

        self.image_segment_right = None
        self.image_segment_mid = None
        self.image_segment_left = None

        self._lines = []
        self.last_y = -1
        self.nr_or_lines_generated = 0

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

    def clear_line_segment(self, index_line, index_segment):
        """Clears a specific segment in a given line

        :param index_line: The line index
        :param index_segment: The segment index
        """
        if index_line >= 0 and index_segment >= 0 and index_line < len(self._lines):
            line = self._lines[index_line]
            if index_segment < len(line.segments):
                line.segments.pop(index_segment)

    def clear_all(self):
        """Clears all lines"""
        self._lines = []

    def generate_new_line(self):
        """Generates a new line
        
        :return: The new line
        """
        self.nr_or_lines_generated += 1

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
            clear_linesegment = random.randint(0, 100) < self.clear_linesegment_probability
            clear_all = (random.randint(0, 100) < self.clear_all_probability) if not clear_linesegment else False

            cnt += 1
            startpoint = (
                startpoint_last[0] + width_last + self.gap_min + random.randint(0, self.gap_add_max),
                startpoint_last[1]
            )
            width = random.randint(self.segments_width_min, self.segments_width_max)
            height = self.segment_height
            images_segment = [self.image_segment_left, self.image_segment_mid, self.image_segment_right]
            segment = Segment(self.game_data.game_config, images_segment, self.spritesheet_segment_propeller, self.spritesheet_segment_clear_linesegment, self.spritesheet_segment_clear_all, startpoint, width, height, moving=moving, clear_linesegment=clear_linesegment, clear_all=clear_all)
            line.add(segment)
            startpoint_last = startpoint
            width_last = width
            reached_end = (cnt > 1000) or (abs(self.min_x) + self.max_x - (startpoint_last[0] + width_last + self.gap_min + self.gap_add_max) <= 0)
        self.add(line)

        return line

    def collides_with(self, player, dt, velocity, keys, offset):
        """Checks whether a level segment collides with the player.
        Returns early and w/o collision check if <CollidesWithClearLine> or <CollidesWithClearAll>

        :param player: The player
        :param dt: Tick rate, milliseconds between each call to 'tick'
        :param velocity: Calculated velocity
        :param keys: The keys
        :param offset: The offset
        :return: CollisionInfo
        """
        plus_right = velocity[0] if player.is_moving() else 0
        minus_left = velocity[0] if player.is_moving() else 0
        plus_bottom = velocity[1] if player.falling else 0
        plus_right_corrected = plus_right + self.collision_detection_correction_right
        plus_left_corrected = minus_left + self.collision_detection_correction_left
        plus_bottom_corrected = plus_bottom + self.collision_detection_correction_bottom

        # Return values
        collisioninfo = CollisionInfo()

        player_rect = player.get_rect()
        for i_l, line in enumerate(self._lines):
            collisioninfo.index_line_colliding = i_l
            for i_s, segment in enumerate(line.segments):
                collisioninfo.index_segment_colliding = i_s
                segment_startpoint_with_offset = segment.get_startpoint_with_offset(offset)
                segment_next_startpoint_with_offset = segment.get_next_startpoint_with_offset(dt, offset)

                # check collisions only if segment is on screen
                x_left_in_screen = (segment.startpoint[0] + segment.width) > offset[0]
                x_right_in_screen = segment_startpoint_with_offset[0] < self.screen_size[0]
                if x_left_in_screen and x_right_in_screen:
                    collisioninfo.collides_clear_linesegment = segment.clear_linesegment and pygame.Rect.colliderect(player_rect, segment.get_clear_linesegment_rect(offset))
                    collisioninfo.collides_clear_all = segment.clear_all and pygame.Rect.colliderect(player_rect, segment.get_clear_all_rect(offset))
                    if collisioninfo.collides_clear_linesegment or collisioninfo.collides_clear_all:
                        return collisioninfo

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
                            collisioninfo.collides_left = True
                        if on_x_right:
                            collisioninfo.collides_right = True
                        if on_y:
                            collisioninfo.collides_bottom = True
                            collisioninfo.segment_top_y = segment_startpoint_with_offset[1]
                            if line.moving:
                                collisioninfo.stands_on_moving_segment = True
                                collisioninfo.segment_speed = segment.get_speed()

                        return collisioninfo

        return collisioninfo

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
        for li in range(0, len(self._lines)):
            self.get(li).draw(offset)
