#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""AppConfig"""

import logging
import time
from pathlib import Path
import tempfile

_app_config = {
    'author': 'Denis Meyer',
    'version': '1.4',
    'build': '2023-03-12-1',
    'copyright': '© 2023 Denis Meyer',
    'conf.game.folder': 'falldown',
    'conf.game.name': 'conf.json',
    'conf.key.name': 'highscore.db',
    'conf.highscore.key.file': 'fernet.key',
    'img_logo_app': None,
    'logging.log_to_file': False,
    'logging.loglevel': logging.INFO,
    'logging.format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
    'logging.datefmt': '%d-%m-%Y %H:%M:%S',
    'logging.logfile': str(Path.home()) + '/falldown/logs/application-' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.log'
}

def app_conf_set(key, value):
    """Sets the value for the given key

    :param key: The key
    :param value: The value
    """
    _app_config[key] = value

def app_conf_get(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key
    :param default: The default if no value could be found for the key
    """
    try:
        return _app_config[key]
    except KeyError as exception:
        logging.error(
            'Returning default for key "{}": "{}"'.format(key, exception))
        return default
