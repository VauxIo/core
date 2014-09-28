import gevent
import gevent.monkey
gevent.monkey.patch_all()
from PyPDF2 import PdfFileReader
import rethinkdb as r
from vaux.storage.metadata import MetaEngine


class PDFIndexer(object):
    def __init__(self, in_queue, hostname, port, db):
        self.index = MetaEngine(hostname, port, db, 'documents')
        self.in_queue = in_queue

    def run(self):
        """
        Thread that waits on a queue and rips metadata from the pdfs and updates
        their entries in rethinkdb
        """
        while True:
            docid = self.in_queue.get()
            document = self.index.get({'id': docid})
            pdf = PdfFileReader(file(document['path'], 'rb'))
            doc_info = pdf.getDocumentInfo()
            pdf_info = {
                'title': doc_info.title or '',
                'author': doc_info.author or '',
                'creator': doc_info.creator or '',
                'producer': doc_info.producer or ''
            }
            r.table('documents').filter(
                {'id': docid}).update(
                    {'pdfinfo': pdf_info}).run(self.index.rdb)
