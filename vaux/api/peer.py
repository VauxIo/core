from flask.ext import restful
from . import database
from flask import abort, request
from datetime import datetime
import pytz
import requests


class PeerInstance (restful.Resource):

    def get(self, id):

        peer = database.get_peer(id)

        if peer is None:

            abort(404)

        peer = {
            'id': peer['id'],
            'address': peer['address'],
            'port': peer['port'],
            'hostname': peer['hostname'],
            'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
        }

        return peer

    #def delete(self, id):

    #    peer = database.get_peer(id)

    #    if peer is None:

    #        abort(404)

    #    database.remove_peer(id)

    #    return '', 204

class PeerResource(restful.Resource):

    def get(self):

        peers = [
            {
                'id': peer['id'],
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in database.get_peers()
        ]

        return {'peers': peers}

    def post(self):

        address = request.form.get('address')
        port = request.form.get('port')
        hostname = request.form.get('hostname')
        last_seen = datetime.utcnow()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not address or not port or not hostname or not last_seen:

            abort(400)

        last_seen = pytz.utc.localize(last_seen)

        if not latitude or not longitude:
            loc_resp = requests.get(
                'https://freegeoip.net/json/{0}'.format(address))

            try:
                location = loc_resp.json()
                location = {'latitude': location['latitude'], 'longitude': location['longitude']}
            except:
                location = {'latitude': 'unknown', 'longitude': 'unknown'}
        else:
            location = {'latitude': latitude, 'longitude': longitude}

        peer = {
            'address': address,
            'port': port,
            'hostname': hostname,
            'last_seen': last_seen,
            'location': location
        }
        database.add_peer(peer)
        peers = [
            {
                'id': peer['id'],
                'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in database.get_peers()
        ]

        return {'peers': peers}
