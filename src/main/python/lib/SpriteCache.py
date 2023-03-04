#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

from lib.Utils import load_image

"""SpriteCache"""

class SpriteCache():
    """SpriteCache"""

    _cache = {
        'app.logo': None,
        'sprite.player.idle.1': None,
        'sprite.player.run.1': None,
        'sprite.player.idle.2': None,
        'sprite.player.run.2': None,
        'sprite.player.idle.3': None,
        'sprite.player.run.3': None,
        'sprite.player.idle.4': None,
        'sprite.player.run.4': None,
        'sprite.player.idle.5': None,
        'sprite.player.run.5': None,
        'sprite.player.idle.6': None,
        'sprite.player.run.6': None,
        'sprite.player.idle.7': None,
        'sprite.player.run.7': None,
        'sprite.player.idle.8': None,
        'sprite.player.run.8': None,
        'barrier.holder.left': None,
        'barrier.holder.right': None,
        'barrier.platform': None,
        'barrier.chain': None,
        'barrier.cannon': None,
        'barrier.laserbeam.1': None,
        'barrier.laserbeam.2': None,
        'barrier.laserbeam.3': None,
        'barrier.laserbeam.4': None,
        'bg.clouds': None,
        'level.segment': None,
        'level.segment.propeller': None,
        'level.border': None,
        'banner': None,
        'button.none': None,
        'button.active': None,
        'button.inactive': None,
        'highscore': None,
        'arrow.down': None,
        'arrow.up': None,
        'imagebutton.active': None,
        'imagebutton.inactive': None,
        'loader': None,
        'loader.filler': None
    }

    def __init__(self, basedir):
        """Initializes the sprite cache
        
        :param basedir: The base path
        """
        logging.debug('Initializing SpriteCache')

        self.basedir = basedir

    def get(self, key):
        """Gets the image

        :param key: The key
        """
        val = self.get(key)
        if not val:
            return None

        return val

    def get_or_load(self, key, name, path=None):
        """Gets or, if not present, loads the image

        :param key: The key
        :param name: The name
        :param path: The path
        """
        val = self.get(key)
        if not val:
            self.set(key, load_image(self.basedir, name, path))
            val = self.get(key)

        return val

    def set(self, key, value, override=False):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        :param override: Whether to force override
        """
        if override or not key in self._cache or not self.get(key):
            self._cache[key] = value

    def get(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._cache[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default
