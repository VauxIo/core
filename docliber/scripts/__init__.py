import os
import os.path
from docliber.storage import LibreDB
from docliber.storage.documents import DocumentExistsError
import sys


def load_from_fs():
    path = sys.argv[1]
    ldb = LibreDB('/tmp', 'localhost', 28015, 'docliber')
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('pdf'):
                try:
                    ldb.add_document(os.path.join(root, name))
                except DocumentExistsError as e:
                    print('Document {0} already exists as {1}'.format(name, e.docid))
    print list(ldb.get_all_documents())
