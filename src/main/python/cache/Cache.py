#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Cache"""
import random
import logging

from cache.FontCache import FontCache
from cache.SoundCache import SoundCache
from cache.SpriteCache import SpriteCache

class Cache():
    """A cache helper"""

    def __init__(self, game_config, basedir):
        """Initializes the cache

        :param game_config: The game configuration
        :param basedir: The base directory
        """
        logging.info('Initializing cache')

        self.game_config = game_config
        self.basedir = basedir

        self.font_cache = FontCache(self.basedir)
        self.sound_cache = SoundCache(self.basedir)
        self.sprite_cache = SpriteCache(self.basedir)

        self.bg_nr = self.game_config.get('background.nr')

        self.bg_index = random.randint(0, self.bg_nr - 1)

        self.sounds = {}
        self.initial_sprites = {}
        self.sprites = {}

        self._init()

    def _init(self):
        """Initializes the file names and paths"""

        self.sounds = {
            'menuitem.activate': 'gui/menuitem-activate.wav',
            'menu.back': 'gui/menu-back.wav',
            'scroll': 'gui/scroll.wav',
            'game.start': 'game/game-start.wav',
            'game.over': 'game/game-over.wav',
            'laser': 'game/laser.wav',
            'bump': 'game/bump.wav',
            'clear.line': 'game/clear-line-segment.wav',
            'clear.all': 'game/clear-all.wav'
        }

        self.initial_sprites = {
            'app.logo': 'logo-app.png',
            'bg.clouds': 'sprites/bg/clouds.png',
            'loader': 'items/loading/loader.png',
            'loader.filler': 'items/loading/loader-filler.png',
            'banner': 'items/banner.png',
            'button.none': 'items/buttons/button-none.png',
            'bg': 'bg/bg-{}.png'.format(self.bg_index)
        }

        self.sprites = {
            'sprite.player.idle.1': 'sprites/players/player-idle-1.png',
            'sprite.player.run.1': 'sprites/players/player-run-1.png',
            'sprite.player.idle.2': 'sprites/players/player-idle-2.png',
            'sprite.player.run.2': 'sprites/players/player-run-2.png',
            'sprite.player.idle.3': 'sprites/players/player-idle-3.png',
            'sprite.player.run.3': 'sprites/players/player-run-3.png',
            'sprite.player.idle.4': 'sprites/players/player-idle-4.png',
            'sprite.player.run.4': 'sprites/players/player-run-4.png',
            'sprite.player.idle.5': 'sprites/players/player-idle-5.png',
            'sprite.player.run.5': 'sprites/players/player-run-5.png',
            'sprite.player.idle.6': 'sprites/players/player-idle-6.png',
            'sprite.player.run.6': 'sprites/players/player-run-6.png',
            'sprite.player.idle.7': 'sprites/players/player-idle-7.png',
            'sprite.player.run.7': 'sprites/players/player-run-7.png',
            'sprite.player.idle.8': 'sprites/players/player-idle-8.png',
            'sprite.player.run.8': 'sprites/players/player-run-8.png',
            'barrier.laserbeam.1': 'sprites/laser/laser-beam-1.png',
            'barrier.laserbeam.2': 'sprites/laser/laser-beam-2.png',
            'barrier.laserbeam.3': 'sprites/laser/laser-beam-3.png',
            'barrier.laserbeam.4': 'sprites/laser/laser-beam-4.png',
            'barrier.holder.left': 'sprites/barrier/barrier-holder-left.png',
            'barrier.holder.right': 'sprites/barrier/barrier-holder-right.png',
            'barrier.chain': 'sprites/barrier/chain.png',
            'level.border': 'sprites/barrier/border.png',
            'level.border.out': 'sprites/barrier/border-out.png',
            'barrier.platform': 'sprites/barrier/barrier-platform.png',
            'barrier.cannon': 'sprites/barrier/barrier-cannon.png',
            'level.segment': 'sprites/segment/segment.png',
            'level.segment.propeller': 'sprites/segment/propeller.png',
            'level.segment.clear.all': 'sprites/segment/clear-all.png',
            'level.segment.clear.line': 'sprites/segment/clear-line-segment.png',
            'button.active': 'items/buttons/button-active.png',
            'button.inactive': 'items/buttons/button-inactive.png',
            'imagebutton.active': 'items/buttons/imagebutton-active.png',
            'imagebutton.inactive': 'items/buttons/imagebutton-inactive.png',
            'highscore': 'items/highscore/highscore.png',
            'arrow.down': 'items/highscore/arrow-down.png',
            'arrow.up': 'items/highscore/arrow-up.png'
        }

    def _cache_sounds(self, sounds_dict):
        """Caches the given sounds

        :param sounds_dict: The sounds dictionary
        """
        for key, path in sounds_dict.items():
            logging.debug('Caching sound "{}": "{}"'.format(key, path))
            self.sound_cache.load_sound(key, path)

    def _cache_sprites(self, sprites_dict):
        """Caches the given sprites

        :param sprites_dict: The sprites dictionary
        """
        for key, path in sprites_dict.items():
            logging.debug('Caching sprite "{}": "{}"'.format(key, path))
            self.sprite_cache.get_or_load(key, path)

    def cache_font(self):
        """Caches the font"""
        logging.info('Caching font')
        font_sizes = self.game_config.get('font.sizes')
        name = self.game_config.get('font.main.name')
        system_font_name = self.game_config.get('font.system')
        font_path = self.game_config.get('font.main.path')
        for font_size in font_sizes:
            key = 'main.{}'.format(font_size)
            size = self.game_config.get('font.main.{}.size'.format(font_size))
            self.font_cache.get_or_load(key, name, size, system_font_name, font_path)

    def cache_sounds(self):
        """Caches the sounds"""
        logging.info('Caching sounds')
        self._cache_sounds(self.sounds)

    def cache_initial_sprites(self):
        """Caches the initial sprites"""
        logging.info('Caching initial sprites')
        self._cache_sprites(self.initial_sprites)

    def cache_sprites(self):
        """Caches the sprites"""
        logging.info('Caching sprites')
        self._cache_sprites(self.sprites)
