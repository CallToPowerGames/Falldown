#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""I18n"""

import logging
import time
from pathlib import Path

from lib.Utils import load_languages, load_i18n

class I18n():
    """I18n"""

    _translations = {
        'game.name': 'Falldown',
        'game.version': 'Version {} Build {}',
        'game.by': 'A game by {}',
        'player.name.unknown': 'Unknown',
        'player.name.1': 'Grumpy Stone',
        'player.name.2': 'Pink Pan',
        'player.name.3': 'VR Guy',
        'player.name.4': 'Drug Frenzy Bunny',
        'player.name.5': 'Crazy Chicken',
        'player.name.6': 'Shroomie',
        'player.name.7': 'Rhino',
        'player.name.8': 'Fastest Snail Alive',
        'scene.pause.score': 'Score: {}',
        'scene.gameover.score': 'Score: {}',
        'scene.game.fps': 'FPS: {}',
        'scene.pause.pause': 'Pause',
        'scene.pause.help': 'Press <Space> to continue, <Escape> to end the game.',
        'scene.gameover.gameover': 'Game over!',
        'scene.gameover.help': 'Press <Enter> or <Escape> to end the game.',
        'scene.exit.txt': 'Bye!',
        'scene.game.score': 'Score: {}',
        'scene.game.go': 'Go, {}!',
        'scene.ai.ai_playing': '"{}" AI',
        'menu.loading.loading.txt': 'Loading...',
        'menu.loading.loading.sounds.txt': 'Loading the sounds...',
        'menu.loading.loading.sprites.txt': 'Loading the images...',
        'menu.loading.loading.highscore.txt': 'Loading the highscore...',
        'menu.loading.loading.menu.txt': 'Loading the menu...',
        'menu.loading.loading.game.txt': 'Loading the game...',
        'menu.loading.loading.background_level.txt': 'Loading background level...',
        'menu.loading.loading.done.txt': 'Loading done.',
        'menu.item.player.speed.start': 'Speed start: {}, {}',
        'menu.item.player.speed.max': 'Speed max: {}, {}',
        'menu.item.player.speed.increase': 'Speed +: {}, {}',
        'menu.item.player.speed.decrease': 'Speed -: {}',
        'menu.item.player.falling.increase': 'Fall +: {}',
        'menu.highscore.txt': 'Highscore',
        'menu.highscore.help': 'Press <Enter> to open the highscore list.',
        'menu.options.txt': 'Options',
        'menu.options.help': 'Press <Enter> for options.',
        'menu.fullscreen.txt': 'Fullscreen',
        'menu.fullscreen.help': 'Press <Enter> to toggle between fullscreen and window mode.',
        'menu.start_game.txt': 'Start Game',
        'menu.start_game.help': 'Press <Enter> to start a new game.',
        'menu.quit_game.txt': 'Quit Game',
        'menu.quit_game.help': 'Press <Enter> to quit game.',
        'menu.playerselection.txt': 'Player Selection',
        'menu.playerselection.help': 'Use <Arrows> to select a player, press <Enter> to start a game. Press <Tab> to show additional info.',
        'menu.playerselection.showinfo.help': 'Use <Arrows> to select a player, press <Enter> to start a game. Press <Tab> to hide additional info.',
        'menu.random.txt': 'Random',
        'menu.random.help': 'Press <Enter> to start a game with a random player.',
        'menu.language.txt': 'Language',
        'menu.language.help': 'Press <Enter> to switch the language.',
        'menu.background.txt': 'Background image',
        'menu.background.help': 'Press <Enter> to show or hide the background image.',
        'menu.back.txt': 'Back',
        'menu.back.help': 'Press <Enter> to get back to the menu.',
        'menu.back.highscore.txt': 'Back',
        'menu.back.highscore.help': 'Use <Arrow-Up> and <Arrow-Down> to scroll the highscore. Press <Enter> to get back to the menu.'
    }

    def __init__(self, game_config, basedir):
        """Initializes the I18n

        :param game_config: The game configuration
        :param basedir: The base path
        """
        logging.debug('Initializing I18n')

        self.game_config = game_config
        self.basedir = basedir

        self.languages = load_languages(self.basedir)
        self.language_main = self.game_config.get('languages.main')

        self._init()

    def _init(self):
        """Initializes the translations"""
        lang = self.languages[self.languages.index(self.language_main)] if self.language_main in self.languages else self.languages['en']
        self.load_language(lang)

    def load_language(self, lang):
        """Loads a language"""
        translations = load_i18n(self.basedir, lang)
        for key, val in translations.items():
            if key in self._translations:
                logging.debug('Overwriting: {}: {}'.format(key, val))
                self.set(key, val)
            else:
                logging.warn('Key-Value pair not found: {}, {}'.format(key, val))

    def switch_language(self):
        """Switches between languages"""
        i = self.languages.index(self.language_main) + 1
        if i >= len(self.languages):
            i = 0
        self.language_main = self.languages[i]
        logging.info('Switched language to "{}"'.format(self.language_main))
        lang = self.languages[self.languages.index(self.language_main)] if self.language_main in self.languages else self.languages['en']
        self.load_language(lang)
        self.game_config.set('languages.main', lang)
        self.game_config.save_game_conf()

    def set(self, key, value):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        """
        self._translations[key] = value

    def get(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._translations[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default
