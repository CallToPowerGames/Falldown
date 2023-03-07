#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

import pygame

from lib.Utils import load_sound, load_music

"""SoundCache"""

class SoundCache():
    """SoundCache"""

    _cache = {
        'menuitem.activate': None,
        'game.start': None,
        'game.over': None,
        'laser': None,
        'bump': None,
        'menu.back': None,
        'scroll': None
    }

    def __init__(self, basedir):
        """Initializes

        :param basedir: The base path
        """
        logging.debug('Initializing SoundCache')
        
        self.basedir = basedir

    # Sounds

    def load_sound(self, key, path):
        """Loads the sound into the cache

        :param key: Sound key
        :param path: Sound path + name
        """
        val = self.get_sound(key)
        if not val:
            self.set_sound(key, load_sound(self.basedir, path))
            val = self.get_sound(key)

    def play(self, key, loops=0, volume=1.0):
        """Plays the sound

        :param key: Sound to play
        :param loops: Number of loops
        """
        val = self.get_sound(key)
        if val:
            val.set_volume(volume)
            val.play(loops=loops)

    def stop(self, key):
        """Stops the sound

        :param sound: Sound to play
        """
        val = self.get_sound(key)
        if val:
            val.stop()

    def get_sound(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._cache[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default

    def set_sound(self, key, value, override=False):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        :param override: Whether to force override
        """
        if override or not key in self._cache or not self.get_sound(key):
            self._cache[key] = value

    # Music (streaming)

    def load_music(self, path):
        """Loads the music

        :param path: Music path + name
        """
        load_music(self.basedir, path)

    def set_music_volume(self, volume=1.0):
        """Sets the volume

        :param volume: The volume (0.0-1.0)
        """
        pygame.mixer.music.set_volume(volume)

    def play_music(self, loops=0, volume=1.0):
        """Plays the music. Music has to be loaded at this time

        :param loops: Number of loops, -1 for endless looping
        :param volume: The volume (0.0-1.0)
        """
        self.set_music_volume(volume)
        pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        """Stops the music"""
        pygame.mixer.music.stop()
