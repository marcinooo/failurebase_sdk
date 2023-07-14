"""Failurebase client module."""

import os
import sys
import logging
from pathlib import Path
from typing import Any
from requests import post, Response


class FailurebaseClient:
    """Client to send given log data to server"""

    def __init__(self, url: str, no_proxy: str = None, log_file: Path | str ='failurebase.log',
                 log_level: int = logging.WARNING, encoding: str | None = None):

        self.url = url
        self.no_proxy = no_proxy

        self._logger = self._setup_logger(log_file, log_level, encoding)

        self._logger.info('Failurebase client configured successfully.')
        self._logger.debug(f'Configuration: url = "{self.url}", no_proxy = "{self.no_proxy}"')

    def log(self, data: Any, safe: bool = True) -> Response:
        """
        Gets given data and sends to server.

        :param data: data to log
        :param safe: if it is True all errors will be handled and fails will not break your code
        :return: response
        """

        if self.no_proxy:
            os.environ['no_proxy'] = self.no_proxy  # '127.0.0.1,localhost'

        try:
            response = post(url=self.url, json=data)
        except Exception as error:

            self._logger.error('Failure was not sent.')
            self._logger.exception(error)

            if not safe:
                raise error from None

            response = None

            self._logger.info('Error was ignored (safe mode is on).')

        else:
            if response.status_code == 201:
                self._logger.info('Response successful: %s', response.content.decode('utf-8'))
            else:
                self._logger.info('Response unsuccessful: %s', response.content.decode('utf-8'))

        return response

    @staticmethod
    def _setup_logger(log_file: Path | str, log_level: int, encoding: str | None = None) -> logging.Logger:

        logger = logging.getLogger('failurebase')
        logger.propagate = False

        if encoding is None:
            encoding = sys.getdefaultencoding()

        handler = logging.FileHandler(log_file, mode='w', encoding=encoding)
        handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger
