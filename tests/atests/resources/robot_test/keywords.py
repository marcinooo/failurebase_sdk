
class MyCustomError(Exception):
    pass


class keywords:

    def show(self, msg):
        self._log(msg, end='')

    def _log(self, msg, end):
        a = 1 / 0  # fail
        print(msg, end=end)

    def raise_sth(self):
        raise MyCustomError('Let\'s fail it!')
