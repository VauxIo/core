from flask.ext import restful
from . import database
from flask import abort, request
from werkzeug import secure_filename
import os

class DocumentInstance(restful.Resource):

    def get(self, id):

        document = database.get_document(id)

        if document is None:

            abort(404)

        document = {
            'id': document['id'],
            'name': document['name'],
            'size': document['size'],
            'path': '/'.join(document['path'].split('/')[-2:]),
            'uploaded': document['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
        }

        return document

    #def delete(self, id):

    #    document = database.get_document(id)

    #    if document is None:

    #        abort(404)

    #    database.remove_document(id)

    #    return '', 204

class DocumentResource(restful.Resource):

    def options(self):

        pass

    def get(self):

        documents = [
            {
                'id': document['id'],
                'name': document['name'],
                'size': document['size'],
                'path': '/'.join(document['path'].split('/')[-2:]),
                'uploaded': document['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
            } for document in database.get_all_documents()
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

        database.add_document(path)

        documents = [
            {
                'id': document['id'],
                'name': document['name'],
                'size': document['size'],
                'path': document['path'],
                'uploaded': document['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
            } for document in database.get_all_documents()
        ]

        return {'documents': documents}
