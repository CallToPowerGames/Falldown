#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Spritesheet"""

import logging

import pygame

class Spritesheet(object):
    """A Spritesheet"""

    def __init__(self, sprite_cache, name, size, nr_images, scale_size=None, startpoint=(0, 0), generate_sides=True, orientation_left=True, colorkey=(0, 0, 0), smooth=False):
        """Initializes the Spritesheet

        :param sprite_cache: The sprite cache
        :param name: The sprite key name(s), can be a list of names or a single name
        :param size: The size
        :param nr_images: The number of images
        :param scale_size: Size to scale to. Leave blank for given size
        :param startpoint: The start point
        :param generate_sides: Flag whether to generate both sides (normal and flipped)
        :param orientation_left: Flag whether to the sprite is left-oriented
        :param colorkey: The color key
        :param smooth: Flag whether to use smoothscale instead of scale
        """
        super().__init__()

        logging.debug('Initializing Spritesheet')

        self.sprite_cache = sprite_cache
        self.name = [name] if type(name) != list else name
        self.size = size
        self.nr_images = nr_images
        self.scale_size = scale_size if scale_size else self.size
        self.startpoint = startpoint
        self.generate_sides = generate_sides
        self.orientation_left = orientation_left
        self.colorkey = colorkey
        self.smooth = smooth

        self.images_left = []
        self.images_right = []

        self.sheet = [self.sprite_cache.get(n) for n in self.name]

        self._init()

    def _init(self):
        """Initializes the spritesheet"""
        coordinates = []
        curr_w = self.startpoint[0]
        curr_h = self.startpoint[1]
        for i in range(0, self.nr_images):
            coordinates.append((curr_w, curr_h, self.size[0], self.size[1]))
            curr_w += self.size[0]

        imgs = self._images_at(coordinates)
        _func = pygame.transform.scale if self.smooth else pygame.transform.smoothscale
        if self.orientation_left:
            self.images_left = [_func(img.convert_alpha(), self.scale_size) for img in imgs]
            if self.generate_sides:
                self.images_right = [pygame.transform.flip(img, True, False) for img in self.images_left]
        else:
            self.images_right = [_func(img.convert_alpha(), self.scale_size) for img in imgs]
            if self.generate_sides:
                self.images_left = [pygame.transform.flip(img, True, False) for img in self.images_right]

    def scale_to(self, scale_size):
        """Scales to a given size

        :param scale_size: The scale size
        """
        self.scale_size = scale_size
        self.images_left = [pygame.transform.scale(img, self.scale_size) for img in self.images_left]
        self.images_right = [pygame.transform.scale(img, self.scale_size) for img in self.images_right]

    def get_scaled_left(self, scale_size):
        """Returns left images scaled to a given size

        :param scale_size: The scale size
        """
        return [pygame.transform.scale(img, scale_size) for img in self.images_left]

    def get_scaled_right(self, scale_size):
        """Returns left images scaled to a given size

        :param scale_size: The scale size
        """
        return [pygame.transform.scale(img, scale_size) for img in self.images_right]

    def _image_at(self, sheet, rectangle):
        """Loads and image of the sheet

        :param sheet: The sheet
        :param rectangle: The rectangle
        :return: Image
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(sheet, (0, 0), rect)
        if self.colorkey is not None:
            self.colorkey = image.get_at((0, 0))
            image.set_colorkey(self.colorkey, pygame.RLEACCEL)
        return image

    def _images_at(self, rects):
        """Loads multiple images via _image_at

        :param rects: The rectangles
        :return: List of images
        """
        images = []
        for sheet in self.sheet:
            images += [self._image_at(sheet, rect) for rect in rects]
        return images
