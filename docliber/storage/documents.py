import gevent
import gevent.monkey
gevent.monkey.patch_all()
import os
import os.path
from docliber.storage.metadata import MetaEngine
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
