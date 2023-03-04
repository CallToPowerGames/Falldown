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

from lib.AppConfig import app_conf_set
from lib.GameConfig import GameConfig
from lib.FontCache import FontCache
from lib.SoundCache import SoundCache
from lib.SpriteCache import SpriteCache
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
        self.font_cache = FontCache()
        self.sound_cache = SoundCache(self.basedir)
        self.sprite_cache = SpriteCache(self.basedir)
        self.cryptography = Cryptography(self.basedir)

        self._init_modules()
        self._cache_fonts()
        self._cache_sounds()
        self._cache_sprites()

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
            pygame.mixer.init()
        else:
            raise SystemExit("Sound module required")

    def _cache_fonts(self):
        """Caches the fonts"""
        logging.info('Caching fonts')
        font_sizes = self.game_config.get('font.sizes')
        try:
            main_font_dir = os.path.join(self.basedir, 'resources', 'fonts')
            font_path = os.path.join(self.game_config.get('font.main.path'), self.game_config.get('font.main.name'))
            logging.debug('Loading font "{}" from directory "{}"'.format(font_path, main_font_dir))
            font_dpcomic = os.path.join(main_font_dir, font_path)
            for font_size in font_sizes:
                self.font_cache.set('main.{}'.format(font_size), pygame.font.Font(font_dpcomic, self.game_config.get('font.main.{}.size'.format(font_size))))
        except Exception as e:
            font_system = self.game_config.get('font.system')
            logging.error('Could not find font "{}", falling back to system font "{}"', font_dpcomic, font_system)
            for font_size in font_sizes:
                self.font_cache.set('main.{}'.format(font_size), pygame.font.Font(font_system, self.game_config.get('font.main.{}.size'.format(font_size))))

    def _cache_sounds(self):
        """Caches the sounds"""
        logging.info('Caching background sounds')

    def _cache_sprites(self):
        """Caches the sprites"""
        logging.info('Caching background sprites')
        self.sprite_cache.get_or_load('app.logo', 'logo-app.png')
        self.sprite_cache.get_or_load('bg.clouds', 'clouds.png', 'sprites')
        self.sprite_cache.get_or_load('banner', 'banner.png', 'items')
        self.sprite_cache.get_or_load('button.none', 'button-none.png', 'items')
        self.sprite_cache.get_or_load('loader', 'loader.png', 'items')
        self.sprite_cache.get_or_load('loader.filler', 'loader-filler.png', 'items')

    def run(self):
        """Initializes and shows the GUI"""
        logging.info('Initializing AppContext GUI')

        return self.game.loop()
