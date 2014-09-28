from flask.ext import restful
from . import db
from flask import abort, request

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
