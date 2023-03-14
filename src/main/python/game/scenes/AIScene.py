#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - AI"""

import logging
import random

import pygame

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Border import Border
from game.sprites.Barrier import Barrier
from game.sprites.Player import Player
from game.level.Level import Level
from game.Camera import Camera
from game.PlayerAI import PlayerAI
from game.drawables.MenuItem import MenuItem
from game.drawables.DrawableUtils import draw_text_in_rect

class AIScene(Scene):
    """AI scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen_size = self.game_data.game_config.get('screen.size')
        self.camera_borders = self.game_data.game_config.get('camera.borders')
        self.music_volume_bg_game = self.game_data.game_config.get('music.volume.background.game')
        self.music_volume_bg_game_effects = self.game_data.game_config.get('music.volume.background.game.effects')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')
        self.game_music = self.game_data.game_config.get('game.music')
        self.screen = self.game_data.game_config.get('screen')
        self.text_color_ai_text = self.game_data.game_config.get('text.color.ai_text')
        self.font_l = self.game_data.cache.font_cache.get('main.l')
        self.font_s = self.game_data.cache.font_cache.get('main.s')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_help = self.game_data.game_config.get('text.color.help')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.ai_init_done = False
        self.border = None
        self.barrier = None
        self.player = None
        self.level = None
        self.camera = None
        self.player_ai = None
        self.sound_played = False
        self.paused = False
        self.playing_music = False
        self.curr_bg_music = ''
        self.ai_txt = ''
        self.width_ai_text = len(self.ai_txt) * 50
        self.height_ai_text = 50
        self.ai_text_max_alpha = 240
        self.ai_text_min_alpha = 15
        self.ai_text_alpha = self.ai_text_min_alpha + 5
        self.ai_text_factor = 1
        self.item_logo = None
        self.ai_txt_y_plus = 40

        self._init_items()

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        # Logo
        width = 380
        height = 100
        rect = (self.screen_mid[0] / 2 - width / 2 + 30, 0, width, height)
        self.item_logo = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0] / 2 + 10 + 30, height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('game.name'),
                                    banner=True
                                )
        self.items.append(self.item_logo)
        
        # Help
        width = self.screen_size[0] - 20
        height = 80
        rect = (self.screen_mid[0] - width / 2, self.screen_size[1] - height - 10, width, height)
        self.item_help = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_help,
                                    text=self.game_data.i18n.get('scene.ai.help'),
                                    rotate=True,
                                    rotate_ticks_max=16,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def init_game(self):
        """Initializes the game objects"""
        self.sound_played = False

        self.border = Border(self.game_data)
        pos_barrier = (self.screen_size[0] / 2, self.camera_borders['top'])
        self.barrier = Barrier(self.game_data, pos_barrier)

        self.player = Player(self.game_data, self.game_data.player_info)
        pos_player = (self.screen_size[0] / 2, self.player.size[1] + self.camera_borders['top'])
        self.player.init(pos_player)

        self.level = Level(self.game_data)
        self.camera = Camera(self.game_data, self.level, self.border, self.barrier, self.player)

        self.player_ai = PlayerAI(self.game_data, self.player, self.level, self.camera)

        self.ai_txt = self.game_data.i18n.get('scene.ai.ai_playing').format(self.game_data.player_info['name'])
        self.width_ai_text = len(self.ai_txt) * 50
        self.height_ai_text = 50
        self.ai_text_max_alpha = 240
        self.ai_text_min_alpha = 15
        self.ai_text_alpha = self.ai_text_min_alpha + 5
        self.ai_text_factor = 1

        self.ai_init_done = True

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))
        self.item_help.set_text(self.game_data.i18n.get('scene.ai.help'))

    def reset(self):
        """Resets the scene"""
        self.ai_init_done = False
        self.border = None
        self.barrier = None
        self.player = None
        self.level = None
        self.camera = None

        self.init_game()

    def stop_music(self):
        """Stops the music of the scene"""
        self.game_data.cache.sound_cache.stop_music()
        self.playing_music = False

    def _back_to_menu(self):
        """Goes back to menu"""
        self.stop_music()
        self.game_data.background.reset(initialize_background_level=True)
        self.set_state(State.MENU)

    def loop(self, tick):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                self._back_to_menu()
                return

        if self.is_state(State.AI):
            if not self.ai_init_done:
                logging.error('AI is not initialized.')
                self._back_to_menu()
                return
            if not self.sound_played:
                self.sound_played = True
                self.game_data.cache.sound_cache.play('game.start', volume=self.music_volume_bg_game_effects)
            if not self.playing_music:
                self.playing_music = True
                self.curr_bg_music = random.choice(self.game_music)
                self.game_data.cache.sound_cache.load_music(self.curr_bg_music)
                self.game_data.cache.sound_cache.play_music(loops=-1, volume=self.music_volume_bg_game)
            elif not self.game_data.cache.sound_cache.is_playing():
                self.playing_music = False
            dt = tick / 1000
            self.game_data.background.loop(dt, self.camera.offset)
            keys_pressed = self.player_ai.loop()
            self.camera.loop(dt, keys_pressed)
            if self.camera.game_over:
                self._back_to_menu()
        else:
            self.ai_init_done = False
            self.game_data.cache.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            self.stop_music()
            self.game_data.background.reset(initialize_background_level=True)

    def draw(self):
        """Draws the game scene"""
        if not self.ai_init_done:
            self._back_to_menu()
            return

        self.game_data.background.draw()
        self.camera.draw(show_score=True, show_fps=False)

        if not self.camera.show_go:
            self.ai_text_alpha += self.ai_text_factor
            if self.ai_text_alpha > self.ai_text_max_alpha or self.ai_text_alpha < self.ai_text_min_alpha:
                self.ai_text_factor *= -1
            draw_text_in_rect(
                self.screen,
                self.ai_txt,
                self.text_color_ai_text,
                self.font_l,
                (self.screen_size[0] - self.width_ai_text, 0, self.width_ai_text, self.height_ai_text),
                (self.screen_mid[0], self.screen_mid[1] / 2 + self.ai_txt_y_plus),
                alpha=self.ai_text_alpha
            )

        for item in self.items:
            item.loop()
            if not item == self.item_help:
                item.draw()
            else:
                item.draw(alpha=self.ai_text_alpha)
