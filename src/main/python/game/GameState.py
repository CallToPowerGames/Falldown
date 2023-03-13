#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Game State"""

import logging
from enum import Enum, unique


@unique
class State(Enum):
    """The internal state"""
    UNDEFINED = 0
    MENU = 10
    OPTIONS = 11
    HIGHSCORE = 12
    PLAYERSELECTION = 13
    GAME = 20
    PAUSE = 21
    GAMEOVER = 22
    LOADING = 30
    EXIT = 40


class GameState():
    """The Game state"""

    def __init__(self):
        """Initializes the game state"""
        logging.debug('Initializing game state')

        self.state = State.UNDEFINED
        self._state_changed = False

        self.reset_state_changed()

    def is_state_changed(self):
        """Returns whether the state changed"""
        return self._state_changed

    def reset_state_changed(self):
        """Resets the state changed state"""
        logging.debug('Resetting state change')
        self._state_changed = False

    def is_state(self, state):
        """Returns whether currently in given state

        :param state: The state
        :return: True if in given state, False else
        """
        return isinstance(state, State) and self.state == state

    def set_state(self, state):
        """Sets the state

        :param state: The state
        :return: True if the state changed happened, False else
        """
        if isinstance(state, State) and not self.is_state(state):
            logging.info('Set state "{}"'.format(state))
            logging.debug('Setting game state to {}'.format(state.name))
            self.state = state
            self._state_changed = True
            return True
        else:
            return False

    def __str__(self):
        return '{}'.format(self.state)
