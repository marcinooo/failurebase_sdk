import sys
import shutil
import subprocess
from pathlib import Path
from pytest import fixture
from robot import run


current_dir = Path(__file__).parent.absolute()
resource_dir = current_dir / 'resources'


@fixture(scope='session')
def outputs_dir():
    outputs = current_dir / 'outputs'

    if outputs.exists():
        shutil.rmtree(outputs)

    outputs.mkdir()

    yield outputs


# def test_robot_listener_with_connection_error(outputs_dir, capsys):
#
#     status = run(resource_dir / 'robot_test' / 'test.robot', loglevel='TRACE', outputdir=outputs_dir, console='none')
#
#     assert status == 5
#
#     failurebase_log = outputs_dir / 'failurebase.log'
#
#     assert failurebase_log.exists()
#
#     with open(failurebase_log, encoding=sys.getdefaultencoding()) as fh:
#         assert 'requests.exceptions.ConnectionError' in fh.read()
#
#     html_log = outputs_dir / 'log.html'
#
#     with open(html_log, encoding=sys.getdefaultencoding()) as fh:
#         assert 'requests.exceptions.ConnectionError' not in fh.read()


def test_robot_listener_with_connection_error(outputs_dir, capsys):

    process = subprocess.Popen('uvicorn app:app', cwd=resource_dir / "server_mock")

    import time
    time.sleep(2)

    status = run(resource_dir / 'robot_test' / 'test.robot', loglevel='TRACE', outputdir=outputs_dir, console='none')

    assert status == 5

    failurebase_log = outputs_dir / 'failurebase.log'

    assert failurebase_log.exists()

    with open(failurebase_log, encoding=sys.getdefaultencoding()) as fh:
        assert 'requests.exceptions.ConnectionError' not in fh.read()

    process.kill()
