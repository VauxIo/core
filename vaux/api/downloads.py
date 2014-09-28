from flask.ext import restful
from . import database
from flask import abort, send_file
import mimetypes


class DownloadInstance(restful.Resource):
    def get(self, id):
        document = database.get_document(id)
        if document is None:
            abort(404)
        mt = mimetypes.guess_type(document['path'])[0]
        return send_file(document['path'],
                         as_attachment=True,
                         attachment_filename=document['name'],
                         mimetype=mt)
