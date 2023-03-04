#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Highscore"""

import logging
from enum import Enum, unique

import pygame

from lib.AppConfig import app_conf_get
from i18n.Translations import translate
from game.drawables.DrawableUtils import draw_text_in_rect

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.drawables.MenuItem import MenuItem

@unique
class HighscoreSceneActiveItem(Enum):
    """The active item"""
    BACK = 10


class HighscoreScene(Scene):
    """Highscore scene"""

    def __init__(self, state, fps, game):
        super().__init__(state, fps, game)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.font_cache.get('main.xl')
        self.font_l = self.game_data.font_cache.get('main.l')
        self.font_s = self.game_data.font_cache.get('main.s')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.text_color_highscore = self.game_data.game_config.get('text.color.highscore')
        self.text_color = self.game_data.game_config.get('text.color')
        self.text_color_inactive = self.game_data.game_config.get('text.color.inactive')
        self.line_width = self.game_data.game_config.get('line.width')
        self.text_color_help = self.game_data.game_config.get('text.color.help')
        self.music_volume_bg_menu_effects = self.game_data.game_config.get('music.volume.background.menu.effects')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.active_item = HighscoreSceneActiveItem.BACK
        self.background = None
        self.items = []
        self.item_back = None
        self.item_help = None
        self.highscore_db = []
        self.loaded_highscore = False

        self.wh_arrow = (64, 64)
        self.width_highscore = 600
        self.height_highscore = 230
        self.rect_highscore = (self.screen_mid[0] - self.width_highscore / 2, self.screen_mid[1] - self.height_highscore / 2 + 20, self.width_highscore, self.height_highscore)
        self.rect_arrow_down = (self.screen_mid[0] - self.width_highscore / 2 + 15, self.screen_mid[1] + self.height_highscore / 2 - 30, self.width_highscore, self.height_highscore)
        self.rect_arrow_up = (self.screen_mid[0] - self.width_highscore / 2 + 15, self.screen_mid[1] - self.height_highscore / 2 + 7, self.width_highscore, self.height_highscore)
        self.image_highscore = pygame.transform.scale(self.game_data.sprite_cache.get('highscore').convert_alpha(), (self.width_highscore, self.height_highscore))
        self.image_arrow_down = pygame.transform.scale(self.game_data.sprite_cache.get('arrow.down').convert_alpha(), self.wh_arrow)
        self.image_arrow_up = pygame.transform.scale(self.game_data.sprite_cache.get('arrow.up').convert_alpha(), self.wh_arrow)
        self.image_highscore_filled = self.image_highscore.copy()
        self.highscore_start_index = 0
        self.highscore_max_items_shown = 7

        self._init_items()

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        self.background = Background(self.game_data)

        # Logo
        width = 650
        height = 150
        rect = (self.screen_mid[0] - width / 2, 0, width, height)
        item_logo = MenuItem(
                                    self.game_data,
                                    self.font_xl,
                                    rect,
                                    (self.screen_mid[0], height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=translate('game.name'),
                                    banner=True
                                )
        self.items.append(item_logo)

        item_width = 520
        item_height = 80

        # Highscore
        width = 500
        height = 70
        rect = (self.screen_mid[0] - width / 2, 0 + height / 2, width, height)
        item_by = MenuItem(
                                self.game_data,
                                self.font_l,
                                rect,
                                (self.screen_mid[0], self.screen_size[1] / 2 - height * 2),
                                width=width,
                                height=height,
                                color=self.text_color,
                                rect_width=-1,
                                text=translate('menu.highscore.txt')
                            )
        self.items.append(item_by)

        # Back
        width = 480
        height = 65
        rect = (self.screen_mid[0] - width / 2, self.screen_mid[1] + height + 85, width, height)
        self.item_back = MenuItem(
                                    self.game_data,
                                    self.font_l,
                                    rect,
                                    (self.screen_mid[0], self.screen_mid[1] + height + height / 2 + 85),
                                    width=width,
                                    height=height,
                                    color=self.text_color,
                                    color_inactive=self.text_color_inactive,
                                    text=translate('menu.back.highscore.txt'),
                                    play_sound_on_activation=True,
                                    button=True
                                )
        self.item_back.sound_played = True
        self.items.append(self.item_back)

        # Help
        width = self.screen_size[0] - 20
        height = item_height
        rect = (self.screen_mid[0] - width / 2, self.screen_size[1] - height - 10, width, height)
        self.item_help = MenuItem(
                                    self.game_data,
                                    self.font_s,
                                    rect,
                                    (self.screen_mid[0], self.screen_size[1] - height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_help,
                                    text=translate('menu.back.highscore.help'),
                                    rotate=True,
                                    rotate_ticks_max=8,
                                    button_none=True
                                )
        self.items.append(self.item_help)

    def _reset_texts(self):
        """Resets the texts to original position"""
        self.item_back.reset_text()
        self.item_help.reset_text()

    def _reset_button_to_init(self, sound_played=False):
        """Resets the buttons to initial activation status"""
        self.item_back.active = True
        self.active_item = HighscoreSceneActiveItem.BACK
        self._reset_texts()
        self.item_help.set_text(translate('menu.back.highscore.help'))
        self.item_back.sound_played = sound_played

    def _keypress_arrow_up(self):
        if self.highscore_start_index > 0:
            self.highscore_start_index -= 1
            self.game_data.sound_cache.play('scroll', volume=self.music_volume_bg_menu_effects)
            self._draw_highscore()

    def _keypress_arrow_down(self):
        max_len = len(self.highscore_db) - self.highscore_max_items_shown
        if self.highscore_start_index < max_len:
            self.highscore_start_index += 1
            self.game_data.sound_cache.play('scroll', volume=self.music_volume_bg_menu_effects)
            self._draw_highscore()

    def _draw_highscore(self):
        """Draws the highscore"""
        self.image_highscore_filled = self.image_highscore.copy()

        width = 500
        height = 80
        curr_w = 320
        curr_h = 20
        h_plus = 32
        for i in range(self.highscore_start_index, len(self.highscore_db)):
            entry = self.highscore_db[i]
            if i >= (self.highscore_max_items_shown + self.highscore_start_index):
                break
            _str = '{:3}. {} - {}'.format(i + 1, entry['name'], entry['score']).ljust(100)
            draw_text_in_rect(self.image_highscore_filled, _str, self.text_color_highscore, self.font_s, (
                0,
                0,
                width,
                height
                ),
                (curr_w, curr_h))
            curr_h += h_plus

    def loop(self, tick):
        dt = tick / 1000

        self.background.loop(dt)

        # Handle "global" events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_state(State.MENU)
                elif event.key == pygame.K_f:
                    self.game_data.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    self._keypress_arrow_up()
                elif event.key == pygame.K_DOWN:
                    self._keypress_arrow_down()
                elif event.key == pygame.K_RETURN:
                    if self.active_item == HighscoreSceneActiveItem.BACK:
                        self._reset_button_to_init(sound_played=True)
                        self.set_state(State.MENU)
                    else:
                        self.game_data.toggle_fullscreen()

        if not self.is_state(State.HIGHSCORE):
            self.loaded_highscore = False
            self.highscore_start_index = 0
            self.game_data.sound_cache.play('menu.back', volume=self.music_volume_bg_menu_effects)
            return

        if not self.loaded_highscore:
            logging.info('Loading highscore db')
            self.highscore_db = self.game_data.highscore.load(reload=True)
            self._draw_highscore()
            self.loaded_highscore = True

    def draw(self):
        """Draws the scene"""
        self.background.draw()

        self.screen.blit(self.image_highscore_filled, self.rect_highscore)

        max_len = len(self.highscore_db) - self.highscore_max_items_shown
        if self.highscore_start_index < max_len:
            self.screen.blit(self.image_arrow_down, self.rect_arrow_down)
        if self.highscore_start_index > 0:
            self.screen.blit(self.image_arrow_up, self.rect_arrow_up)

        for item in self.items:
            item.loop()
            item.draw()
