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

    def __init__(self, cryptography, basedir, max_entries=100):
        """Initializes the Highscore

        :param cryptography: The Cryptography
        :param basedir: The base path
        :param max_entries: Max highscore entries
        """
        logging.info('Initializing highscore')

        self.cryptography = cryptography
        self.basedir = basedir
        self.max_entries = max_entries

        self.highscore_db = None

    def _save(self):
        """Save the highscore db"""
        self.save(self.highscore_db)

    def _reload_db(self):
        """Reloads the highscore db"""
        logging.info('Reloading highscore')
        self.highscore_db = load_highscore_db(self.cryptography, self.basedir)
        self.highscore_db = sorted(self.highscore_db, key=lambda e: e['score'], reverse=True)

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
        self.highscore_db = sorted(db, key=lambda e: e['score'], reverse=True)
        if len(self.highscore_db) > self.max_entries:
            logging.info('Cutting highscore db to {} entries'.format(self.max_entries))
            self.highscore_db = self.highscore_db[:self.max_entries]
        save_highscore_db(self.cryptography, self.highscore_db, self.basedir)

    def add_entry(self, name, score, reload_db=True, save_db=True):
        """Adds an entry to the highscore db

        :param name: The name of the player
        :param score: The score
        :param reload: Whether to reload the db before adding/saving
        :param save_db: Whether to save the db after adding the entry
        """
        logging.info('Adding highscore entry [name={}, score={}] to db'.format(name, score))
        if reload_db:
            self._reload_db()
        self.highscore_db.append({
            'name': name,
            'score': score
        })
        if save_db:
            self._save()
