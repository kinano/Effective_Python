#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from functools import wraps

from app import app

def change_logging_level(level=logging.DEBUG):
    """
    Temporarily changes the app log level for the called function
    """
    def decorator(f):
        @wraps(f)

        def decorated_function(*args, **kwargs):
            oldLevel = app.logger.getEffectiveLevel()
            app.logger.setLevel(level)
            try:
                return f(*args, **kwargs)
            finally:
                app.logger.setLevel(oldLevel)

        return decorated_function

    return decorator
