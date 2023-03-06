import os
import logging
import json
from pathlib import Path

import pygame

from config.AppConfig import app_conf_get

def log_app_info():
    """Prints app info"""
    logging.info('Falldown version {} build {}, a game by {}'.format(app_conf_get('version'), app_conf_get('build'), app_conf_get('author')))

def initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        logging.info('Logging to file')
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

def update_logging(loglevel, logtofile=False):
    """Updates the logging

    :param loglevel: DEBUG, INFO, ERROR
    :param logtofile: Flag whether to log to file
    """
    logging.info('Setting log level to "{}"'.format(loglevel))
    _lvl = logging.INFO
    if loglevel == 'DEBUG':
        _lvl = logging.DEBUG
    elif loglevel == 'ERROR':
        _lvl = logging.ERROR
    logging.getLogger().setLevel(_lvl)

    if not app_conf_get('logging.log_to_file') and logtofile:
        logging.info('Logging to file')
        basedir = os.path.dirname(app_conf_get('logging.logfile'))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)
    else:
        logging.info('Not logging to file')

def get_font(name, size, system_font_name, basedir, base_path):
    """Returns the font if found. Returns the system font if not found.

    :param key: The key
    :param name: The name
    :param size: The size
    :param system_font_name: The system font name
    :param basedir: The base path
    :param base_path: The base path - for default if not found in user folder
    """
    main_font_dir = os.path.join(basedir, 'resources', 'fonts')
    try:
        font_path = os.path.join(base_path, name)
        logging.debug('Loading font "{}" from directory "{}"'.format(font_path, main_font_dir))
        font = os.path.join(main_font_dir, font_path)
        return pygame.font.Font(font, size)
    except Exception as e:
        logging.error('Could not find font, falling back to system font')
        return pygame.font.SysFont(system_font_name, size)

def load_game_conf(basedir, base_path=None):
    """
    Loads the game configuration

    :param basedir: The base path
    :param base_path: The base path - for default if not found in user folder
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.game.folder')
    file = app_conf_get('conf.game.name')

    # Try to load from user home directory
    home_dir_path = os.path.join(homedir, homefolder)
    home_file_path = os.path.join(homedir, homefolder, file)
    file_path = home_file_path
    logging.info('Trying to load game configuration from home directory {}'.format(file_path))
    load_from_home_dir = False
    if os.path.isfile(file_path):
        logging.info('Game config in user folder exists')
        load_from_home_dir = True
    ## Fallback to resources folder
    else:
        if not base_path:
            file_path = os.path.join(basedir, 'resources', file)
        else:
            file_path = os.path.join(basedir, 'resources', base_path, file)
        logging.info('Trying to load game configuration {}'.format(file_path))

    game_config = {}

    if os.path.isfile(file_path):
        logging.info('Game config exists. Loading from "{}"'.format(file_path))
        loaded = False
        try:
            with open(file_path, 'r') as jsonfile:
                game_config = json.load(jsonfile)
                loaded = True
        except Exception as ex:
            logging.error('Failed loading from "{}": {}'.format(file_path, ex))
        if not load_from_home_dir and loaded:
            logging.info('Writing game config to home directory "{}"'.format(home_file_path))
            try:
                if not os.path.exists(home_dir_path):
                    os.makedirs(home_dir_path)
                try:
                    with open(home_file_path, 'w') as jsonfile:
                        json.dump(game_config, jsonfile)
                except Exception as ex:
                    logging.error('Failed writing to "{}": {}'.format(home_file_path, ex))
            except Exception as ex:
                logging.error('Failed creating a new directory in home directory "{}"'.format(home_dir_path, ex))
    else:
        logging.info('Not loading any game config')

    return game_config

def load_highscore_db(cryptography, basedir):
    """
    Loads the highscore database

    :param cryptography: The base Cryptography
    :param basedir: The base path
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.game.folder')
    file = app_conf_get('conf.key.name')

    # Try to load from user home directory
    home_dir_path = os.path.join(homedir, homefolder)
    home_file_path = os.path.join(homedir, homefolder, file)
    file_path = home_file_path

    highscore_db = []

    logging.info('Trying to load highscore db from home directory {}'.format(file_path))
    if os.path.isfile(file_path):
        logging.info('Highscore db in user folder exists')

        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                decrypted = cryptography.decrypt(content)
                highscore_db = json.loads(decrypted)
        except Exception as ex:
            logging.error('Failed loading from "{}": {}'.format(file_path, ex))
    else:
        logging.info('Not loading any highscore db')

    return highscore_db

def save_highscore_db(cryptography, highscore_db, basedir):
    """
    Saves the highscore database

    :param cryptography: The base Cryptography
    :param basedir: The base path
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.game.folder')
    file = app_conf_get('conf.key.name')

    # Try to save to user home directory
    home_dir_path = os.path.join(homedir, homefolder)
    home_file_path = os.path.join(homedir, homefolder, file)
    file_path = home_file_path

    if os.path.isfile(file_path):
        logging.debug('Deleting old highscore db in user folder')

        try:
            os.remove(file_path)
        except Exception as ex:
            logging.error('Failed removing "{}": {}'.format(file_path, ex))

    logging.info('Saving highscore db to home directory {}'.format(file_path))
    try:
        if not os.path.exists(home_dir_path):
            os.makedirs(home_dir_path)
        try:
            with open(home_file_path, 'wb') as file:
                dump = json.dumps(highscore_db)
                encrypted = cryptography.encrypt(dump)
                file.write(encrypted)
        except Exception as ex:
            logging.error('Failed writing to "{}": {}'.format(home_file_path, ex))
    except Exception as ex:
        logging.error('Failed creating a new directory in home directory "{}"'.format(home_dir_path, ex))

def load_key(basedir, file, base_path=None):
    """
    Loads the key

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading key "{}" from directory "{}"'.format(file, file_path))
    try:
        with open(file_path, 'rb') as f:
            key = f.read()
    except pygame.error:
        raise SystemExit('Could not load key "{}": {}'.format(file_path, pygame.get_error()))
    return key

def load_image(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "{}" from directory "{}"'.format(file, file_path))
    try:
        surface = pygame.image.load(file_path)
    except pygame.error:
        raise SystemExit('Could not load image "{}": {}'.format(file_path, pygame.get_error()))
    return surface  # .convert()

def load_sound(basedir, file, base_path=None):
    """
    Loads a sound, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading sound "{}" from directory "{}"'.format(file, file_path))
    try:
        return pygame.mixer.Sound(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load sound "{}"'.format(file_path))

def load_music(basedir, file, base_path=None):
    """
    Loads a sound, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading sound "{}" from directory "{}"'.format(file, file_path))
    try:
        return pygame.mixer.music.load(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load sound "{}"'.format(file_path))
