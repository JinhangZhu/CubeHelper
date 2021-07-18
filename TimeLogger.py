# -*- coding: utf-8 -*-
# @Time     : 2021/7/18 23:47
# @Author   : Jinhang
# @File     : TimeLogger.py


from datetime import datetime
import logging


class TimeLogger:
    def __init__(self):
        self._last_time = None

    def info(self, msg="", start=False):
        indent_string = ''
        logging.info(indent_string + msg)
        current_time = datetime.now()

        if start:
            self._last_time = current_time
        else:
            duration = current_time - self._last_time
            duration = int(duration.total_seconds() * 1000)
            logging.info(indent_string + 'Duration: {} ms'.format(duration))

    # @staticmethod
    def debug(self, msg=""):
        indent_string = ' ' * 4
        logging.debug(indent_string + msg)
