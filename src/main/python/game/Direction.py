#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Direction"""

import logging
from enum import Enum, unique


@unique
class Direction(Enum):
    """The direction"""
    LEFT = 0
    RIGHT = 10
