import gevent
import gevent.monkey
gevent.monkey.patch_all()
import os
import os.path
from docliber.storage.metadata import MetaEngine
from hashlib import sha1
import itertools


def take(n, i):
    return list(itertools.islice(i, n))


class DocEngine():
    """
    Layout:
        documents/
            index.db
            aa/
                <hash of document>
    """
    def __init__(self, root_path):
        self.root_path = root_path
        self.doc_path = os.path.join(self.root_path, "documents")
        self._create_dirs()
        self.index = MetaEngine(self.doc_path, dbname='index')

    def _create_dirs(self):
        """
        Create the document storage directories
        """
        if not os.path.exists(self.doc_path):
            os.mkdir(self.doc_path)

    def _add_documents_thread(self, paths):
        index_kvs = []
        greenlets = []

        def injest(path):
            name = os.path.basename(path)
            hasher = sha1()
            print("injesting {0}".format(path))
            with open(path) as fd:
                while True:
                    data = fd.read(hasher.block_size)
                    if data == '':
                        break
                    hasher.update(data)
            file_hash = hasher.hexdigest()
            subdir = os.path.join(self.doc_path, file_hash[0:2])
            if not os.path.exists(subdir):
                os.mkdir(subdir)
            os.rename(path, os.path.join(subdir, file_hash))
            index_kvs.append(("{0}_hash".format(name), file_hash))

        for path in paths:
            greenlets.append(gevent.spawn(injest, path))
        gevent.joinall(greenlets)
        self.index.batch_put_pickle(index_kvs)

    def add_documents(self, paths):
        """
        Add a list of documents to the store
        """
        greenlets = []
        while True:
            batch = take(20, paths)
            print batch
            greenlets.append(gevent.spawn(self._add_documents_thread, batch))
            if len(batch) < 20:
                break
        gevent.joinall(greenlets)
        print("Added {0} documents".format(len(paths)))

    def find_document(self, doc_name):
        """
        Return the path to a document if we have it
        """
        key = "{0}_hash".format(doc_name)
        if self.index.has_key(key):
            fhash = self.index.load_pickle(key)
            subdir = fhash[0:2]
            return os.path.join(self.doc_path, subdir, fhash)
        return None
