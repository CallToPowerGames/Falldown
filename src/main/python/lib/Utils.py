import os
import logging
import json
from pathlib import Path

import pygame

from config.AppConfig import app_conf_get

def log_app_info():
    """Prints app info"""
    logging.info('====================================================================')
    logging.info('|| Falldown version {} build {}, a game by {} ||'.format(app_conf_get('version'), app_conf_get('build'), app_conf_get('author')))
    logging.info('====================================================================')

def initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        logging.info('Logging to file')
        basedir = os.path.dirname(app_conf_get('logging.logfile'))
        try:
            if not os.path.exists(basedir):
                os.makedirs(basedir)
        except Exception as ex:
            logging.error('Failed creating a new directory "{}": {}'.format(basedir, ex))

    logging.basicConfig(level=app_conf_get('logging.loglevel'),
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding='utf-8', delay=False)
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
        try:
            if not os.path.exists(basedir):
                os.makedirs(basedir)
        except Exception as ex:
            logging.error('Failed creating a new directory "{}": {}'.format(basedir, ex))
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding='utf-8', delay=False)
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
        logging.error('Could not find font "{}"'.format(name))

    logging.info('Falling back to system font')
    try:
        return pygame.font.SysFont(system_font_name, size)
    except Exception as e:
        raise SystemExit('Could not system font "{}": {}'.format(file_path, e))

def load_languages(basedir):
    """Loads the available languages

    :param basedir: The base path
    """
    logging.info('Loading available languages')
    path = os.path.join(basedir, 'resources', 'i18n')
    lang_files = [f[:-len('.json')] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
    logging.info('Available languages: {}'.format(lang_files))
    return lang_files

def load_i18n(basedir, lang):
    """Loads the i18n

    :param basedir: The base path
    :param lang: The language
    """
    file_path = os.path.join(basedir, 'resources', 'i18n', '{}.json'.format(lang))
    logging.info('Trying to load translations from "{}"'.format(file_path))

    translations = {}
    
    if os.path.isfile(file_path):
        logging.info('Translations exist. Loading.')
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                translations = json.load(jsonfile)
        except Exception as ex:
            logging.error('Failed loading from "{}": {}'.format(file_path, ex))
    else:
        logging.info('Translations "{}" do not exist.'.format(file_path))

    return translations

def _load_game_conf(file_path):
    """Loads the game configuration

    :param file_path: The file path
    """
    game_config = {}
    loaded = False
    if os.path.isfile(file_path):
        logging.info('Game config exists. Loading from "{}"'.format(file_path))
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                game_config = json.load(jsonfile)
                loaded = True
        except Exception as ex:
            logging.error('Failed loading from "{}": {}'.format(file_path, ex))

    return loaded, game_config

def _load_game_conf_from_home_folder(basedir):
    """Loads the game configuration from home folder

    :param basedir: The base path
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.game.folder')
    file = app_conf_get('conf.game.name')

    file_path = os.path.join(homedir, homefolder, file)
    logging.info('Trying to load game configuration from home directory {}'.format(file_path))

    return _load_game_conf(file_path)

def _load_game_conf_from_resources(basedir):
    """Loads the game configuration from resources

    :param basedir: The base path
    """
    file = app_conf_get('conf.game.name')
    file_path = os.path.join(basedir, 'resources', file)
    logging.info('Trying to load game configuration from "{}"'.format(file_path))

    return _load_game_conf(file_path)

def _save_game_conf(basedir, game_config):
    """Loads the game configuration to the home directory

    :param basedir: The base path
    :param game_config: The game config
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.game.folder')
    file = app_conf_get('conf.game.name')

    home_dir_path = os.path.join(homedir, homefolder)
    file_path = os.path.join(homedir, homefolder, file)

    logging.info('Writing game config to home directory "{}"'.format(file_path))
    try:
        if not os.path.exists(home_dir_path):
            os.makedirs(home_dir_path)
    except Exception as ex:
        logging.error('Failed creating a new directory in home directory "{}": {}'.format(home_dir_path, ex))

    try:
        with open(file_path, 'w') as jsonfile:
            json.dump(game_config, jsonfile)
    except Exception as ex:
        logging.error('Failed writing to "{}": {}'.format(file_path, ex))

def write_game_conf(basedir, dict_overwrites):
    """Writes the game config with an updated version

    :param basedir: The base path
    :param dict_overwrites: An overwrite dict
    """
    loaded, game_config = _load_game_conf_from_home_folder(basedir)
    if not loaded:
        loaded, game_config = _load_game_conf_from_resources(basedir)

    if loaded:
        for k, v in dict_overwrites.items():
            logging.info('Overriding game config key "{}={}" with "{}={}"'.format(k, game_config[k], k, v))
            game_config[k] = v
        _save_game_conf(basedir, game_config)
    else:
        logging.info('Could not load any game config')

def load_game_conf(basedir, config_version):
    """Loads the game configuration

    :param basedir: The base path
    :param config_version: The config version. If the loaded config version is smaller than the given, it gets overwritten
    """
    logging.info('Loading game configuration, current version: {}'.format(config_version))

    loaded_from_home_dir, game_config = _load_game_conf_from_home_folder(basedir)
    loaded = loaded_from_home_dir
    if not loaded_from_home_dir:
        loaded, game_config = _load_game_conf_from_resources(basedir)

    if loaded:
        _version = game_config['config.version'] if 'config.version' in game_config else 0
        logging.info('Loaded game configuration version: {}'.format(_version))

        if loaded_from_home_dir and _version < config_version:
            homedir = str(Path.home())
            homefolder = app_conf_get('conf.game.folder')
            file = app_conf_get('conf.game.name')
            file_path = os.path.join(homedir, homefolder, file)

            logging.info('Version number {} < specified version number {}'.format(_version, config_version))
            lang = game_config['languages.main']
            logging.info('Removing game config from "{}"'.format(file_path))
            try:
                os.remove(file_path)
            except Exception as ex:
                logging.error('Failed removing "{}": {}'.format(file_path, ex))

            loaded_from_home_dir = False
            loaded, game_config = _load_game_conf_from_resources(basedir)
            game_config['languages.main'] = lang

        if not loaded_from_home_dir:
            _save_game_conf(basedir, game_config)
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
    except Exception as ex:
        logging.error('Failed creating a new directory in home directory "{}": {}'.format(home_dir_path, ex))

    try:
        with open(home_file_path, 'wb') as file:
            dump = json.dumps(highscore_db)
            encrypted = cryptography.encrypt(dump)
            file.write(encrypted)
    except Exception as ex:
        logging.error('Failed writing to "{}": {}'.format(home_file_path, ex))

def load_key(basedir):
    """
    Loads the key

    :param basedir: The base path
    """
    file = app_conf_get('conf.highscore.key.file')
    file_path = os.path.join(basedir, 'resources', file)
    logging.debug('Loading key "{}"'.format(file_path))
    key = None
    try:
        with open(file_path, 'rb') as f:
            key = f.read()
    except pygame.error:
        raise SystemExit('Could not load key "{}": {}'.format(file_path, pygame.get_error()))

    return key

def load_image(basedir, path):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param path: The path + name
    """
    file_path = os.path.join(basedir, 'resources', 'images', path)
    logging.debug('Loading image "{}"'.format(file_path))
    try:
        surface = pygame.image.load(file_path)
    except pygame.error:
        raise SystemExit('Could not load image "{}": {}'.format(file_path, pygame.get_error()))

    return surface

def load_sound(basedir, path):
    """
    Loads a sound, prepares it for play

    :param basedir: The base path
    :param path: The path + name
    """
    file_path = os.path.join(basedir, 'resources', 'sounds', path)
    logging.debug('Loading sound "{}"'.format(file_path))
    try:
        return pygame.mixer.Sound(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load sound "{}"'.format(file_path))

def load_music(basedir, path):
    """
    Loads a sound, prepares it for play

    :param basedir: The base path
    :param path: The path + name
    """
    file_path = os.path.join(basedir, 'resources', 'music', path)
    logging.debug('Loading sound "{}"'.format(file_path))
    try:
        return pygame.mixer.music.load(file_path) if os.path.exists(file_path) else None
    except:
        raise SystemExit('Could not load sound "{}"'.format(file_path))
