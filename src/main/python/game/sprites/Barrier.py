#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Barrier"""

import logging

import pygame

from game.sprites.Spritesheet import Spritesheet

class Barrier(pygame.sprite.Sprite):
    """The barrier"""

    def __init__(self, game_data, position_midbottom=(0, 0)):
        """Initializes the barrier

        :param game_data: The game data
        :param position_midbottom: The position mid bottom
        """
        super().__init__()

        logging.debug('Initializing barrier')

        self.game_data = game_data
        self.position_original = (position_midbottom[0], position_midbottom[1])

        self.screen = self.game_data.game_config.get('screen')
        self.camera_borders = self.game_data.game_config.get('camera.borders')
        self.offset_max_left = self.game_data.game_config.get('offset.max.left')
        self.offset_max_right = self.game_data.game_config.get('offset.max.right')
        self.offset_max_up = self.game_data.game_config.get('offset.max.up')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.border_chain_size = self.game_data.game_config.get('border.chain.size')
        self.barrier_platform_size = self.game_data.game_config.get('barrier.platform.size')
        self.barrier_cannon_size = self.game_data.game_config.get('barrier.cannon.size')
        self.barrier_holder_left_size = self.game_data.game_config.get('barrier.holder.left.size')
        self.barrier_holder_right_size = self.game_data.game_config.get('barrier.holder.right.size')
        self.barrier_laserbeam_size = self.game_data.game_config.get('barrier.laserbeam.size')
        self.speed = self.game_data.game_config.get('barrier.speed')
        self.speed_increase = self.game_data.game_config.get('barrier.speed.increase')
        self.barrier_laser_correction = self.game_data.game_config.get('barrier.laser.correction')
        self.music_volume_bg_game_effects = self.game_data.game_config.get('music.volume.background.game.effects')
        self.collision_detection_correction_top = self.game_data.game_config.get('level.collision.detection.correction.bottom')
        self.barrier_cannon_left_correction = self.game_data.game_config.get('barrier.cannon.left.correction')
        self.barrier_cannon_right_correction = self.game_data.game_config.get('barrier.cannon.right.correction')

        self.spritesheet_chain = Spritesheet(self.game_data.sprite_cache, 'barrier.chain', self.border_chain_size, 1, generate_sides=False)
        self.spritesheet_holder_left = Spritesheet(self.game_data.sprite_cache, 'barrier.holder.left', self.barrier_holder_left_size, 16)
        self.spritesheet_holder_right = Spritesheet(self.game_data.sprite_cache, 'barrier.holder.right', self.barrier_holder_right_size, 12)
        self.spritesheet_platform = Spritesheet(self.game_data.sprite_cache, 'barrier.platform', self.barrier_platform_size, 8, generate_sides=False)
        self.spritesheet_cannon = Spritesheet(self.game_data.sprite_cache, 'barrier.cannon', self.barrier_cannon_size, 1, orientation_left=False)
        self.spritesheet_laserbeam = Spritesheet(self.game_data.sprite_cache, [
            'barrier.laserbeam.1',
            'barrier.laserbeam.2',
            'barrier.laserbeam.3',
            'barrier.laserbeam.4'
        ], self.barrier_laserbeam_size, 1, generate_sides=False)

        self.image_chain = None
        self.image_platform = None
        self.image_laserbeam = None
        self.image_barrier_holder_left = None
        self.image_barrier_holder_right = None
        self.image_barrier_cannon_left = None
        self.image_barrier_cannon_right = None

        self.curr_img_platform = 0
        self.curr_img_laserbeam = 0
        self.curr_img_index_holder_left = 0
        self.curr_img_index_holder_right = 0

        self.sound_playing = False
        self.stopped = False
        self.paused = False
        self.started = False
        self.rect = None
        self.rect_original = None

        self.curr_barrier_holder_left = 0
        self.update_barrier_holder_left = 1
        self.curr_barrier_holder_right = 0
        self.update_barrier_holder_right = 2
        self.curr_laserbeam = 0
        self.update_laserbeam = 1
        self.curr_platform = 0
        self.update_platform = 1

        self._init()

    def _init(self):
        """Initializes the barrier"""
        logging.debug("Initializing the barrier")

        self.position = (self.position_original[0], self.position_original[1])

        self.image_chain = self.spritesheet_chain.images_left[0]
        self.image_platform = self.spritesheet_platform.images_left[self.curr_img_platform]
        self.image_laserbeam = self.spritesheet_laserbeam.images_left[self.curr_img_laserbeam]
        self.image_barrier_holder_left = self.spritesheet_holder_left.images_right[self.curr_img_index_holder_left]
        self.image_barrier_holder_right = self.spritesheet_holder_right.images_left[self.curr_img_index_holder_right]
        self.image_barrier_cannon_left = self.spritesheet_cannon.images_right[0]
        self.image_barrier_cannon_right = self.spritesheet_cannon.images_left[0]

        self.rect = pygame.Rect(
                    0,
                    0,
                    self.screen_size[0],
                    self.image_laserbeam.get_height()
               )
        self.rect_original = pygame.Rect(
                    0,
                    0,
                    self.screen_size[0],
                    self.image_laserbeam.get_height()
               )

    def pause(self):
        """Pauses"""
        self.paused = True
        # self.stop(fullstop=False)

    def unpause(self):
        """Pauses"""
        self.paused = False

    def stop(self, fullstop=True):
        """Stops everything

        :param fullstop: Fully stops the music
        """
        if self.sound_playing:
            self.game_data.sound_cache.stop('laser')
            self.sound_playing = False
            if fullstop:
                self.stopped = True

    def update_sprite(self):
        """Updates the sprite"""
        if self.curr_barrier_holder_left > self.update_barrier_holder_left:
            self.curr_barrier_holder_left = 0
            self.image_barrier_holder_left = self.spritesheet_holder_left.images_right[self.curr_img_index_holder_left]
            self.curr_img_index_holder_left += 1
            if self.curr_img_index_holder_left >= len(self.spritesheet_holder_left.images_right):
                self.curr_img_index_holder_left = 0
        else:
            self.curr_barrier_holder_left += 1
            
        if self.curr_barrier_holder_right > self.update_barrier_holder_right:
            self.curr_barrier_holder_right = 0
            self.image_barrier_holder_right = self.spritesheet_holder_right.images_left[self.curr_img_index_holder_right]
            self.curr_img_index_holder_right += 1
            if self.curr_img_index_holder_right >= len(self.spritesheet_holder_right.images_left):
                self.curr_img_index_holder_right = 0
        else:
            self.curr_barrier_holder_right += 1

        if self.curr_laserbeam > self.update_laserbeam:
            self.curr_laserbeam = 0
            self.image_laserbeam = self.spritesheet_laserbeam.images_left[self.curr_img_laserbeam]
            self.curr_img_laserbeam += 1
            if self.curr_img_laserbeam >= len(self.spritesheet_laserbeam.images_left):
                self.curr_img_laserbeam = 0
        else:
            self.curr_laserbeam += 1

        if self.curr_platform > self.update_platform:
            self.curr_platform = 0
            self.image_platform = self.spritesheet_platform.images_left[self.curr_img_platform]
            self.curr_img_platform += 1
            if self.curr_img_platform >= len(self.spritesheet_platform.images_left):
                self.curr_img_platform = 0
        else:
            self.curr_platform += 1

    def is_visible(self, offset):
        """Returns whether the barrier is visible

        :param offset: The offset
        :return: Flag whether the barrier is visible
        """
        return self.started and (self.rect.y + self.image_laserbeam.get_height()) > offset.y

    def draw(self, offset):
        """Draws the barrier

        :param offset: The offset
        """
        if abs(self.offset_max_left - offset.x) < self.camera_borders['left']:
            # Left chains
            height = 0
            while height < self.screen_size[1]:
                self.screen.blit(self.image_chain,
                    pygame.Rect(
                            self.offset_max_left + (self.camera_borders['left'] / 2) - (self.image_chain.get_width() / 2) - offset.x,
                            self.offset_max_up + height,
                            self.image_chain.get_width(),
                            self.image_chain.get_height()
                    ),
                )
                height += self.image_chain.get_height()

        if abs(self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x) < (self.screen_size[0] + self.camera_borders['left'] - self.camera_borders['right']):
            # Right chains
            height = 0
            while height < self.screen_size[1]:
                self.screen.blit(self.image_chain,
                    pygame.Rect(
                            self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_chain.get_width() / 2) - offset.x,
                            self.offset_max_up + height,
                            self.image_chain.get_width(),
                            self.screen_size[1]
                    ),
                )
                height += self.image_chain.get_height()

        if self.is_visible(offset):
            if not self.stopped and not self.sound_playing:
                self.sound_playing = True
                self.game_data.sound_cache.play('laser', loops=-1, volume=self.music_volume_bg_game_effects)
            self._draw(offset)
        else:
            self.stop(fullstop=False)
            self._draw_not_visible(offset)

    def _draw(self, offset):
        """Draws the barrier

        :param offset: The offset
        """
        # Laserbeam
        barrier_width = 0
        max_size = self.screen_size[0] + abs(self.offset_max_left) + self.offset_max_right - self.camera_borders['left'] - (self.camera_borders['right'] / 2) + self.barrier_laser_correction[0] * 2
        while (barrier_width + self.image_laserbeam.get_width()) <= max_size:
            self.screen.blit(self.image_laserbeam,
                pygame.Rect(
                        self.offset_max_left - self.barrier_laser_correction[0] + (self.camera_borders['left'] / 2) + (self.image_barrier_holder_left.get_width() / 3) + self.image_barrier_cannon_right.get_width() + barrier_width - offset.x,
                        self.rect.y - self.barrier_laser_correction[1] - offset.y,
                        self.image_laserbeam.get_width(),
                        self.image_laserbeam.get_height()
                )
            )
            barrier_width += self.image_laserbeam.get_width()
        rect = pygame.Rect(
                self.offset_max_left - self.barrier_laser_correction[0] + self.camera_borders['left'] + self.image_platform.get_width() - offset.x + barrier_width,
                self.rect.y - self.barrier_laser_correction[1] - offset.y,
                max_size - barrier_width,
                self.image_laserbeam.get_height()
        )
        self.screen.blit(self.image_laserbeam, rect, rect)

        if abs(self.offset_max_left - offset.x) < self.camera_borders['left']:
            # Left platform
            self.screen.blit(self.image_platform,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect.y + self.image_platform.get_height() - offset.y,
                        self.image_platform.get_width(),
                        self.image_platform.get_height()
                )
            )

            # Left barrier holder
            self.screen.blit(self.image_barrier_holder_left,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect.y - (self.image_platform.get_height() / 2) - (self.image_barrier_holder_left.get_height() / 2) - offset.y,
                        self.image_barrier_holder_left.get_width(),
                        self.image_barrier_holder_left.get_height()
                )
            )

            # Left cannon
            self.screen.blit(self.image_barrier_cannon_left,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) + (self.image_barrier_holder_left.get_width() / 3) + self.barrier_cannon_left_correction[0] - offset.x,
                        self.rect.y + (self.image_platform.get_height() / 2) - (self.image_barrier_cannon_left.get_height() / 2) + self.barrier_cannon_left_correction[1] - offset.y,
                        self.image_barrier_cannon_left.get_width(),
                        self.image_laserbeam.get_height() + self.image_barrier_cannon_left.get_height()
                )
            )

        if abs(self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x) < (self.screen_size[0] + self.camera_borders['left'] - self.camera_borders['right']):
            # Right platform
            self.screen.blit(self.image_platform,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect.y + self.image_platform.get_height() - offset.y,
                        self.image_platform.get_width(),
                        self.image_platform.get_height()
                )
            )

            # Right barrier holder
            self.screen.blit(self.image_barrier_holder_right,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect.y - (self.image_platform.get_height() / 2) - (self.image_barrier_holder_right.get_height() / 2) - offset.y,
                        self.image_barrier_holder_right.get_width(),
                        self.image_barrier_holder_right.get_height()
                )
            )

            # Right cannon
            self.screen.blit(self.image_barrier_cannon_right,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) + (self.image_barrier_holder_right.get_width() / 3) - self.image_barrier_cannon_right.get_width() + self.barrier_cannon_right_correction[0] - offset.x,
                        self.rect.y + (self.image_platform.get_height() / 2) - (self.image_barrier_cannon_right.get_height() / 2) + self.barrier_cannon_right_correction[1] - offset.y,
                        self.image_barrier_cannon_right.get_width(),
                        self.image_laserbeam.get_height() + self.image_barrier_cannon_right.get_height()
                )
            )

    def _draw_not_visible(self, offset):
        """Draws the barrier

        :param offset: The offset
        """
        # Laserbeam
        barrier_width = 0
        max_size = self.screen_size[0] + abs(self.offset_max_left) + self.offset_max_right - self.camera_borders['left'] - (self.camera_borders['right'] / 2) + self.barrier_laser_correction[0] * 2
        while (barrier_width + self.image_laserbeam.get_width()) <= max_size:
            self.screen.blit(self.image_laserbeam,
                pygame.Rect(
                        self.offset_max_left - self.barrier_laser_correction[0] + (self.camera_borders['left'] / 2) + (self.image_barrier_holder_left.get_width() / 3) + self.image_barrier_cannon_right.get_width() + barrier_width - offset.x,
                        0 - self.barrier_laser_correction[1],
                        self.image_laserbeam.get_width(),
                        self.image_laserbeam.get_height()
                )
            )
            barrier_width += self.image_laserbeam.get_width()
        rect = pygame.Rect(
                    self.offset_max_left - self.barrier_laser_correction[0] + (self.camera_borders['left'] / 2) + (self.image_barrier_holder_left.get_width() / 3) + self.image_barrier_cannon_right.get_width() + barrier_width - offset.x,
                    0 - self.barrier_laser_correction[1],
                    max_size - barrier_width,
                    self.image_laserbeam.get_height()
                )
        self.screen.blit(self.image_laserbeam, rect, rect)
        
        if abs(self.offset_max_left - offset.x) < self.camera_borders['left']:
            # Left platform
            self.screen.blit(self.image_platform,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect_original.y + self.image_platform.get_height(),
                        self.image_platform.get_width(),
                        self.image_platform.get_height()
                )
            )

            # Left barrier holder
            self.screen.blit(self.image_barrier_holder_left,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect_original.y - (self.image_platform.get_height() / 2) - (self.image_barrier_holder_left.get_height() / 2),
                        self.image_barrier_holder_left.get_width(),
                        self.image_barrier_holder_left.get_height()
                )
            )

            # Left cannon
            self.screen.blit(self.image_barrier_cannon_left,
                pygame.Rect(
                        self.offset_max_left + (self.camera_borders['left'] / 2) + (self.image_barrier_holder_left.get_width() / 3) + self.barrier_cannon_left_correction[0] - offset.x,
                        self.rect_original.y + (self.image_platform.get_height() / 2) - (self.image_barrier_cannon_left.get_height() / 2) + self.barrier_cannon_left_correction[1],
                        self.image_barrier_cannon_left.get_width(),
                        self.image_laserbeam.get_height() + self.image_barrier_cannon_left.get_height()
                )
            )

        if abs(self.screen_size[0] + self.offset_max_right - self.camera_borders['right'] - offset.x) < (self.screen_size[0] + self.camera_borders['left'] - self.camera_borders['right']):
            # Right platform
            self.screen.blit(self.image_platform,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect_original.y + self.image_platform.get_height(),
                        self.image_platform.get_width(),
                        self.image_platform.get_height()
                )
            )

            # Right barrier holder
            self.screen.blit(self.image_barrier_holder_right,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) - offset.x,
                        self.rect_original.y - (self.image_platform.get_height() / 2) - (self.image_barrier_holder_left.get_height() / 2),
                        self.image_barrier_holder_right.get_width(),
                        self.image_barrier_holder_right.get_height()
                )
            )

            # Right cannon
            self.screen.blit(self.image_barrier_cannon_right,
                pygame.Rect(
                        self.screen_size[0] + self.offset_max_right - (self.camera_borders['right'] / 2) - (self.image_platform.get_width() / 2) - self.image_barrier_cannon_right.get_width() + (self.image_barrier_holder_right.get_width() / 3) + self.barrier_cannon_right_correction[0] - offset.x,
                        self.rect_original.y + (self.image_platform.get_height() / 2) - (self.image_barrier_cannon_right.get_height() / 2) + self.barrier_cannon_right_correction[1],
                        self.image_barrier_cannon_right.get_width(),
                        self.image_laserbeam.get_height() + self.image_barrier_cannon_right.get_height()
                )
            )

    def collides_with(self, player, offset):
        """Checks whether the barrier collides with the player

        :param player: The player
        :param offset: The offset
        """
        player_top = player.get_rect().top + self.collision_detection_correction_top
        laser_bottom = self.rect.y + (self.image_laserbeam.get_height() / 2) - self.barrier_laser_correction[1] - offset.y
        return player_top < laser_bottom

    def increase_speed(self):
        """Increases the speed of the barrier"""
        self.speed += self.speed_increase
        logging.debug('Barrier speed increased')

    def get_velocity(self, dt):
        """Returns the velocity

        :param dt: Tick rate, milliseconds between each call to 'tick'
        """
        return self.speed * dt
