#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Application Context"""

import os
from pathlib import Path
import logging

import pygame

from config.AppConfig import app_conf_set
from lib.Utils import update_logging, log_app_info
from config.GameConfig import GameConfig
from cache.FontCache import FontCache
from cache.SoundCache import SoundCache
from cache.SpriteCache import SpriteCache
from game.GameData import GameData
from game.Game import Game
from lib.Cryptography import Cryptography
from lib.Highscore import Highscore

class AppContext():
    """Application Context"""

    def __init__(self, basedir):
        """Initializes the GUI

        :param appconfig: The AppConfig
        :param basedir: The base directory
        """
        super().__init__()

        logging.debug('Initializing AppContext')

        self.basedir = basedir

        self.game_config = GameConfig(self.basedir)
        self.font_cache = FontCache(self.basedir)
        self.sound_cache = SoundCache(self.basedir)
        self.sprite_cache = SpriteCache(self.basedir)
        self.cryptography = Cryptography(self.basedir)

        update_logging(self.game_config.get('logging.level'), logtofile=self.game_config.get('logging.logtofile'))
        log_app_info()

        self._init_modules()
        self._cache_initial_fonts()
        self._cache_initial_sounds()
        self._cache_initial_sprites()

        self.highscore = Highscore(self.cryptography, self.basedir, max_entries=self.game_config.get('highscore.entries.max'))
        self.game_data = GameData(self.game_config, self.highscore, self.font_cache, self.sound_cache, self.sprite_cache)
        self.game = Game(self.game_data)

    def _init_modules(self):
        """Initializes pygame modules

        :return: True if all modules are supported, False else
        """
        logging.info('Initializing modules')
        logging.info('Initializing extended image module')
        if not pygame.image.get_extended():
            raise SystemExit("Extended image module required")
        logging.info('Initializing font module')
        if pygame.font:
            pygame.font.init()
        else:
            raise SystemExit("Font module required")
        logging.info('Initializing mixer module')
        if pygame.mixer:
            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.mixer.init()
        else:
            raise SystemExit("Sound module required")

    def _cache_initial_fonts(self):
        """Caches the initial fonts"""
        logging.info('Caching initial fonts')
        font_sizes = self.game_config.get('font.sizes')
        name = self.game_config.get('font.main.name')
        system_font_name = self.game_config.get('font.system')
        font_path = self.game_config.get('font.main.path')
        for font_size in font_sizes:
            key = 'main.{}'.format(font_size)
            size = self.game_config.get('font.main.{}.size'.format(font_size))
            self.font_cache.get_or_load(key, name, size, system_font_name, font_path)

    def _cache_initial_sounds(self):
        """Caches the initial sounds"""
        logging.info('Caching initial sounds')

    def _cache_initial_sprites(self):
        """Caches the initial sprites"""
        logging.info('Caching initial sprites')
        self.sprite_cache.get_or_load('app.logo', 'logo-app.png')
        self.sprite_cache.get_or_load('bg.clouds', 'clouds.png', 'sprites/bg')
        self.sprite_cache.get_or_load('loader', 'loader.png', 'items/loading')
        self.sprite_cache.get_or_load('loader.filler', 'loader-filler.png', 'items/loading')
        self.sprite_cache.get_or_load('banner', 'banner.png', 'items')
        self.sprite_cache.get_or_load('button.none', 'button-none.png', 'items/buttons')

    def run(self):
        """Initializes and shows the GUI"""
        logging.info('Initializing AppContext GUI')

        return self.game.loop()
