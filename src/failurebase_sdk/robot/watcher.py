"""Robot framework library with listener."""

import logging
from datetime import datetime
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
from failurebase_sdk.client import FailurebaseClient
from failurebase_sdk.utils import FailureSchema, TestSchema


class watcher:
    """Robot Framework fail listener."""

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):

        self.ROBOT_LIBRARY_LISTENER = self

        self.last_log = None
        self.client = None

    def initialize_failurebase(self, url: str, no_proxy: str, log_name: Path | str | None = None,
                               log_level: int = logging.WARNING, encoding: str | None = None) -> None:
        """Keyword to initialize """

        if log_name is None:
            output_dir = BuiltIn().get_variable_value("${OUTPUT DIR}")
            log_name = Path(output_dir) / 'failurebase.log'

        self.client = FailurebaseClient(url, no_proxy, log_name, log_level, encoding)

    def log_message(self, message: str) -> None:
        self.last_log = message

    def end_test(self, _, attrs) -> None:

        if attrs['status'] == 'FAIL':
            timestamp = self._change_format_of_timestamp(self.last_log.get('timestamp'))
            test = TestSchema(uid=attrs.get('longname'), file=attrs.get('source'), marks=attrs.get('tags'))
            fail = FailureSchema(test=test, message=attrs.get('message'), traceback=self.last_log.get('message'),
                                 timestamp=timestamp)

            self.client.log(fail.dump())

    @staticmethod
    def _change_format_of_timestamp(timestamp: str) -> str:
        ts_obj = datetime.strptime(timestamp, '%Y%m%d %H:%M:%S.%f')
        return datetime.strftime(ts_obj, '%Y-%m-%dT%H:%M:%S.%f')
