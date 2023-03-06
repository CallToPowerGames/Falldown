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

from lib.Utils import initialize_logger
from lib.AppContext import AppContext

if __name__ == '__main__':
    initialize_logger()

    basedir = os.path.dirname(__file__)

    appctxt = AppContext(basedir)
    exit_code = appctxt.run()
    sys.exit(exit_code)
