from src.interfaces.logger import ILogger
import datetime as dt
import os
from enum import IntEnum
from typing import Self, Callable


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Logger(ILogger):
    def __init__(self, module_name: str, log_level: LogLevel | str):
        self.__module_name = module_name
        self._print_log: Callable[[str], None]
        directory = os.path.dirname(".\\logs\\")
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

        if self.__min_level == LogLevel.DEBUG:
            self._print_log = print
        else:
            self._print_log = self._log_to_file


    def log_debug(self, message: str) -> Self:
        if self.__min_level <= LogLevel.DEBUG:
            self._print_log(self._get_log_line('DEBUG', message))
        return self


    def log_info(self, message: str) -> Self:
        if self.__min_level <= LogLevel.INFO:
            self._print_log(self._get_log_line('INFO', message))
        return self


    def log_warning(self, message: str) -> Self:
        if self.__min_level <= LogLevel.WARNING:
            self._print_log(self._get_log_line('WARNING', message))
        return self


    def log_error(self, message: str) -> Self:
        if self.__min_level <= LogLevel.ERROR:
            self._print_log(self._get_log_line('ERROR', message))
        return self


    def log_critical(self, message: str) -> Self:
        if self.__min_level <= LogLevel.CRITICAL:
            self._print_log(self._get_log_line('CRITICAL', message))
        return self


    def _log_to_file(self, message: str):
        log_file_name = f"{dt.date.today().strftime('%Y-%m-%d')}.log"
        log_path = os.path.join(self._log_file_dir, log_file_name)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')


    def _get_log_line(self, log_type: str, message: str) -> str:
        log_date: str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cleaned_msg = message.replace('\r', '').replace('\n', '')
        return '[{:^10}] {:>10} : {} - {}'.format(log_date, log_type, self.__module_name, cleaned_msg)


