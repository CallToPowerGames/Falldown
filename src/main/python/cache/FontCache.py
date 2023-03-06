#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

from lib.Utils import get_font

"""FontCache"""

class FontCache():
    """FontCache"""

    _cache = {
        'main.xs': None,
        'main.s': None,
        'main.l': None,
        'main.xl': None
    }

    def __init__(self, basedir):
        """Initializes the sprite cache

        :param basedir: The base path
        """
        logging.debug('Initializing FontCache')
        
        self.basedir = basedir

    def get_or_load(self, key, name, size, system_font_name, path=None):
        """Gets or, if not present, loads the font

        :param key: The key
        :param name: The name
        :param size: The size
        :param system_font_name: The system font name
        :param path: The path
        """
        val = self.get(key)
        if not val:
            self.set(key, get_font(name, size, system_font_name, self.basedir, path))
            val = self.get(key)

        return val

    def set(self, key, value, override=False):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        :param override: Whether to force override
        """
        if override or not key in self._cache or not self._cache[key]:
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
