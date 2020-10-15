#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2019. 10. 30.

@author: yhj
'''

import os
import sys
import logging

from logging import INFO, ERROR
#from logging import INFO, DEBUG, ERROR, WARNING, CRITICAL

if hasattr(sys, 'frozen'): #support for py2exe
    _SRCFILE = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _SRCFILE = __file__[:-4] + '.py'
else:
    _SRCFILE = __file__
_SRCFILE = os.path.normcase(_SRCFILE)

class Logger:
    '''Log 유틸'''
    def __init__(self):
        '''Logger default 정보'''
        self.log = logging.getLogger()
        self.log.setLevel(INFO)

        log_format = logging.Formatter("%(asctime)s %(levelname)s[%(filename)s/line%(lineno)s]: %(message)s")

        self.log_stream_handler = logging.StreamHandler(sys.stdout)
        self.log_stream_handler.setFormatter(log_format)

        # log 중복 출력 방지
        if self.log.hasHandlers():
            self.log.handlers.clear()

        self.log.addHandler(self.log_stream_handler)

#     # CRITICAL level 로그 처리
#     def critical(self, msg, *args):
#         '''CRITICAL level 로그 처리'''
#         if self.log.isEnabledFor(CRITICAL):
#             self._log(CRITICAL, msg, args)

    # ERROR level 로그 처리
    def error(self, msg, *args):
        '''ERROR level 로그 처리'''
        if self.log.isEnabledFor(ERROR):
            self._log(ERROR, msg, args)

#     # WARNING level 로그 처리
#     def warning(self, msg, *args):
#         '''WARNING level 로그 처리'''
#         if self.log.isEnabledFor(WARNING):
#             self._log(WARNING, msg, args)

    # INFO level 로그 처리
    def info(self, msg, *args):
        '''INFO level 로그 처리'''
        if self.log.isEnabledFor(INFO):
            self._log(INFO, msg, args)

#     # DEBUG level 로그 처리
#     def debug(self, msg, *args):
#         '''DEBUG level 로그 처리'''
#         if self.log.isEnabledFor(DEBUG):
#             self._log(DEBUG, msg, args)

    # log 메세지 정보 정리
    def _log(self, level, msg, args):
        ''' log 메세지 정보 정리'''
        exc_info = None
        extra = None

        if _SRCFILE:
            try:
                file_name, line_num, func_name = self.find_caller()
            except ValueError:
                file_name, line_num, func_name = "Unknown file", 0, "Unknown function"
        else:
            file_name, line_num, func_name = "Unknown file", 0, "Unknown function"

        record = self.log.makeRecord(self.log.name,
                                     level,
                                     file_name,
                                     line_num,
                                     msg,
                                     args,
                                     exc_info,
                                     func_name, extra)
        self.log.handle(record)

    # 호출지 관련 정보 조회
    def find_caller(self):
        ''' 호출지 관련 정보 조회'''
        log_current_frame = logging.currentframe()

        if log_current_frame is not None:
            log_current_frame = log_current_frame.f_back

        results = "(unknown file)", 0, "(unknown function)"
        while hasattr(log_current_frame, "f_code"):
            f_code = log_current_frame.f_code
            filename = os.path.normcase(f_code.co_filename)
            if filename == _SRCFILE:
                log_current_frame = log_current_frame.f_back
                continue
            results = (f_code.co_filename, log_current_frame.f_lineno, f_code.co_name)
            break

        return results
    