#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

"""Highscore"""

import logging

from lib.Utils import load_highscore_db, save_highscore_db

class Highscore():
    """The highscore"""

    def __init__(self, game_config, cryptography, basedir):
        """Initializes the Highscore

        :param game_config: The game configuration
        :param cryptography: The Cryptography
        :param basedir: The base path
        """
        logging.info('Initializing highscore')

        self.game_config = game_config
        self.cryptography = cryptography
        self.basedir = basedir

        self.max_entries = self.game_config.get('highscore.entries.max')

        self.highscore_db = None

    def _get_sorted(self, db):
        """Returns a sorted database"""
        return sorted(db, key=lambda e: e['score'], reverse=True)

    def _save(self):
        """Save the highscore db"""
        self.save(self.highscore_db)

    def _reload_db(self):
        """Reloads the highscore db"""
        logging.info('Reloading highscore')
        self.highscore_db = load_highscore_db(self.cryptography, self.basedir)
        self.highscore_db = self._get_sorted(self.highscore_db)

    def load(self, reload_db=False):
        """(Re-)Loads the highscore db

        :param reload_db: Whether to reload
        :return: The db
        """
        if reload_db or not self.highscore_db:
            self._reload_db()

        return self.highscore_db

    def save(self, db):
        """Save the highscore db

        :param db: The new db
        """
        logging.info('Saving highscore')
        self.highscore_db = self._get_sorted(self.highscore_db)
        if len(self.highscore_db) > self.max_entries:
            logging.info('Cutting highscore db at {} entries'.format(self.max_entries))
            self.highscore_db = self.highscore_db[:self.max_entries]
        save_highscore_db(self.cryptography, self.highscore_db, self.basedir)

    def add_entry(self, name_key, score, reload_db=True, save_db=True):
        """Adds an entry to the highscore db

        :param name_key: The name key of the player
        :param score: The score
        :param reload: Whether to reload the db before adding/saving
        :param save_db: Whether to save the db after adding the entry
        """
        logging.info('Adding highscore entry [name_key={}, score={}] to db'.format(name_key, score))
        if reload_db:
            self._reload_db()
        self.highscore_db.append({
            'name_key': name_key,
            'score': score
        })
        if save_db:
            self._save()
