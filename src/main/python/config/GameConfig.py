#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""GameConfig"""

import logging

from lib.Utils import load_game_conf, write_game_conf
import game.Colors as Colors

class GameConfig():
    """Game configuration"""

    _config = {
        # In the public config
        'config.version': 3, # if user folder conf.json is < this version, it gets overwritten
        'languages.main': 'en',
        'logging.level': 'INFO',
        'logging.logtofile': False,
        'debug.show': False,
        'debug.barrier.start': True,
        'fps.show': False,
        'font.main.xs.size': 12,
        'font.main.s.size': 25,
        'font.main.m.size': 40,
        'font.main.l.size': 50,
        'font.main.xl.size': 75,
        'fps.loading': 30,
        'fps.menu': 30,
        'fps.highscore': 30,
        'fps.options': 30,
        'fps.pause': 30,
        'fps.gameover': 30,
        'fps.playerselection': 30,
        'fps.game': 60,
        'fps.ai': 60,
        'fps.exit': 30,
        'barrier.start.after.lines': 10,
        'score.plus': 1,
        'score.plus.clear.linesegment': 2,
        'score.plus.clear.all': 4,
        'highscore.entries.max': 100,
        'ai.timer': 15.0,
        'exit.timer1': 2.0,
        'exit.timer2': 0.2,
        'offset.max.up': 0,
        'offset.max.left': -1000,
        'offset.max.right': 1000,
        'music.volume.background.menu': 1.0, # 0.0-1.0
        'music.volume.background.menu.effects': 1.0, # 0.0-1.0
        'music.volume.background.game': 1.0, # 0.0-1.0
        'music.volume.background.game.barriervisible': 0.3, # 0.0-1.0
        'music.volume.background.game.effects': 1.0, # 0.0-1.0
        'background.draw': True,
        'background.number.bg.clouds.big': 70,
        'background.number.bg.clouds.mid': 80,
        'background.number.bg.clouds.small': 90,
        'background.speed.bg.clouds.big.min': 40,
        'background.speed.bg.clouds.big.max': 70,
        'background.speed.bg.clouds.mid.min': 20,
        'background.speed.bg.clouds.mid.max': 35,
        'background.speed.bg.clouds.small.min': 10,
        'background.speed.bg.clouds.small.max': 15,
        'camera.borders': { # Read: "Pixels from [...]"
            'left': 150,
            'right': 150,
            'top': 50,
            'bottom': 240
        },
        'level.generator.modifier': 1.4,
        'level.line.moving.probability': 15, # in percent
        'level.line.clear.linesegment.probability': 10, # in percent
        'level.line.clear.all.probability': 3, # in percent
        'level.segments.width.min': 50,
        'level.segments.width.max': 500,
        'level.segments.height': 22,
        'level.segments.gap.min': 50,
        'level.segments.gap.add.max': 100,
        'level.segments.gap.vert.min': 50,
        'level.segments.gap.vert.add.max': 60,
        'level.segments.move.speed': 5,
        'level.segments.move.max': 200,
        'level.segment.moving.decrease.factor': 2,
        'level.iterations.showgo': 80,
        'barrier.speed': 130,
        'barrier.speed.increase': 1,
        'player.barrier.move.correction': 30,
        'player.speed.start.1': [0, 80],
        'player.speed.max.1': [550, 700],
        'player.speed.increase.1': [20, 5],
        'player.speed.decrease.1': 25,
        'player.speed.fallingfactor.increase.1': 0.8,
        'player.speed.start.2': [20, 80],
        'player.speed.max.2': [550, 800],
        'player.speed.increase.2': [20, 5],
        'player.speed.decrease.2': 30,
        'player.speed.fallingfactor.increase.2': 0.8,
        'player.speed.start.3': [10, 40],
        'player.speed.max.3': [550, 600],
        'player.speed.increase.3': [20, 5],
        'player.speed.decrease.3': 30,
        'player.speed.fallingfactor.increase.3': 0.8,
        'player.speed.start.4': [60, 40],
        'player.speed.max.4': [650, 600],
        'player.speed.increase.4': [20, 5],
        'player.speed.decrease.4': 20,
        'player.speed.fallingfactor.increase.4': 0.7,
        'player.speed.start.5': [40, 10],
        'player.speed.max.5': [750, 450],
        'player.speed.increase.5': [30, 5],
        'player.speed.decrease.5': 20,
        'player.speed.fallingfactor.increase.5': 0.8,
        'player.speed.start.6': [50, 80],
        'player.speed.max.6': [650, 800],
        'player.speed.increase.6': [20, 5],
        'player.speed.decrease.6': 30,
        'player.speed.fallingfactor.increase.6': 0.4,
        'player.speed.start.7': [0, 80],
        'player.speed.max.7': [900, 900],
        'player.speed.increase.7': [10, 10],
        'player.speed.decrease.7': 35,
        'player.speed.fallingfactor.increase.7': 0.9,
        'player.speed.start.8': [0, 80],
        'player.speed.max.8': [450, 900],
        'player.speed.increase.8': [10, 5],
        'player.speed.decrease.8': 50,
        'player.speed.fallingfactor.increase.8': 0.9,
        # Not in the public config
        'debug.config.ignore': False,
        'screen.size': (800, 600),
        'winstyle': 0,
        'menu.music': ['bg/bg-0.wav', 'bg/bg-1.wav'],
        'game.music': ['game/game-0.wav', 'game/game-1.wav', 'game/game-2.wav', 'game/game-3.wav'],
        'font.sizes': ['xs', 's', 'm', 'l', 'xl'],
        'font.system': 'freesanbold.ttf',
        'font.main.path': 'yoster-island',
        'font.main.name': 'yoster.ttf',
        'app.icon.size': (32, 32),
        'level.offset.max': 10000000,
        'level.border.img.size': (64, 128),
        'level.border.out.img.size': (8, 85),
        'level.collision.detection.correction.left': 2,
        'level.collision.detection.correction.right': 2,
        'level.collision.detection.correction.bottom': 8,
        'level.collision.detection.correction.top': 5,
        'background.startpoint.bg.clouds.big': (0, 208),
        'background.size.bg.clouds.big': (115, 32),
        'background.startpoint.bg.clouds.mid': (272, 215),
        'background.size.bg.clouds.mid': (36, 16),
        'background.startpoint.bg.clouds.small': (176, 218),
        'background.size.bg.clouds.small': (25, 13),
        'background.nr': 4,
        'background.size': (512, 512),
        'background.startpoint': (0, 0),
        'background.scale.factor.max.small': 2.5,
        'background.scale.factor.max.mid': 2.5,
        'background.scale.factor.max.big': 2.5,
        'background.offset.factor.x.bg.image': 1,
        'background.offset.factor.x.small': 1,
        'background.offset.factor.x.mid': 1,
        'background.offset.factor.x.big': 1,
        'background.offset.factor.y.bg.image': 5 / 10,
        'background.offset.factor.y.small': 6 / 10,
        'background.offset.factor.y.mid': 7 / 10,
        'background.offset.factor.y.big': 8 / 10,
        'border.chain.size': (8, 8),
        'barrier.platform.size': (32, 8),
        'barrier.cannon.size': (39, 25),
        'barrier.cannon.left.correction': (0, -1),
        'barrier.cannon.right.correction': (-5, -1),
        'barrier.laser.correction': (3, 2),
        'barrier.laserbeam.size': (20, 9),
        'barrier.holder.left.size': (36, 30),
        'barrier.holder.right.size': (36, 30),
        'player.stuck.correction': 2,
        'player.stuck.threshold': 5,
        'player.nr': 8, # If number is changed, check logic in PlayerSelectionScene!
        'player.orientationleft.1': True,
        'player.nrimages.idle.1': 14,
        'player.nrimages.run.1': 14,
        'player.size.1': (38, 34),
        'player.rect.inner.1': (3, 4),
        'player.orientationleft.2': False,
        'player.nrimages.idle.2': 11,
        'player.nrimages.run.2': 12,
        'player.size.2': (32, 32),
        'player.rect.inner.2': (8, 4),
        'player.orientationleft.3': False,
        'player.nrimages.idle.3': 11,
        'player.nrimages.run.3': 12,
        'player.size.3': (32, 32),
        'player.rect.inner.3': (8, 4),
        'player.orientationleft.4': True,
        'player.nrimages.idle.4': 8,
        'player.nrimages.run.4': 12,
        'player.size.4': (34, 44),
        'player.rect.inner.4': (8, 4),
        'player.orientationleft.5': True,
        'player.nrimages.idle.5': 13,
        'player.nrimages.run.5': 14,
        'player.size.5': (32, 34),
        'player.rect.inner.5': (8, 4),
        'player.orientationleft.6': True,
        'player.nrimages.idle.6': 14,
        'player.nrimages.run.6': 16,
        'player.size.6': (32, 32),
        'player.rect.inner.6': (8, 4),
        'player.orientationleft.7': True,
        'player.nrimages.idle.7': 11,
        'player.nrimages.run.7': 6,
        'player.size.7': (52, 34),
        'player.rect.inner.7': (8, 4),
        'player.orientationleft.8': True,
        'player.nrimages.idle.8': 15,
        'player.nrimages.run.8': 10,
        'player.size.8': (38, 24),
        'player.rect.inner.8': (3, 4),
        'level.segment.img.left.startpoint': (51, 0),
        'level.segment.img.left.size': (8, 10),
        'level.segment.img.mid.startpoint': (59, 0),
        'level.segment.img.mid.size': (8, 10),
        'level.segment.img.right.startpoint': (67, 0),
        'level.segment.img.right.size': (8, 10),
        'level.segment.img.propeller.startpoint': (0, 0),
        'level.segment.img.propeller.size': (32, 5),
        'level.segment.img.clear.linesegment.startpoint': (0, 0),
        'level.segment.img.clear.linesegment.size': (60, 40),
        'level.segment.img.clear.all.startpoint': (0, 0),
        'level.segment.img.clear.all.size': (14, 46),
        'background.main.color': Colors.BLUE_DEEPSKY,
        'background.load.filler.color': Colors.GREY_LIGHT,
        'text.color': Colors.BLUE_COBALT,
        'text.color.highscore': Colors.BLACK,
        'text.color.inactive': Colors.GREY,
        'text.color.help': Colors.GREY,
        'text.color.logo': Colors.RED_BURGUNDY,
        'text.color.score': Colors.RED_BURGUNDY,
        'text.color.go': Colors.RED_BURGUNDY,
        'text.color.ai_text': Colors.RED_BURGUNDY,
        'border.color': Colors.BLACK,
        'fps.text.color': Colors.BLUE_COBALT,
        'screen': None
    }

    def __init__(self, basedir):
        """Initializes the game config

        :param basedir: The base path
        """
        logging.debug('Initializing GameConfig')

        self.basedir = basedir

        self.debug_config_ignore = self._config['debug.config.ignore']

        self._init()

    def _init(self):
        """Initializes the game config"""
        if self.debug_config_ignore:
            logging.info('Ignoring loading external config')
            return

        config = load_game_conf(self.basedir, self.get('config.version', 1))
        for key, val in config.items():
            if key in self._config:
                logging.debug('Overwriting: {}: {}'.format(key, val))
                self.set(key, val)
            else:
                logging.warn('Key-Value pair not found: {}, {}'.format(key, val))

    def save_game_conf(self):
        """Writes the game config"""
        logging.info('Saving game config')
        dict_overwrites = {
            'background.draw': self.get('background.draw'),
            'languages.main': self.get('languages.main')
        }
        write_game_conf(self.basedir, dict_overwrites)

    def set(self, key, value):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        """
        self._config[key] = value

    def get(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._config[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default
