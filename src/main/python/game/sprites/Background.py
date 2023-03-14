#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Background"""

import logging
import random

import pygame

from game.GameState import State
from game.Direction import Direction
from game.sprites.Spritesheet import Spritesheet
from game.sprites.Cloud import Cloud
from game.level.Level import Level
from game.sprites.Player import Player
from game.Camera import Camera

class Background(pygame.sprite.Sprite):
    """The background"""

    def __init__(self, game_data, update_every_nth_loop=30):
        """Initializes the background

        :param game_data: The game data,
        :param update_every_nth_loop: Update every nth loop (clean and refill)
        """
        super().__init__()

        logging.debug('Initializing background')

        self.game_data = game_data

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.offset_max_left = self.game_data.game_config.get('offset.max.left')
        self.offset_max_right = self.game_data.game_config.get('offset.max.right')
        self.bg_main_color = self.game_data.game_config.get('background.main.color')
        self.nr_of_clouds_big = self.game_data.game_config.get('background.number.bg.clouds.big')
        self.startpoint_bg_clouds_big = self.game_data.game_config.get('background.startpoint.bg.clouds.big')
        self.size_bg_clouds_big = self.game_data.game_config.get('background.size.bg.clouds.big')
        self.speed_bg_clouds_big_min = self.game_data.game_config.get('background.speed.bg.clouds.big.min')
        self.speed_bg_clouds_big_max = self.game_data.game_config.get('background.speed.bg.clouds.big.max')
        self.nr_of_clouds_mid = self.game_data.game_config.get('background.number.bg.clouds.mid')
        self.startpoint_bg_clouds_mid = self.game_data.game_config.get('background.startpoint.bg.clouds.mid')
        self.size_bg_clouds_mid = self.game_data.game_config.get('background.size.bg.clouds.mid')
        self.speed_bg_clouds_mid_min = self.game_data.game_config.get('background.speed.bg.clouds.mid.min')
        self.speed_bg_clouds_mid_max = self.game_data.game_config.get('background.speed.bg.clouds.mid.max')
        self.nr_of_clouds_small = self.game_data.game_config.get('background.number.bg.clouds.small')
        self.startpoint_bg_clouds_small = self.game_data.game_config.get('background.startpoint.bg.clouds.small')
        self.size_bg_clouds_small = self.game_data.game_config.get('background.size.bg.clouds.small')
        self.speed_bg_clouds_small_min = self.game_data.game_config.get('background.speed.bg.clouds.small.min')
        self.speed_bg_clouds_small_max = self.game_data.game_config.get('background.speed.bg.clouds.small.max')
        self.bg_size = self.game_data.game_config.get('background.size')
        self.bg_startpoint = self.game_data.game_config.get('background.startpoint')
        self.bg_draw = self.game_data.game_config.get('background.draw')
        self.offset_factor_x_bg_image = self.game_data.game_config.get('background.offset.factor.x.bg.image')
        self.offset_factor_x_small = self.game_data.game_config.get('background.offset.factor.x.small')
        self.offset_factor_x_mid = self.game_data.game_config.get('background.offset.factor.x.mid')
        self.offset_factor_x_big = self.game_data.game_config.get('background.offset.factor.x.big')
        self.offset_factor_y_bg_image = self.game_data.game_config.get('background.offset.factor.y.bg.image')
        self.offset_factor_y_small = self.game_data.game_config.get('background.offset.factor.y.small')
        self.offset_factor_y_mid = self.game_data.game_config.get('background.offset.factor.y.mid')
        self.offset_factor_y_big = self.game_data.game_config.get('background.offset.factor.y.big')
        self.background_scale_factor_max_small = self.game_data.game_config.get('background.scale.factor.max.small')
        self.background_scale_factor_max_mid = self.game_data.game_config.get('background.scale.factor.max.mid')
        self.background_scale_factor_max_big = self.game_data.game_config.get('background.scale.factor.max.big')
        self.level_offset_max = self.game_data.game_config.get('level.offset.max')
        self.camera_borders = self.game_data.game_config.get('camera.borders')

        self.min_size_x = self.offset_max_left
        self.max_size_x = self.screen_size[0] + abs(self.offset_max_left) + self.offset_max_right

        self.spritesheet_bg_clouds_big_cloud = Spritesheet(self.game_data.cache.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_big, nr_images=1, startpoint=self.startpoint_bg_clouds_big, generate_sides=False)
        self.spritesheet_bg_clouds_mid_cloud = Spritesheet(self.game_data.cache.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_mid, nr_images=1, startpoint=self.startpoint_bg_clouds_mid, generate_sides=False)
        self.spritesheet_bg_clouds_small_cloud = Spritesheet(self.game_data.cache.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_small, nr_images=1, startpoint=self.startpoint_bg_clouds_small, generate_sides=False)
        self.big_clouds = []
        self.mid_clouds = []
        self.small_clouds = []

        self.spritesheet_bg = Spritesheet(self.game_data.cache.sprite_cache, 'bg', size=self.bg_size, nr_images=1, startpoint=self.bg_startpoint, generate_sides=False, colorkey=None)
        self.image_bg = None

        self.clean_every_nth = update_every_nth_loop
        self.curr_clean = 0

        self.offset = pygame.math.Vector2(0, 0)
        self.offset_plus = pygame.math.Vector2(1, 1)

        self.background_level_active = True
        self.background_level = None
        self.background_player = None
        self.background_camera = None

        self._init()

    def _init(self):
        """Initializes the background"""
        self.big_clouds = []
        for i in range(int(self.nr_of_clouds_big / 3)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_big_cloud, (self.size_bg_clouds_big[0], self.size_bg_clouds_big[1]), self.background_scale_factor_max_big)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)
        self.mid_clouds = []
        for i in range(int(self.nr_of_clouds_mid / 3)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_mid_cloud, (self.size_bg_clouds_mid[0], self.size_bg_clouds_mid[1]), self.background_scale_factor_max_mid)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)
        self.small_clouds = []
        for i in range(int(self.nr_of_clouds_small / 3)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_small_cloud, (self.size_bg_clouds_small[0], self.size_bg_clouds_small[1]), self.background_scale_factor_max_small)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
            self.small_clouds.append(cloud)

        self.sort_clouds()

        self.image_bg = self.spritesheet_bg.images_left[0]

    def _get_scaled_cloud(self, spritesheet, original_size, factor):
        """Scales a cloud

        :param spritesheet: The spritesheet
        :param original_size: The original size
        :param factor: The scale factor
        """
        rand_float = round(random.uniform(1, factor), 1)
        _size = (original_size[0] * rand_float, original_size[1] * rand_float)
        return _size, spritesheet.get_scaled_left(_size)[0]

    def init_background_level(self):
        """Initializes the background level"""
        self.background_level_active = True
        self.background_level = Level(self.game_data)
        self.background_level.last_y = -1

        self.background_camera = Camera(self.game_data,
                                        level=self.background_level,
                                        player=self.background_player,
                                        show_go=False, directly_generate_segments=True)

    def clear_background_level(self):
        """Clears the background level"""
        self.background_level_active = False
        self.background_level = None
        self.background_player = None
        self.background_camera = None

    def clean(self):
        """Cleans the background elements, removes all lines not in the offset area"""
        new_big_clouds = []
        for cloud in self.big_clouds:
            in_x = cloud.get_curr_x() + cloud.size[0] >= self.offset_max_left
            in_y = cloud.startpoint[1] + cloud.size[1] >= self.offset_big.y
            if in_x and in_y:
                new_big_clouds.append(cloud)
        self.big_clouds = new_big_clouds

        new_mid_clouds = []
        for cloud in self.mid_clouds:
            in_x = cloud.get_curr_x() + cloud.size[0] >= self.offset_max_left
            in_y = cloud.startpoint[1] + cloud.size[1] >= self.offset_mid.y
            if in_x and in_y:
                new_mid_clouds.append(cloud)
        self.mid_clouds = new_mid_clouds

        new_small_clouds = []
        for cloud in self.small_clouds:
            in_x = cloud.get_curr_x() + cloud.size[0] >= self.offset_max_left
            in_y = cloud.startpoint[1] + cloud.size[1] >= self.offset_small.y
            if in_x and in_y:
                new_small_clouds.append(cloud)
        self.small_clouds = new_small_clouds

        self.sort_clouds()

    def fill(self):
        """Fills up clouds"""
        # In the current screen
        y_min = int(self.offset.y)
        y_max = int(self.offset.y) + self.screen_size[1]

        big_clouds_missing = self.nr_of_clouds_big - len(self.big_clouds)
        for i in range(int(big_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_big_cloud, (self.size_bg_clouds_big[0], self.size_bg_clouds_big[1]), self.background_scale_factor_max_big)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)

        mid_clouds_missing = self.nr_of_clouds_mid - len(self.mid_clouds)
        for i in range(int(mid_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_mid_cloud, (self.size_bg_clouds_mid[0], self.size_bg_clouds_mid[1]), self.background_scale_factor_max_mid)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)

        small_clouds_missing = self.nr_of_clouds_small - len(self.small_clouds)
        for i in range(int(small_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_small_cloud, (self.size_bg_clouds_small[0], self.size_bg_clouds_small[1]), self.background_scale_factor_max_small)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
            self.small_clouds.append(cloud)

        # Below the current screen
        x_min = self.min_size_x
        x_max = self.max_size_x
        y_min = int(self.offset.y) + self.screen_size[1]
        y_max = int(self.offset.y) + self.screen_size[1] * 2

        big_clouds_missing = self.nr_of_clouds_big - len(self.big_clouds)
        for i in range(int(big_clouds_missing / 3)):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_big_cloud, (self.size_bg_clouds_big[0], self.size_bg_clouds_big[1]), self.background_scale_factor_max_big)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)

        mid_clouds_missing = self.nr_of_clouds_mid - len(self.mid_clouds)
        for i in range(int(mid_clouds_missing / 3)):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_mid_cloud, (self.size_bg_clouds_mid[0], self.size_bg_clouds_mid[1]), self.background_scale_factor_max_mid)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)

        small_clouds_missing = self.nr_of_clouds_small - len(self.small_clouds)
        for i in range(int(small_clouds_missing / 3)):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            _size, _img = self._get_scaled_cloud(self.spritesheet_bg_clouds_small_cloud, (self.size_bg_clouds_small[0], self.size_bg_clouds_small[1]), self.background_scale_factor_max_small)
            cloud = Cloud(self.game_data, _img, (x, y), _size, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
            self.small_clouds.append(cloud)

        self.sort_clouds()

    def sort_clouds(self):
        """Sorts clouds so that slower clouds can be drawn first"""
        self.big_clouds = sorted(self.big_clouds, key=lambda e: e.speed)
        self.mid_clouds = sorted(self.mid_clouds, key=lambda e: e.speed)
        self.small_clouds = sorted(self.small_clouds, key=lambda e: e.speed)

    def reset(self, initialize_background_level=False):
        """Resets the background"""
        logging.info('Resetting background')
        self.offset = pygame.math.Vector2(0, 0)
        self.offset_plus = pygame.math.Vector2(1, 1)
        self.clear_background_level()
        if initialize_background_level:
            self.init_background_level()
        self._init()

    def reload_conf(self):
        """Reloads relevant config parameters"""
        self.bg_draw = self.game_data.game_config.get('background.draw')

    def loop(self, dt, offset=pygame.math.Vector2(0, 0), iterate_offset=False):
        """Loops the background

        :param dt: Tick rate, milliseconds between each call to 'tick'
        :param offset: The offset. Only set if iterate_offset is False
        :param iterate_offset: Flag whether to slowly iterate the offset
        """
        if iterate_offset:
            self.offset += self.offset_plus
            if self.offset.y > self.level_offset_max:
                self.reset(init_background_level=True)
            elif (self.offset[0] > self.offset_max_right) or (self.offset[0] < self.offset_max_left):
                self.offset_plus = (-1 * self.offset_plus[0], self.offset_plus[1])
        else:
            self.offset = offset

        if self.curr_clean >= self.clean_every_nth:
            self.curr_clean = 0
            self.clean()
            self.fill()
            logging.debug('#Clouds={}'.format(len(self.big_clouds) + len(self.mid_clouds) + len(self.small_clouds)))
        else:
            self.curr_clean += 1

        for cloud in self.big_clouds:
            cloud.loop(dt)
        for cloud in self.mid_clouds:
            cloud.loop(dt)
        for cloud in self.small_clouds:
            cloud.loop(dt)

        if self.background_camera:
            self.background_camera.offset = self.offset
            self.background_camera.loop(dt, {})

    def _draw(self, clouds, offset):
        """Draws the background

        :param clouds: Cloud array
        """
        nr_drawn = 0
        for cloud in clouds:
            x_left_in_screen = (cloud.startpoint[0] + cloud.size[0]) > offset.x
            x_right_in_screen = (cloud.startpoint[0] - offset.x) < self.screen_size[0]
            y_in_top_screen = (cloud.startpoint[1] + cloud.size[1]) > offset.y
            if x_left_in_screen and x_right_in_screen and y_in_top_screen:
                cloud.draw(offset)
                nr_drawn += 1

        return nr_drawn

    def _draw_bg(self, offset):
        """Draws the background"""
        startpoint_y = 0
        while (startpoint_y + self.image_bg.get_height()) <= offset.y:
            startpoint_y += self.image_bg.get_height()
        curr_y = startpoint_y - offset.y
        nr_drawn = 0
        for i in range(int(self.screen_size[1] / self.image_bg.get_height()) + 2):
            startpoint_x = self.offset_max_left - self.image_bg.get_width()
            while (startpoint_x + self.image_bg.get_width()) <= offset.x:
                startpoint_x += self.image_bg.get_width()
            curr_x = startpoint_x - offset.x
            for i in range(int(self.screen_size[0] / self.image_bg.get_width()) + 2):
                self.screen.blit(self.image_bg,
                    pygame.Rect(
                        curr_x,
                        curr_y,
                        self.image_bg.get_width(),
                        self.image_bg.get_height()
                    )
                )
                nr_drawn += 1
                curr_x += self.image_bg.get_width()
            curr_y += self.image_bg.get_height()

        return nr_drawn

    def draw(self, draw_background_level=False):
        """Draws the background

        :param offset: The offset
        """
        if self.bg_draw:
            _offset = pygame.math.Vector2(self.offset.x * self.offset_factor_x_bg_image, self.offset.y * self.offset_factor_y_bg_image)
            self._draw_bg(_offset)
        else:
            self.screen.fill(self.bg_main_color)

        self.offset_small = pygame.math.Vector2(self.offset.x * self.offset_factor_x_small, self.offset.y * self.offset_factor_y_small)
        self.offset_mid = pygame.math.Vector2(self.offset.x * self.offset_factor_x_mid, self.offset.y * self.offset_factor_y_mid)
        self.offset_big = pygame.math.Vector2(self.offset.x * self.offset_factor_x_big, self.offset.y * self.offset_factor_y_big)

        nr_drawn = self._draw(self.small_clouds, self.offset_small)
        nr_drawn += self._draw(self.mid_clouds, self.offset_mid)
        nr_drawn += self._draw(self.big_clouds, self.offset_big)

        # logging.debug('#Clouds drawn: {}'.format(nr_drawn))

        if draw_background_level and self.background_camera:
            self.background_camera.offset = self.offset
            self.background_camera.draw(show_score=False, show_fps=False)
