import gevent
import gevent.monkey
import gevent.queue
gevent.monkey.patch_all()
import os
import os.path
from vaux.storage.metadata import MetaEngine
from vaux.storage.pdfindexer import PDFIndexer
from vaux.peering import Replicator
from hashlib import sha1
import itertools
import datetime
import pytz
from shutil import move


def take(n, i):
    return list(itertools.islice(i, n))


class DocumentExistsError(Exception):
    def __init__(self, message, docid):
        Exception.__init__(self, message)
        self.docid = docid


class DocEngine():
    """
    Layout:
        documents/
            index.db
            aa/
                <hash of document>
    """
    def __init__(self, root_path, hostname, port, db):
        self.root_path = root_path
        self.doc_path = os.path.join(self.root_path, "documents")
        self._create_dirs()
        self.index = MetaEngine(hostname, port, db, 'documents')
        self.pdfindex_queue = gevent.queue.Queue()
        self.replica_queue = gevent.queue.Queue()
        self.pdfindexers = [PDFIndexer(self.pdfindex_queue, hostname, port, db)
                            for x in xrange(0, 4)]
        self.replicators = [Replicator(self.replica_queue, hostname, port, db)
                            for x in xrange(0, 4)]
        map(gevent.spawn, map(lambda thread: thread.run, self.pdfindexers + self.replicators))

    def _create_dirs(self):
        """
        Create the document storage directories
        """
        if not os.path.exists(self.doc_path):
            os.mkdir(self.doc_path)

    def add_document(self, path):
        """
        object format is: {
            "name": <str>,
            "size": <int>,
            "upload_time": <datetime>
            "path": <str> }
        """
        index_objects = []

        name = os.path.basename(path)
        hasher = sha1()
        print("injesting {0}".format(path))
        size = os.stat(path).st_size
        upload_time = datetime.datetime.now(pytz.utc)
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
        final_path = os.path.join(subdir, file_hash)
        if self.index.exists({'path': final_path}):
            original = self.index.get({'path': final_path})
            raise DocumentExistsError("This document already exists", original['id'])
        move(path, final_path)
        index_objects.append({
            'name': name,
            'size': size,
            'upload_time': upload_time,
            'path': final_path})
        self.index.put(index_objects)
        self.pdfindex_queue.put(self.index.get({'path': final_path})['id'])
        self.replica_queue.put(self.index.get({'path': final_path})['id'])

    def get_document_path(self, docid):
        """
        Return the path to a document if we have it. This function
        expects the full name of a document"
        """
        return self.index.get({"id": docid})

    def search_documents(self, search_str):
        """
        Search our index by file name
        """
        for doc in self.index.search(lambda doc: doc['name'].match(search_str)):
            yield doc

    def remove_document(self, docid):
        """
        Spin up greenlets to remove a list of documents
        """
        self.index.delete({'id': docid})

    def list_documents(self):
        """
        Return a list of all documents
        """
        for doc in self.index.get_all():
            yield doc
