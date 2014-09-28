from flask.ext import restful
from . import db
from flask import abort, request
import datetime

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