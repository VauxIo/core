import os
from flask import Flask, abort, request
from flask.ext import restful
from vaux.storage import LibreDB
from datetime import datetime
from werkzeug import secure_filename
from cors import crossdomain

app = Flask(__name__)
database = LibreDB('../data', 'localhost', 28015, 'docliber')

from peer import PeerResource, PeerInstance
from document import DocumentResource, DocumentInstance

api = restful.Api(app)

api.decorators=[crossdomain(origin='*')]

api.add_resource(PeerResource, '/peers/')
api.add_resource(PeerInstance, '/peers/<string:id>/')
api.add_resource(DocumentResource, '/documents/')
api.add_resource(DocumentInstance, '/documents/<string:id>/')
