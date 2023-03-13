#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

import logging

"""Scene"""

class Scene():
    """Scene"""

    def __init__(self, state, fps, game_data):
        """Initializes the scene

        :param state: The state that can be handled
        :param fps: The state fps
        :param game_data: The game data
        """
        self.state = state
        self.fps = fps
        self.game_data = game_data

        self.items = []
        self.init = False

    def exit(self):
        """Exits the game"""
        logging.debug('Exit')
        self.game_data.exit()

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        pass

    def reset_texts(self):
        """Resets the texts to original position"""
        for item in self.items:
            item.reset_text()

    def set_state(self, state):
        """Sets the state

        :param state: The state
        """
        self.game_data.game_state.set_state(state)

    def is_state(self, state):
        """Checks whether is in a given state

        :param state: The state to check
        :return: True if game is in given state, False else
        """
        return self.game_data.game_state.is_state(state)

    def can_handle_state(self, state):
        """Checks whether the scene can handle the given state

        :param state: The state
        :return: True if the scene can handle the given state, False else
        """
        return self.state == state

    def loop(self, tick):
        """Loops the scene

        :param tick: Ticks
        """
        pass

    def draw(self):
        """Draws the scene"""
        pass
