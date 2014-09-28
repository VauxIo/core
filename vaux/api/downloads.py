from flask.ext import restful
from . import database
from flask import abort, send_file
from werkzeug import secure_filename
import os


class DownloadInstance(restful.Resource):
    def get(self, id):
        document = database.get_document(id)
        if document is None:
            abort(404)
        return send_file(document['path'])

