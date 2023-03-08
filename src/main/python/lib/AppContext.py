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
from cache.Cache import Cache
from i18n.I18n import I18n
from config.GameConfig import GameConfig
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
        self.i18n = I18n(self.basedir, self.game_config)
        self.cache = Cache(self.basedir, self.game_config)
        self.cryptography = Cryptography(self.basedir)

        update_logging(self.game_config.get('logging.level'), logtofile=self.game_config.get('logging.logtofile'))
        log_app_info()

        self._init_modules()
        self.cache.cache_font()
        self.cache.cache_initial_sprites()

        self.highscore = Highscore(self.cryptography, self.basedir, max_entries=self.game_config.get('highscore.entries.max'))
        self.game_data = GameData(self.game_config, self.i18n, self.highscore, self.cache)
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
            raise SystemExit('Sound module required')

    def run(self):
        """Initializes and start the game loop"""
        logging.info('Initializing AppContext')

        return self.game.loop()
