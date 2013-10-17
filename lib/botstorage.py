import shelve


class BotStorage:
    _data = None

    def __init__(self, filename):
        self._data = shelve.open(filename, writeback=True)

    def _key(self, category, key):
        return '%s:%s' % (category, key)

    def get(self, category, key):
        return self._data[self._key(category, key)]

    def set(self, category, key, value):
        self._data[self._key(category, key)] = value
        self._data.sync()

    def setdefault(self, category, key, value):
        # set value only if not yet set
        if not self.exists(category, key):
            self.set(category, key, value)

    def exists(self, category, key):
        return self._key(category, key) in self._data

    def delete(self, category, key):
        del self._data[self._key(category, key)]

class BotConfigWrapper(object):
    prefix = 'core:config'

    def __init__(self, storage, config):
        self.storage = storage
        for key in dir(config):
            if key.startswith('_'):
                continue
            if key == "storage":
                continue
            storage.setdefault(self.prefix, key, getattr(config, key))
        self.__initialised = True

    def __getattr__(self, attr):
        if self.storage.exists(self.prefix, attr):
            return self.storage.get(self.prefix, attr)
        raise AttributeError

    def __setattr__(self, item, value):
        if not self.__dict__.has_key('__initialised'):  # this test allows attributes to be set in the __init__ method
            return object.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):               # any normal attributes are handled normally
            object.__setattr__(self, item, value)
        else:
            self.storage.set(self.prefix, attr, value)
