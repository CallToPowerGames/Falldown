#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

"""FontCache"""

class FontCache():
    """FontCache"""

    _cache = {
        'main.xs': None,
        'main.s': None,
        'main.l': None,
        'main.xl': None
    }

    def __init__(self):
        """Initializes the sprite cache"""
        logging.debug('Initializing FontCache')

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
