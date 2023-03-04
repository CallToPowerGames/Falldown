#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

"""The translation table"""

_translations = {
    'game.name': 'Falldown',
    'game.version': 'Version {}',
    'game.by': 'A game by {}',
    'scene.pause.score': 'Score: {}',
    'scene.game.fps': 'FPS: {}',
    'scene.pause.pause': 'Pause',
    'scene.pause.help': 'Press <Space> to continue, <Escape> to quit',
    'scene.gameover.gameover': 'Game over!',
    'scene.gameover.help': 'Press <Enter> or <Escape> to quit',
    'scene.exit.txt': 'Bye!',
    'scene.game.score': 'Score: {}',
    'scene.game.go': 'Go, {}!',
    'menu.highscore.txt': 'Highscore',
    'menu.highscore.help': 'Press <Enter> to see the highscore list',
    'menu.options.txt': 'Options',
    'menu.options.help': 'Press <Enter> for more options',
    'menu.fullscreen.txt': 'Toggle fullscreen',
    'menu.fullscreen.help': 'Press <Enter> to toggle between fullscreen and window mode.',
    'menu.start_game.txt': 'Start Game',
    'menu.start_game.help': 'Press <Enter> to start a new game',
    'menu.quit_game.txt': 'Quit Game',
    'menu.quit_game.help': 'Press <Enter> to quit game',
    'menu.playerselection.txt': 'Player Selection',
    'menu.playerselection.help': 'Use <Arrows> to select a player, press <Enter> to start a game.',
    'menu.random.txt': 'Random',
    'menu.random.help': 'Press <Enter> to start a game with a random player.',
    'menu.back.txt': 'Back',
    'menu.back.help': 'Press <Enter> to get back to the menu',
    'menu.back.highscore.txt': 'Back',
    'menu.back.highscore.help': 'Press <Enter> to get back to the menu, <Arrow-Up> and <Arrow-Down> to scroll the highscore.'
}


def translate(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key to be translated
    :param default: The default if no value could be found for the key
    """
    try:
        return _translations[key]
    except KeyError as exception:
        logging.error(
            'Returning default for key "{}": "{}"'.format(key, exception))
        return default
