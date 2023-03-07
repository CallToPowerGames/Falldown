#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2023 Denis Meyer
#
# This file is part of Falldown.
#

from cryptography.fernet import Fernet
import logging

from lib.Utils import load_key

"""Cryptography"""

# Generate key only once and save it:
# print(Fernet.generate_key())

class Cryptography():
    """Cryptography"""

    def __init__(self, basedir):
        """Initializes Cryptography

        :param basedir: The base path
        """
        logging.info('Initializing Cryptography')

        self.basedir = basedir

        self.key = load_key(basedir)

    def encrypt(self, message):
        """
        Encrypts a message
        """
        encoded_message = message.encode()
        f = Fernet(self.key)
        return f.encrypt(encoded_message)

    def decrypt(self, encrypted_message):
        """
        Decrypts an encrypted message
        """
        f = Fernet(self.key)
        decrypted_message = f.decrypt(encrypted_message)

        return decrypted_message.decode()
