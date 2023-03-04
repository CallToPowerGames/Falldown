#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""GameData"""

import logging
from threading import Timer
import pygame

from game.GameState import GameState, State
from game.scenes.LoadingScene import LoadingScene
from game.scenes.MenuScene import MenuScene
from game.scenes.HighscoreScene import HighscoreScene
from game.scenes.OptionsScene import OptionsScene
from game.scenes.PlayerSelectionScene import PlayerSelectionScene
from game.scenes.GameScene import GameScene
from game.scenes.PauseScene import PauseScene
from game.scenes.GameOverScene import GameOverScene
from game.scenes.ExitScene import ExitScene

class GameData():
    """Game data"""

    def __init__(self, game_config, highscore, font_cache, sound_cache, sprite_cache):
        """Initializes the Game data

        :param game_config: The game config
        :param highscore: The highscore
        :param font_cache: The font cache
        :param sound_cache: The sound cache
        :param sprite_cache: The sprite cache
        """
        logging.info('Initializing game data')

        self.game_config = game_config
        self.highscore = highscore
        self.font_cache = font_cache
        self.sound_cache = sound_cache
        self.sprite_cache = sprite_cache

        self.game_state = GameState()
        self.looping = False
        self.fullscreen = False
        self.exiting = False
        self.scenes = {}
        self.scene_loading = None
        self.scene_menu = None
        self.scene_highscore = None
        self.scene_options = None
        self.scene_playerselection = None
        self.scene_game = None
        self.scene_pause = None
        self.scene_gameover = None
        self.timer_exit = None

        self.players = []
        self.player_index = 0
        self.score = 0
        self.fps = 0

    def init_loading_scene(self):
        """Initializes the scenes"""
        logging.debug('Initializing loading scene')

        self.scene_loading = LoadingScene(State.LOADING, self.game_config.get('fps.loading'), self)
        self.scene_exit = ExitScene(State.EXIT, self.game_config.get('fps.exit'), self)

        self.scenes[State.LOADING] = self.scene_loading
        self.scenes[State.EXIT] = self.scene_exit

    def init_scenes(self):
        """Initializes the scenes"""
        logging.debug('Initializing scenes')

        self.scene_menu = MenuScene(State.MENU, self.game_config.get('fps.menu'), self)
        self.scene_highscore = HighscoreScene(State.HIGHSCORE, self.game_config.get('fps.highscore'), self)
        self.scene_options = OptionsScene(State.OPTIONS, self.game_config.get('fps.options'), self)
        self.scene_playerselection = PlayerSelectionScene(State.PLAYERSELECTION, self.game_config.get('fps.playerselection'), self)
        self.scene_game = GameScene(State.GAME, self.game_config.get('fps.game'), self)
        self.scene_pause = PauseScene(State.PAUSE, self.game_config.get('fps.pause'), self)
        self.scene_gameover = GameOverScene(State.GAMEOVER, self.game_config.get('fps.gameover'), self)

        self.scenes[State.MENU] = self.scene_menu
        self.scenes[State.HIGHSCORE] = self.scene_highscore
        self.scenes[State.OPTIONS] = self.scene_options
        self.scenes[State.PLAYERSELECTION] = self.scene_playerselection
        self.scenes[State.GAME] = self.scene_game
        self.scenes[State.PAUSE] = self.scene_pause
        self.scenes[State.GAMEOVER] = self.scene_gameover

    def toggle_fullscreen(self):
        """Toggles between fullscreen modes"""
        screen_backup = self.game_config.get('screen').copy()

        if not self.fullscreen:
            logging.debug("Changing to fullscreen mode")
            self._set_screen(pygame.display.set_mode(self.game_config.get('screen.size'), self.game_config.get('winstyle') | pygame.FULLSCREEN))
        else:
            logging.debug("Changing to windowed mode")
            self._set_screen(pygame.display.set_mode(self.game_config.get('screen.size'), self.game_config.get('winstyle')))

        self.game_config.get('screen').blit(screen_backup, (0, 0))
        pygame.display.update()
        self.fullscreen = not self.fullscreen

    def _set_screen(self, screen):
        """Sets the screen

        :param screen: The screen
        """
        self.screen = screen
        self.game_config.set('screen', screen)

    def check_reset_game(self):
        """Checks whether to reset game"""
        if self.game_state.is_state_changed():
            self.reset_game()
            self.game_state.reset_state_changed()

    def reset_game(self):
        """Resets the game"""
        logging.debug('Reset game')
        self.scene_game.reset()

    def get_scene(self, state):
        """Returns the scene for the given state

        :param state: The state
        :return: The scene for the state
        """
        if state in self.scenes:
            return self.scenes[state]

        logging.error('No scene found for state "{}"'.format(self.game_state))
        return None

    def exit(self):
        """Starts exitting, not stopping the loop"""
        logging.info('Quitting to exit screen')
        self.game_state.set_state(State.EXIT)
        try:
            if self.timer_exit:
                self.timer_exit.cancel()
                self.timer_exit.stop()
        except:
            pass

        self.timer_exit = Timer(self.game_config.get('exit.timer1'), self._exit_stop_loop).start()

    def _exit_stop_loop(self):
        """Exits, stops the loop"""
        if not self.looping:
            return

        logging.debug('Stopping loop')
        self.looping = False
        try:
            if self.timer_exit:
                self.timer_exit.cancel()
                self.timer_exit.stop()
        except:
            pass

        self.timer_exit = Timer(self.game_config.get('exit.timer1'), self._exit_full).start()

    def _exit_full(self):
        """Exits, sets flag to full quit"""
        if self.exiting:
            return

        logging.debug('Ready to quit')
        self.looping = False
        self.exiting = True
        try:
            if self.timer_exit:
                self.timer_exit.cancel()
                self.timer_exit.stop()
        except:
            pass
