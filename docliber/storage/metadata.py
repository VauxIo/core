import leveldb
import os.path
import cPickle


class MetaEngine(object):
    def __init__(self, root_path, dbname='meta'):
        self.db = leveldb.LevelDB(os.path.join(root_path, dbname))

    def batch_put_pickle(self, kvs):
        """
        Submit a batch of writes to leveldb.
        values are automatically pickled
        :param kvs: List of tuples containing (key,val)
        :type kvs: list
        """
        batch = leveldb.WriteBatch()
        for key, val in kvs:
            batch.Put(key, cPickle.dumps(val))
        self.db.Write(batch, sync=True)

    def batch_delete(self, keys):
        """
        Delete a batch of keys from leveldb
        :param keys: The keys to delete
        :type keys: list
        """
        batch = leveldb.WriteBatch()
        for key in keys:
            batch.Delete(key)
        self.db.Write(batch, sync=True)

    def delete(self, key):
        """
        Delete a single key
        """
        self.db.Delete(key)

    def put_pickle(self, key, val):
        """
        Take a python value, pickle it, and put into the datbase
        :param key: The key to store the value under
        :type key: str
        :param val: Any python object that can be pickled
        :type val: object
        """
        self.db.Put(key, cPickle.dumps(val))

    def load_pickle(self, key):
        """
        Load a python value out of the database. The value of this key
        is automaticaly unpickled and returned.
        :param key: the key to lookup in leveldb
        :type key: str
        """
        return cPickle.loads(self.db.Get(key))

    def put_iterable(self, root_key, iterable):
        """
        Store the size of an iterable in the root_key
        and then do {root_key}_<n> to store the actual contents of
        the iterable
        :param root_key: The key to store this iterable under
        :type root_key: str
        :param iterable: An interable to store in leveldb
        :type iterable: iterable
        """
        self.put_pickle(root_key, len(iterable))
        items = [("{0}_{1}".format(root_key, index), item)
                 for index, item in enumerate(iterable)]
        self.batch_put_pickle(items)


    def load_iterable(self, root_key):
        """
        Load a list of some kind back into memory from leveldb
        produces a generator that yields key value pairs
        """
        size = self.load_pickle(root_key)
        kfrom = "{0}_0".format(root_key)
        kto = "{0}_{1}".format(root_key, size-1)
        for key, val in self.db.RangeIter(key_from=kfrom, key_to=kto):
            yield key, cPickle.loads(val)

    def delete_iterable(self, root_key):
        """
        Delete an iterable from leveldb. This uses MetaEngine.batch_delete
        """
        size = self.load_pickle(root_key)
        items = ["{0}_{1}".format(root_key, x) for x in xrange(0, size)]
        self.batch_delete(items)

    def has_key(self, key):
        """
        Check if a key is in the datbase
        """
        try:
            self.load_pickle(key)
            return True
        except:
            return False
