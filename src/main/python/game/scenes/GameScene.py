#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Game"""

import logging
import random

import pygame

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.sprites.Border import Border
from game.sprites.Barrier import Barrier
from game.sprites.Player import Player
from game.level.Level import Level
from game.Camera import Camera

class GameScene(Scene):
    """Game scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen_size = self.game_data.game_config.get('screen.size')
        self.camera_borders = self.game_data.game_config.get('camera.borders')
        self.music_volume_bg_game = self.game_data.game_config.get('music.volume.background.game')
        self.music_volume_bg_game_effects = self.game_data.game_config.get('music.volume.background.game.effects')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')
        self.game_music = self.game_data.game_config.get('game.music')

        self.background = None
        self.border = None
        self.barrier = None
        self.player = None
        self.level = None
        self.camera = None
        self.sound_played = False
        self.paused = False
        self.playing_music = False
        self.curr_bg_music = ''

        self.game_init_done = False

    def init_game(self):
        """Initializes the game objects"""
        self.sound_played = False

        self.border = Border(self.game_data)
        pos_barrier = (self.screen_size[0] / 2, self.camera_borders['top'])
        self.barrier = Barrier(self.game_data, pos_barrier)

        self.player = Player(self.game_data)
        pos_player = (self.screen_size[0] / 2, self.player.size[1] + self.camera_borders['top'])
        self.player.init(pos_player)

        self.level = Level(self.game_data)
        self.background = Background(self.game_data)
        self.camera = Camera(self.game_data, self.border, self.barrier, self.player, self.background, self.level)

        self.game_init_done = True

    def reset(self):
        """Resets the scene"""
        self.game_init_done = False
        self.init_game()

    def toggle_show_fps(self):
        """Toggles the fps display"""
        self.game_data.game_config.set('fps.show', not self.game_data.game_config.get('fps.show'))

    def loop_visuals(self, tick):
        dt = tick / 1000
        self.camera.loop_visuals(dt)

    def stop_music(self):
        """Stops the music of the scene"""
        self.game_data.sound_cache.stop_music()
        self.playing_music = False

    def loop(self, tick):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_show_fps()
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.paused = True
                    self.camera.pause()
                    self.set_state(State.PAUSE)

        if self.is_state(State.GAME):
            if self.paused:
                self.paused = False
                self.camera.unpause()
            if not self.sound_played:
                self.sound_played = True
                self.game_data.sound_cache.play('game.start', volume=self.music_volume_bg_game_effects)
            dt = tick / 1000
            self.camera.loop(dt, pygame.key.get_pressed())
            if self.camera.game_over:
                self.set_state(State.GAMEOVER)

        if not self.is_state(State.GAME):
            if not self.is_state(State.PAUSE):
                self.game_init_done = False
            self.game_data.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            if not self.is_state(State.PAUSE) and not self.is_state(State.GAMEOVER):
                self.stop_music()
            return
        else:
            if not self.game_init_done:
                logging.error('Game is not initialized.')
                self.set_state(State.PLAYERSELECTION)
                self.stop_music()
                return
            if not self.playing_music:
                self.playing_music = True
                self.curr_bg_music = random.choice(self.game_music)
                self.game_data.sound_cache.load_music(self.curr_bg_music)
                self.game_data.sound_cache.play_music(loops=-1, volume=self.music_volume_bg_game)

    def draw(self, show_score=True, show_fps=True):
        """Draws the game scene

        :param show_score: Flag whether to show the score
        :param show_fps: Flag whether to show the fps, shows only if toggled on
        """
        self.camera.draw(show_score=show_score, show_fps=show_fps)
