#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Main"""

import sys
import os
import logging
import urllib.request
import json

from lib.AppConfig import app_conf_get
from lib.GameConfig import GameConfig
from lib.AppContext import AppContext
from game.Game import Game


def _initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        basedir = os.path.dirname(app_conf_get('logging.logfile'))

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logging.basicConfig(level=app_conf_get('logging.loglevel'),
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(app_conf_get('logging.loglevel'))
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)


if __name__ == '__main__':
    print('Current working directory: {}'.format(os.getcwd()))

    _initialize_logger()

    basedir = os.path.dirname(__file__)

    logging.info('Falldown version {} build {}, a game by {}'.format(app_conf_get('version'), app_conf_get('build'), app_conf_get('author')))
    appctxt = AppContext(basedir)
    exit_code = appctxt.run()
    sys.exit(exit_code)
