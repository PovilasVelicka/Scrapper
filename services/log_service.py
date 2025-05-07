
from interfaces.logger import ILogger

import datetime as dt
import os
from enum import IntEnum
from typing import Self


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class FileLogger(ILogger):
    """
    A simple file logger that writes messages to a log file.
    Each log entry includes a timestamp and the log type.
    The log file is named after the current date and stored in the specified directory.
    """

    def __init__(self, log_file_dir: str, log_level: LogLevel | str):
        directory = os.path.dirname(log_file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._log_file_dir = directory

        if isinstance(log_level, LogLevel):
            self.__min_level = log_level.value
        else:
            try:
                self.__min_level = LogLevel[log_level].value
            except KeyError:
                self.__min_level = LogLevel.INFO

    def log_debug(self, message: str) -> Self:
        if self.__min_level <= LogLevel.DEBUG:
            self._append(self._get_log_line('DEBUG', message))
        return self

    def log_info(self, message: str) -> Self:
        if self.__min_level <= LogLevel.INFO:
            self._append(self._get_log_line('INFO', message))
        return self

    def log_warning(self, message: str) -> Self:
        if self.__min_level <= LogLevel.WARNING:
            self._append(self._get_log_line('WARNING', message))
        return self

    def log_error(self, message: str) -> Self:
        if self.__min_level <= LogLevel.ERROR:
            self._append(self._get_log_line('ERROR', message))
        return self

    def log_critical(self, message: str) -> Self:
        if self.__min_level <= LogLevel.CRITICAL:
            self._append(self._get_log_line('CRITICAL', message))
        return self

    def _append(self, message: str):
        log_file_name = f"{dt.date.today().strftime('%Y-%m-%d')}.log"
        log_path = os.path.join(self._log_file_dir, log_file_name)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    @staticmethod
    def _get_log_line(log_type: str, message: str) -> str:
        log_date: str = dt.datetime.now().strftime('%H:%M:%S')
        cleaned_msg = message.replace('\r', '').replace('\n', '')
        return '[{:^10}] {:>10} : {}'.format(log_date, log_type, cleaned_msg)


class ConsolLoger(ILogger):
    """
    A simple console logger that print messages to a consol.
    Each log entry includes a timestamp and the log type.
    """

    def __init__(self, log_level: LogLevel | str):
        if isinstance(log_level, LogLevel):
            self.__min_level = log_level.value
        else:
            try:
                self.__min_level = LogLevel[log_level].value
            except KeyError:
                self.__min_level = LogLevel.INFO

    def log_debug(self, message: str) -> Self:
        if self.__min_level <= LogLevel.DEBUG:
            print(self._get_log_line('DEBUG', message))
        return self

    def log_info(self, message: str) -> Self:
        if self.__min_level <= LogLevel.INFO:
            print(self._get_log_line('INFO', message))
        return self

    def log_warning(self, message: str) -> Self:
        if self.__min_level <= LogLevel.WARNING:
            print(self._get_log_line('WARNING', message))
        return self

    def log_error(self, message: str) -> Self:
        if self.__min_level <= LogLevel.ERROR:
            print(self._get_log_line('ERROR', message))
        return self

    def log_critical(self, message: str) -> Self:
        if self.__min_level <= LogLevel.CRITICAL:
            print(self._get_log_line('CRITICAL', message))
        return self

    @staticmethod
    def _get_log_line(log_type: str, message: str) -> str:
        log_date: str = dt.datetime.now().strftime('%H:%M:%S')
        cleaned_msg = message.replace('\r', '').replace('\n', '')
        return '[{:^10}] {:>10} : {}'.format(log_date, log_type, cleaned_msg)