#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Game"""

import logging
import sys
import pygame

from i18n.Translations import translate
from game.GameState import State


class Game():
    """Main Game"""

    def __init__(self, game_data):
        """Initializes the Game

        :param game_data: The game data
        """
        logging.info('Initializing game')

        self.game_data = game_data

        self.clock = None

        self._init()
        self._set_allowed_events()

    def _init(self):
        """Initializes"""
        logging.debug('Initializing')
        self.game_data.game_state.set_state(State.LOADING)

        self._init_library()

        pygame.display.set_caption(translate('game.name'))
        img_icon = self.game_data.cache.sprite_cache.get('app.logo').convert()
        icon = pygame.transform.scale(img_icon, self.game_data.game_config.get('app.icon.size'))
        pygame.display.set_icon(icon)

        pygame.mouse.set_visible(0)

    def _set_allowed_events(self):
        """Allowes only certain events"""
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    def _init_library(self):
        """Initializes library"""
        logging.debug('Initializing library')
        self.clock = pygame.time.Clock()
        size = self.game_data.game_config.get('screen.size')
        winstyle = 0
        self.game_data.game_config.set('winstyle', winstyle)
        self.game_data.game_config.set('screen', pygame.display.set_mode(size, winstyle | pygame.DOUBLEBUF))

        self.game_data.init_loading_scene()

    def loop(self):
        """Main loop"""
        if self.game_data.looping:
            logging.debug('Game loop already started, not looping')
            return

        pygame.display.update()

        logging.debug('Starting the main loop')
        self.game_data.looping = True

        while self.game_data.looping:
            scene = self.game_data.get_scene(self.game_data.game_state.state)
            if scene:
                tick = self.clock.tick(scene.fps)
                self.game_data.fps = self.clock.get_fps()
                pygame.display.update()
                scene.loop(tick)
                scene.draw()
            else:
                logging.error('Unknown state: {}'.format(self.game_data.game_state))
                self.game_data.exit()

            if self.game_data.game_state.state == State.LOADING and scene.init:
                self.game_data.game_state.set_state(State.MENU)

        logging.debug('Waiting to quit')
        while not self.game_data.exiting:
            scene = self.game_data.get_scene(self.game_data.game_state.state)
            if scene:
                pygame.display.update()
                tick = self.clock.tick(scene.fps)
            else:
                logging.error('Unknown state: {}'.format(self.game_data.game_state))
                self.game_data.exit()

        try:
            logging.info('Quitting modules')
            pygame.font.quit()
            pygame.mixer.quit()

            logging.info('Quitting')
            pygame.quit()
        except Exception as e:
            logging.error(e)

        return sys.exit(0)
