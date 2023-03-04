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
        self.camera_borders = self.game_data.game_config.get('camera.borders')
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

        self.min_size_x = self.offset_max_left
        self.max_size_x = self.screen_size[0] + abs(self.offset_max_left) + self.offset_max_right

        self.w_clouds_big = self.size_bg_clouds_big[0]
        self.h_clouds_big = self.size_bg_clouds_big[1]
        self.w_clouds_mid = self.size_bg_clouds_mid[0]
        self.h_clouds_mid = self.size_bg_clouds_mid[1]
        self.w_clouds_small = self.size_bg_clouds_small[0]
        self.h_clouds_small = self.size_bg_clouds_small[1]

        self.spritesheet_bg_clouds_big_cloud = Spritesheet(self.game_data.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_big, nr_images=1, startpoint=self.startpoint_bg_clouds_big, generate_sides=False)
        self.spritesheet_bg_clouds_mid_cloud = Spritesheet(self.game_data.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_mid, nr_images=1, startpoint=self.startpoint_bg_clouds_mid, generate_sides=False)
        self.spritesheet_bg_clouds_small_cloud = Spritesheet(self.game_data.sprite_cache, 'bg.clouds', size=self.size_bg_clouds_small, nr_images=1, startpoint=self.startpoint_bg_clouds_small, generate_sides=False)
        self.big_clouds = []
        self.mid_clouds = []
        self.small_clouds = []

        self.clean_every_nth = update_every_nth_loop
        self.curr_clean = 0
        self.offset = pygame.math.Vector2(0, 0)

        self._init()

    def _init(self):
        """Initializes the background"""
        for i in range(int(self.nr_of_clouds_big / 2)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_big_cloud.images_left[0], (x, y), self.w_clouds_big, self.h_clouds_big, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)
        for i in range(int(self.nr_of_clouds_mid)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_mid_cloud.images_left[0], (x, y), self.w_clouds_mid, self.h_clouds_mid, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)
        for i in range(int(self.nr_of_clouds_small)):
            x = random.randint(self.min_size_x, self.max_size_x)
            y = random.randint(0, self.screen_size[1])
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_small_cloud.images_left[0], (x, y), self.w_clouds_small, self.h_clouds_small, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
            self.small_clouds.append(cloud)

    def clean(self):
        """Cleans the background elements, removes all lines not in the offset area"""
        new_big_clouds = []
        for cloud in self.big_clouds:
            in_x = cloud.get_curr_x() + cloud.width >= self.offset_max_left
            in_y = cloud.startpoint[1] >= self.offset.y
            if in_x and in_y:
                new_big_clouds.append(cloud)
        self.big_clouds = new_big_clouds

        new_mid_clouds = []
        for cloud in self.mid_clouds:
            in_x = cloud.get_curr_x() + cloud.width >= self.offset_max_left
            in_y = cloud.startpoint[1] >= self.offset.y
            if in_x and in_y:
                new_mid_clouds.append(cloud)
        self.mid_clouds = new_mid_clouds

        new_small_clouds = []
        for cloud in self.small_clouds:
            in_x = cloud.get_curr_x() + cloud.width >= self.offset_max_left
            in_y = cloud.startpoint[1] >= self.offset.y
            if in_x and in_y:
                new_small_clouds.append(cloud)
        self.small_clouds = new_small_clouds

    def fill(self):
        """Fills up clouds"""
        
        # In the current screen
        y_min = int(self.offset.y)
        y_max = int(self.offset.y) + self.screen_size[1]

        big_clouds_missing = self.nr_of_clouds_big - len(self.big_clouds)
        for i in range(int(big_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_big_cloud.images_left[0], (x, y), self.w_clouds_big, self.h_clouds_big, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)

        mid_clouds_missing = self.nr_of_clouds_mid - len(self.mid_clouds)
        for i in range(int(mid_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_mid_cloud.images_left[0], (x, y), self.w_clouds_mid, self.h_clouds_mid, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)

        small_clouds_missing = self.nr_of_clouds_small - len(self.small_clouds)
        for i in range(int(small_clouds_missing / 3)):
            x = self.max_size_x
            y = random.randint(y_min, y_max)
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_small_cloud.images_left[0], (x, y), self.w_clouds_small, self.h_clouds_small, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
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
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_big_cloud.images_left[0], (x, y), self.w_clouds_big, self.h_clouds_big, self.speed_bg_clouds_big_min, self.speed_bg_clouds_big_max)
            self.big_clouds.append(cloud)

        mid_clouds_missing = self.nr_of_clouds_mid - len(self.mid_clouds)
        for i in range(int(mid_clouds_missing / 3)):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_mid_cloud.images_left[0], (x, y), self.w_clouds_mid, self.h_clouds_mid, self.speed_bg_clouds_mid_min, self.speed_bg_clouds_mid_max)
            self.mid_clouds.append(cloud)

        small_clouds_missing = self.nr_of_clouds_small - len(self.small_clouds)
        for i in range(int(small_clouds_missing / 3)):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            cloud = Cloud(self.game_data, self.spritesheet_bg_clouds_small_cloud.images_left[0], (x, y), self.w_clouds_small, self.h_clouds_small, self.speed_bg_clouds_small_min, self.speed_bg_clouds_small_max)
            self.small_clouds.append(cloud)

    def loop(self, dt):
        """Loops the background

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
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

    def _draw(self, clouds):
        """Draws the background

        :param clouds: Cloud array
        """
        for cloud in clouds:
            x_left_in_screen = (cloud.startpoint[0] + cloud.width) > self.offset.x
            x_right_in_screen = (cloud.startpoint[0] - self.offset.x) < self.screen_size[0]
            y_in_top_screen = (cloud.startpoint[1] + cloud.height) > self.offset.y
            if x_left_in_screen and x_right_in_screen and y_in_top_screen:
                cloud.draw(self.offset)

    def draw(self, offset=pygame.math.Vector2(0, 0)):
        """Draws the background

        :param offset: The offset
        """
        self.screen.fill(self.bg_main_color)

        self.offset = offset

        self._draw(self.big_clouds)
        self._draw(self.mid_clouds)
        self._draw(self.small_clouds)
