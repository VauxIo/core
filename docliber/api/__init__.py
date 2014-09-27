from flask import Flask, abort, request
from flask.ext import restful
from docliber.storage import LibreDB
from datetime import datetime

app = Flask(__name__)
db = LibreDB('../data')


class PeerInstance (restful.Resource):

    def get(self, id):
        peers = db.meta.load_pickle('peers')
        if id in peers.keys():
            peer = peers[id]
            peer = {
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            }
            return peer
        else:
            abort(404)

    def delete(self, id):
        peers = db.meta.load_pickle('peers')
        if id in peers.keys():
            db.remove_peer(id)
        else:
            abort(404)


class PeerResource(restful.Resource):

    def get(self):
        peers = [
            {
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in db.get_peers()
        ]

        return {'peers': peers}

    def post(self):

        address = request.form.get('address')
        port = request.form.get('port')
        hostname = request.form.get('hostname')
        last_seen = request.form.get('last_seen')

        if not address or not port or not hostname or not last_seen:

            abort(400)

        peer = {
            'address': address,
            'port': port,
            'hostname': hostname,
            'last_seen': datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S')
        }

        db.add_peer(peer)

        peers = [
            {
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in db.get_peers()
        ]

        return {'peers': peers}

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

api = restful.Api(app)
api.add_resource(PeerResource, '/peers/')
api.add_resource(PeerInstance, '/peers/<string:id>/')
api.add_resource(DocumentResource, '/documents/')
