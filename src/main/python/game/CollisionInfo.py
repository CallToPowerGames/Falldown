#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""CollisionInfo"""

import logging
import random

class CollisionInfo():
    """The collision information
    
    <CollidesBottom>
    <CollidesLeft>
    <CollidesRight>
    <SegmentTopY>
    <StandsOnMovingSegment>
    <SegmentSpeed>
    <CollidesWithClearLine>
    <CollidesWithClearAll>
    <IndexLineColliding>
    <IndexSegmentColliding>
    """

    def __init__(self):
        """Initializes the collision information"""
        self.collides_bottom = False
        self.collides_left = False
        self.collides_right = False
        self.segment_top_y = 0
        self.stands_on_moving_segment = False
        self.segment_speed = 0
        self.collides_clear_linesegment = False
        self.collides_clear_all = False
        self.index_line_colliding = -1
        self.index_segment_colliding = -1
