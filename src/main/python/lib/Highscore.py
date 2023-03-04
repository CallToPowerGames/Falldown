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

    def load(self, reload=False):
        """(Re-)Loads the highscore db

        :param reload: Whether to reload
        :return: The db
        """
        if reload or not self.highscore_db:
            logging.info('Loading highscore')
            self.highscore_db = load_highscore_db(self.cryptography, self.basedir)
            self.highscore_db = sorted(self.highscore_db, key=lambda e: e['score'], reverse=True)

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
