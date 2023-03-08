#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Scene - Loading"""

import logging

import pygame

from game.scenes.Scene import Scene
from game.GameState import State
from game.sprites.Background import Background
from game.drawables.MenuItem import MenuItem

class LoadingScene(Scene):
    """Loading scene"""

    def __init__(self, state, fps, game_data):
        super().__init__(state, fps, game_data)

        self.screen = self.game_data.game_config.get('screen')
        self.screen_size = self.game_data.game_config.get('screen.size')
        self.font_xl = self.game_data.cache.font_cache.get('main.xl')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')
        self.load_filler_bg_color = self.game_data.game_config.get('background.load.filler.color')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.curr_initial_wait = 0
        self.initial_wait = 10
        self.background = None
        self.item_logo = None
        self.init = False
        self.init_perc = 0
        self.load_filler_bg_height = 20
        self.wh_loader = (300, 200)
        self.image_loader = pygame.transform.scale(self.game_data.cache.sprite_cache.get('loader').convert_alpha(), self.wh_loader)
        self.loader_rect = (
                            self.screen_mid[0] - self.wh_loader[0] / 2,
                            self.screen_mid[1] - self.wh_loader[1] / 2,
                            self.wh_loader[0],
                            self.wh_loader[1]
                        )
        self.wh_loader_filler = (280, 200)
        self.images_loader_filler = []
        _raw_img = self.game_data.cache.sprite_cache.get('loader.filler').convert_alpha()
        for i in range(0, 101):
            wh = (self.wh_loader_filler[0] / 100 * i, self.wh_loader_filler[1])
            img = pygame.transform.scale(_raw_img, wh)
            self.images_loader_filler.append(img)

        self.set_percentage(self.init_perc)
        self._init_items()

    def set_percentage(self, p):
        """Sets the loading percentage, 0-100

        :param p: Percentage, 0-100
        """
        if p < 0:
            self.image_loader_filler = self.images_loader_filler[0]
        elif p > 100:
            self.image_loader_filler = self.images_loader_filler[100]
        else:
            self.image_loader_filler = self.images_loader_filler[p]
        self.loader_filler_rect = (
            self.screen_mid[0] - self.wh_loader_filler[0] / 2,
            self.screen_mid[1] - self.wh_loader_filler[1] / 2,
            self.wh_loader_filler[0] / 5,
            self.wh_loader_filler[1]
        )

    def _init_items(self):
        """Initializes the items"""
        logging.debug('Initializing items')

        self.background = Background(self.game_data)

        # Logo
        width = 650
        height = 150
        rect = (self.screen_mid[0] - width / 2, 0, width, height)
        self.item_logo = MenuItem(
                                    self.game_data,
                                    self.font_xl,
                                    rect,
                                    (self.screen_mid[0], height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=self.game_data.i18n.get('game.name')
                                )
        self.items.append(self.item_logo)

    def reload_i18n_texts(self):
        """Reloads the i18n texts"""
        self.item_logo.set_text(self.game_data.i18n.get('game.name'))

    def loop(self, tick):
        dt = tick / 1000
        self.background.loop(dt)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()

        if not self.is_state(State.LOADING):
            return

        # Simulate a cool feeling of loading. And load some stuff in between
        if self.curr_initial_wait >= self.initial_wait and not self.init:
            if self.init_perc < 10:
                self.init_perc = 10
            elif self.init_perc < 20:
                self.init_perc = 20
            elif self.init_perc < 30:
                self.init_perc = 30
            elif self.init_perc < 40:
                self.init_perc = 40
                self.game_data.cache.cache_sounds()
            elif self.init_perc < 50:
                self.init_perc = 50
            elif self.init_perc < 60:
                self.init_perc = 60
            elif self.init_perc < 70:
                self.init_perc = 70
            elif self.init_perc < 80:
                self.init_perc = 80
                self.game_data.cache.cache_sprites()
            elif self.init_perc < 90:
                self.init_perc = 90
            elif self.init_perc < 100:
                self.init_perc = 100
                self.game_data.init_scenes()
            else:
                self.init = True
            self.set_percentage(self.init_perc)
        else:
            self.curr_initial_wait += 1

    def draw(self):
        self.background.draw()

        pygame.draw.rect(
            self.screen,
            self.load_filler_bg_color,
            (
                self.screen_mid[0] - self.wh_loader_filler[0] / 2,
                self.screen_mid[1] - (self.load_filler_bg_height / 2),
                self.wh_loader_filler[0],
                self.load_filler_bg_height
            )
        )
        self.screen.blit(self.image_loader_filler, self.loader_filler_rect)
        self.screen.blit(self.image_loader, self.loader_rect)

        for item in self.items:
            item.loop()
            item.draw()
