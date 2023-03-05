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

from i18n.Translations import translate
from game.drawables.DrawableUtils import draw_text_in_rect

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
        self.font_xl = self.game_data.font_cache.get('main.xl')
        self.text_color_logo = self.game_data.game_config.get('text.color.logo')

        self.screen_mid = self.screen_size[0] / 2, self.screen_size[1] / 2
        self.curr_initial_wait = 0
        self.initial_wait = 5
        self.background = None
        self.items = []

        self.init = False
        self.init_perc = 0

        self.wh_loader = (300, 200)
        self.image_loader = pygame.transform.scale(self.game_data.sprite_cache.get('loader').convert_alpha(), self.wh_loader)
        self.loader_rect = (
                            self.screen_mid[0] - self.wh_loader[0] / 2,
                            self.screen_mid[1] - self.wh_loader[1] / 2,
                            self.wh_loader[0],
                            self.wh_loader[1]
                        )

        self.wh_loader_filler = (280, 200)
        self.images_loader_filler = []
        _raw_img = self.game_data.sprite_cache.get('loader.filler').convert_alpha()
        for i in range(0, 101):
            wh = (280 / 100 * i, 200)
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
        item_logo = MenuItem(
                                    self.game_data,
                                    self.font_xl,
                                    rect,
                                    (self.screen_mid[0], height / 2),
                                    width=width,
                                    height=height,
                                    color=self.text_color_logo,
                                    rect_width=-1,
                                    text=translate('game.name')
                                )
        self.items.append(item_logo)

    def _cache_sounds(self):
        """Caches the sounds"""
        logging.info('Caching sounds')
        self.game_data.sound_cache.load_sound('menuitem.activate', 'menuitem-activate.wav')
        self.game_data.sound_cache.load_sound('game.start', 'game-start.wav')
        self.game_data.sound_cache.load_sound('game.over', 'game-over.wav')
        self.game_data.sound_cache.load_sound('laser', 'laser.wav')
        self.game_data.sound_cache.load_sound('bump', 'bump.wav')
        self.game_data.sound_cache.load_sound('menu.back', 'menu-back.wav')
        self.game_data.sound_cache.load_sound('scroll', 'scroll.wav')

    def _cache_sprites(self):
        """Caches the sprites"""
        logging.info('Caching sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.1', 'player-idle-1.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.1', 'player-run-1.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.2', 'player-idle-2.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.2', 'player-run-2.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.3', 'player-idle-3.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.3', 'player-run-3.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.4', 'player-idle-4.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.4', 'player-run-4.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.5', 'player-idle-5.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.5', 'player-run-5.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.6', 'player-idle-6.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.6', 'player-run-6.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.7', 'player-idle-7.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.7', 'player-run-7.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.idle.8', 'player-idle-8.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('sprite.player.run.8', 'player-run-8.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.holder.left', 'barrier-holder-left.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.holder.right', 'barrier-holder-right.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.chain', 'chain.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.platform', 'barrier-platform.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.cannon', 'barrier-cannon.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.laserbeam.1', 'laser-beam-1.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.laserbeam.2', 'laser-beam-2.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.laserbeam.3', 'laser-beam-3.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('barrier.laserbeam.4', 'laser-beam-4.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('level.segment', 'segment.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('level.segment.propeller', 'propeller.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('level.border', 'border.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('level.border.out', 'border-out.png', 'sprites')
        self.game_data.sprite_cache.get_or_load('button.active', 'button-active.png', 'items')
        self.game_data.sprite_cache.get_or_load('button.inactive', 'button-inactive.png', 'items')
        self.game_data.sprite_cache.get_or_load('highscore', 'highscore.png', 'items')
        self.game_data.sprite_cache.get_or_load('arrow.down', 'arrow-down.png', 'items')
        self.game_data.sprite_cache.get_or_load('arrow.up', 'arrow-up.png', 'items')
        self.game_data.sprite_cache.get_or_load('imagebutton.active', 'imagebutton-active.png', 'items')
        self.game_data.sprite_cache.get_or_load('imagebutton.inactive', 'imagebutton-inactive.png', 'items')

    def loop(self, tick):
        dt = tick / 1000
        self.background.loop(dt)

        # Handle "global" events
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
                self._cache_sounds()
            elif self.init_perc < 50:
                self.init_perc = 50
            elif self.init_perc < 60:
                self.init_perc = 60
            elif self.init_perc < 70:
                self.init_perc = 70
            elif self.init_perc < 80:
                self.init_perc = 80
                self._cache_sprites()
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

        self.screen.blit(self.image_loader_filler, self.loader_filler_rect)
        self.screen.blit(self.image_loader, self.loader_rect)

        for item in self.items:
            item.loop()
            item.draw()
