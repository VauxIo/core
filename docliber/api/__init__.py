import os
from flask import Flask, abort, request
from flask.ext import restful
from docliber.storage import LibreDB
from datetime import datetime
from werkzeug import secure_filename

app = Flask(__name__)
db = LibreDB('../data')


class DocumentResource(restful.Resource):

    def get(self):

        documents = [
            {
                'name': document['name'],
                'size': document['size'],
                'uploaded': document['uploaded'].strftime('%Y-%m-%d %H:%M:%S')
            } for document in db.get_all_documents()
        ]

        return {'documents': documents}

    def post(self):

        file = request.files['file']

        if not file:

            abort(400)

        filename = secure_filename(file.filename)

        if not os.path.exists('/tmp/uploaded/'):

            os.makedirs('/tmp/uploaded/')

        path = os.path.join('/tmp/uploaded/', filename)

        file.save(path)

        db.add_document(path)

        return ''

from peer import PeerResource, PeerInstance

api = restful.Api(app)
api.add_resource(PeerResource, '/peers/')
api.add_resource(PeerInstance, '/peers/<string:id>/')
api.add_resource(DocumentResource, '/documents/')
