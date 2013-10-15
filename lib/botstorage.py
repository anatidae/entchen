import shelve


class BotStorage:
    _data = None

    def __init__(self, config):
        self._data = shelve.open(config.storage, writeback=True)

    def _key(self, category, key):
        return '%s:%s' % (category, key)

    def get(self, category, key):
        return self._data[self._key(category, key)]

    def set(self, category, key, value):
        self._data[self._key(category, key)] = value
        self._data.sync()

    def delete(self, category, key):
        del self._data[self._key(category, key)]
