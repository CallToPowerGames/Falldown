#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Camera"""

import logging

import pygame

from game.drawables.MenuItem import MenuItem
from game.drawables.DrawableUtils import draw_text_in_rect


class Camera():
    """The camera"""

    def __init__(self, game_data, border, barrier, player, background, level):
        """Initializes the camera

        :param game_data: The game data
        :param border: The border
        :param barrier: The barrier
        :param player: The player
        :param background: The background
        :param level: The level
        """
        logging.info('Initializing camera')

        self.game_data = game_data
        self.border = border
        self.barrier = barrier
        self.player = player
        self.background = background
        self.level = level

        self.screen = self.game_data.game_config.get('screen')
        self.font_xs = self.game_data.cache.font_cache.get('main.xs')
        self.font_s = self.game_data.cache.font_cache.get('main.s')
        self.font_l = self.game_data.cache.font_cache.get('main.l')
        self.segment_height = self.game_data.game_config.get('level.segments.height')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.camera_borders = self.game_data.game_config.get('camera.borders')
        self.offset_max_left = self.game_data.game_config.get('offset.max.left')
        self.offset_max_right = self.game_data.game_config.get('offset.max.right')
        self.offset_max_up = self.game_data.game_config.get('offset.max.up')
        self.text_color_score = self.game_data.game_config.get('text.color.score')
        self.text_color_go = self.game_data.game_config.get('text.color.go')
        self.fps_text_color = self.game_data.game_config.get('fps.text.color')
        self.player_stuck_correction = self.game_data.game_config.get('player.stuck.correction')
        self.player_barrier_move_correction = self.game_data.game_config.get('player.barrier.move.correction')
        self.debug_show = self.game_data.game_config.get('debug.show')
        self.start_barrier = self.game_data.game_config.get('debug.barrier.start')
        self.music_volume_bg_game_effects = self.game_data.game_config.get('music.volume.background.game.effects')
        self.music_volume_bg_game = self.game_data.game_config.get('music.volume.background.game')
        self.music_volume_bg_game_barriervisible = self.game_data.game_config.get('music.volume.background.game.barriervisible')
        self.nr_iterations_show_go = self.game_data.game_config.get('level.iterations.showgo')
        self.collision_detection_correction_bottom = self.game_data.game_config.get('level.collision.detection.correction.bottom')
        self.segment_moving_decrease_factor = self.game_data.game_config.get('level.segment.moving.decrease.factor')
        self.player_stuck_threshold = self.game_data.game_config.get('player.stuck.threshold')
        self.barrier_start_after_lines = self.game_data.game_config.get('barrier.start.after.lines')
        self.score_plus = self.game_data.game_config.get('score.plus')
        self.score_plus_clear_linesegment = self.game_data.game_config.get('score.plus.clear.linesegment')
        self.score_plus_clear_all = self.game_data.game_config.get('score.plus.clear.all')

        self.nr_lines_created_since_last_clean = 0
        self.clean_every_n_created_lines = 10
        self.offset = pygame.math.Vector2()
        self.player_first_time_colliding_left = True
        self.player_first_time_colliding_right = True
        self.player_first_time_colliding_bottom = True
        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.show_go = True
        self.nr_it_show_go = self.nr_iterations_show_go

        self.camera_rect = pygame.Rect(
            self.camera_borders['left'],
            self.camera_borders['top'],
            self.screen_size[0] - self.camera_borders['left'] - self.camera_borders['right'],
            self.screen_size[1] - self.camera_borders['top']- self.camera_borders['bottom']
        )

        self.music_volume = 0

        self.velocity_player = [0, 0]
        self.velocity_barrier = 0

        self.game_data.score = 0
        width_score = 300
        height_score = 50
        rect = (self.screen_size[0] - width_score - 10, 10, width_score, height_score)
        self.item_score = MenuItem(
                                self.game_data,
                                self.font_s,
                                rect,
                                (self.screen_size[0] - width_score / 2 - 5, height_score / 2 + 10),
                                width=width_score,
                                height=height_score,
                                color=self.text_color_score,
                                rect_width=-1,
                                text=self.game_data.i18n.get('scene.game.score').format(self.game_data.score),
                                banner=True
                            )

        self.game_over = False

    def stop(self):
        """Stops"""
        self.barrier.stop()

    def pause(self):
        """Pauses"""
        self.barrier.pause()

    def unpause(self):
        """Unpauses"""
        self.barrier.unpause()

    def _player_move_left(self, velocity):
        """Moves the player left

        :param velocity: The x velocity
        """
        self.player.rect.x -= velocity
        if self.player.rect.left < self.camera_rect.left:
            self.player.rect.left = self.camera_rect.left
            self.offset.x -= velocity
            if self.offset.x < self.offset_max_left:
                self.offset.x = self.offset_max_left
                self.player.reset_speed_x()

    def _player_move_right(self, velocity):
        """Moves the player right

        :param velocity: The x velocity
        """
        self.player.rect.x += velocity
        if self.player.rect.right > self.camera_rect.right:
            self.player.rect.right = self.camera_rect.right
            self.offset.x += velocity
            if self.offset.x > self.offset_max_right:
                self.offset.x = self.offset_max_right
                self.player.reset_speed_x()

    def _player_move_top(self, velocity):
        """Moves the player top

        :param velocity: The y velocity
        """
        self.player.rect.y = self.player.rect.y - velocity
        if self.player.rect.top < self.camera_rect.top:
            self.player.rect.top = self.camera_rect.top
            self.offset.y -= velocity
            if self.offset.y < self.offset_max_up:
                self.offset.y = self.offset_max_up

    def _player_move_bottom_ignore_collision(self, velocity):
        """Moves the player bottom

        :param velocity: The y velocity
        """
        player_rect = self.player.rect
        player_plus_velocity_y = player_rect.y + player_rect.height + velocity
        if player_plus_velocity_y <= self.camera_rect.bottom:
            self.player.rect.y = self.player.rect.y + velocity
        else:
            self.player.rect.y = self.camera_rect.bottom - self.player.rect.height
            self.offset.y += velocity
        
        self.player.falling = True
        self.player_first_time_colliding_bottom = True

    def _player_move_bottom(self, velocity, segment_top_y):
        """Moves the player bottom

        :param velocity: The y velocity
        :param segment_top_y: The y of the segment
        """
        collides = False
        player_rect = self.player.rect
        player_plus_velocity_y = player_rect.y + player_rect.height + velocity
        segment_top_y_corr = segment_top_y - self.collision_detection_correction_bottom
        if player_plus_velocity_y <= self.camera_rect.bottom:
            if segment_top_y > 0 and player_plus_velocity_y >= segment_top_y_corr:
                self.player.rect.y = segment_top_y - self.player.rect.height
                collides = True
            else:
                self.player.rect.y = self.player.rect.y + velocity
        else:
            if segment_top_y > 0 and player_plus_velocity_y >= segment_top_y_corr:
                old_y = self.player.rect.y
                self.player.rect.y = segment_top_y - self.player.rect.height
                corrected_velocity = velocity - abs(self.player.rect.y - old_y)
                self.offset.y += abs(corrected_velocity)
                collides = True
            else:
                self.player.rect.y = self.camera_rect.bottom - self.player.rect.height
                self.offset.y += velocity
        
        if collides:
            if self.player_first_time_colliding_bottom:
                self.player_first_time_colliding_bottom = False
                self.game_data.cache.sound_cache.play('bump', volume=self.music_volume_bg_game_effects)
            self.player.reset_speed_y()
        else:
            self.player.falling = True
            self.player_first_time_colliding_bottom = True

    def _update_current_key(self, keys):
        """Updates the current key on the player

        :param keys: The keys
        """
        self.player.current_key = None
        if not (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
            if keys[pygame.K_LEFT]:
                self.player.current_key = pygame.K_LEFT
            elif keys[pygame.K_RIGHT]:
                self.player.current_key = pygame.K_RIGHT


    def _clean_and_generate_new_level_elements(self):
        """Cleans up and - if it's time - generates new level elements"""
        if self.level.last_y < (self.offset.y + self.screen_size[1] + self.segment_height):
            logging.debug('Generating next line...')
            self.level.generate_new_line()
            self.nr_lines_created_since_last_clean += 1
            if self.level.nr_or_lines_generated > self.barrier_start_after_lines:
                if self.start_barrier:
                    self.barrier.started = True
                    self.barrier.increase_speed()
                self.game_data.score += self.score_plus
        if self.nr_lines_created_since_last_clean >= self.clean_every_n_created_lines:
            self.level.clean(self.offset.y)
            logging.debug('#Lines: {}'.format(len(self.level._lines)))
            self.nr_lines_created_since_last_clean = 0

    def _check_game_over(self):
        """Checks whether the game is over and sets a flag"""
        if self.barrier.is_visible(self.offset):
            if self.music_volume != self.music_volume_bg_game_barriervisible:
                self.music_volume = self.music_volume_bg_game_barriervisible
                self.game_data.cache.sound_cache.set_music_volume(self.music_volume)
            if self.barrier.collides_with(self.player, self.offset):
                logging.info('Player collided with barrier')
                self.game_data.cache.sound_cache.play('game.over', volume=self.music_volume_bg_game_effects)
                self.stop()
                self.game_data.cache.sound_cache.set_music_volume(self.music_volume_bg_game)
                self.game_over = True
        elif self.music_volume != self.music_volume_bg_game:
            self.music_volume = self.music_volume_bg_game
            self.game_data.cache.sound_cache.set_music_volume(self.music_volume_bg_game)

    def loop_visuals(self, dt):
        self.background.loop(dt)
        self.level.loop_visuals(dt)
        self.barrier.update_sprite()
        self.player.update_sprite()

    def loop(self, dt, keys):
        """Updates the camera

        :param dt: Tick rate, milliseconds between each call to 'tick'
        :param keys: The keys
        """
        self.background.loop(dt)
        self.level.loop(dt)
        self.item_score.loop()

        if self.game_over:
            return

        if self.show_go:
            self.nr_it_show_go -= 1
            if self.nr_it_show_go <= 0:
                self.show_go = False

        self._clean_and_generate_new_level_elements()

        self._update_current_key(keys)

        self.velocity_player = self.player.get_velocity(dt)

        # Collision detection and more
        collisioninfo = self.level.collides_with(self.player, dt, self.velocity_player, keys, self.offset)

        # Handle "Powers"
        if collisioninfo.collides_clear_linesegment:
            self.level.clear_line_segment(collisioninfo.index_line_colliding, collisioninfo.index_segment_colliding)
            self.game_data.score += self.score_plus_clear_linesegment
            self.game_data.cache.sound_cache.play('clear.line', volume=self.music_volume_bg_game_effects)
        if collisioninfo.collides_clear_all:
            self.level.clear_all()
            self.nr_lines_created_since_last_clean = 0
            self.game_data.score += self.score_plus_clear_all
            self.game_data.cache.sound_cache.play('clear.all', volume=self.music_volume_bg_game_effects)
        if collisioninfo.collides_clear_linesegment or collisioninfo.collides_clear_all:
            if self.barrier.started:
                self.barrier.increase_speed()
            return

        # Handle left side colisions
        if collisioninfo.collides_left:
            if self.player_first_time_colliding_left:
                self.player_first_time_colliding_left = False
        else:
            self.player_first_time_colliding_left = True

        # Handle right side colisions
        if collisioninfo.collides_right:
            if self.player_first_time_colliding_right:
                self.player_first_time_colliding_right = False
        else:
            self.player_first_time_colliding_right = True

        # Handle standing on a moving segment
        if collisioninfo.stands_on_moving_segment:
            # Slow speed
            if (collisioninfo.segment_speed < 0 and keys[pygame.K_RIGHT]) or (collisioninfo.segment_speed > 0 and keys[pygame.K_LEFT]):
                if self.segment_moving_decrease_factor > 0:
                    self.velocity_player[0] = self.velocity_player[0] / self.segment_moving_decrease_factor
            # Move with moving segments
            if collisioninfo.segment_speed < 0 and self.player.can_go_left():
                self._player_move_left((abs(collisioninfo.segment_speed) - self.player_barrier_move_correction) * dt)
            elif collisioninfo.segment_speed > 0 and self.player.can_go_right():
                self._player_move_right((collisioninfo.segment_speed + self.player_barrier_move_correction) * dt)

        # Slide move
        if self.player.is_sliding():
            if self.player.is_going_left() and not collisioninfo.collides_left:
                self._player_move_left(self.velocity_player[0])
            elif self.player.is_going_right() and not collisioninfo.collides_right:
                self._player_move_right(self.velocity_player[0])
        # Normal move
        else:
            if keys[pygame.K_LEFT] and not collisioninfo.collides_left:
                self._player_move_left(self.velocity_player[0])
            elif keys[pygame.K_RIGHT] and not collisioninfo.collides_right:
                self._player_move_right(self.velocity_player[0])

        # Left/Right stuck move (stuck correction)
        corrected_top = False
        if collisioninfo.collides_bottom:
            c_left = collisioninfo.collides_left and self.player.can_go_left() and keys[pygame.K_LEFT]
            c_right = collisioninfo.collides_right and self.player.can_go_right() and keys[pygame.K_RIGHT]
            player_plus_velocity_y = self.player.rect.y + self.player.rect.height + self.velocity_player[1]
            if (self.player.rect.y + self.velocity_player[1]) > (collisioninfo.segment_top_y - self.player.get_rect().height):
                if collisioninfo.collides_left or collisioninfo.collides_right:
                    self.player.half_speed_x()
                    self._player_move_bottom_ignore_collision(self.velocity_player[1])
                    corrected_top = True
            elif (player_plus_velocity_y < (collisioninfo.segment_top_y + self.player_stuck_threshold)) and (c_left or c_right):
                self._player_move_top(self.player_stuck_correction)
                corrected_top = True
                if c_left:
                    self._player_move_left(self.velocity_player[0])
                elif c_right:
                    self._player_move_right(self.velocity_player[0])

        # Fall down
        if not corrected_top and self.velocity_player[1] >= 0:
            self._player_move_bottom(self.velocity_player[1], collisioninfo.segment_top_y)

        # Move the barrier
        if self.barrier.started:
            self.barrier.rect.y += self.barrier.get_velocity(dt)

        # Update all sprites
        self.barrier.update_sprite()
        self.player.update_sprite()

        self._check_game_over()

    def draw(self, show_score=True, show_fps=True):
        """Draws all elements of the camera

        :param show_score: Flag whether to show the score
        :param show_fps: Flag whether to show the fps, shows only if toggled on
        """
        self.background.draw(self.offset)
        self.level.draw(self.offset)
        self.border.draw(self.offset)
        self.player.draw()
        self.barrier.draw(self.offset)

        if self.show_go:
            txt = self.game_data.i18n.get('scene.game.go').format(self.game_data.player_info['name'])
            width_go = len(txt) * 50
            height_go = 50
            draw_text_in_rect(
                self.screen,
                txt,
                self.text_color_go,
                self.font_l,
                (self.screen_size[0] - width_go, 0, width_go, height_go),
                self.screen_mid
            )

        # Score
        if show_score:
            self.item_score.set_text(self.game_data.i18n.get('scene.game.score').format(self.game_data.score))
            self.item_score.draw()

        # FPS information
        if show_fps and self.game_data.game_config.get('fps.show'): # read everytime from config!
            width_fps = 100
            height_fps = 40
            draw_text_in_rect(
                self.screen,
                self.game_data.i18n.get('scene.game.fps').format(int(self.game_data.fps)),
                self.fps_text_color,
                self.font_xs,
                (0, 0, width_fps, height_fps),
                (width_fps / 2, height_fps / 2)
            )

        # Debug information
        if self.debug_show:
            # Camera borders
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                pygame.Rect(
                    self.camera_borders['left'],
                    self.camera_borders['top'],
                    self.screen_size[0] - self.camera_borders['left'] - self.camera_borders['right'],
                    self.screen_size[1] - self.camera_borders['top'] - self.camera_borders['bottom']
                ),
                width=3
            )
