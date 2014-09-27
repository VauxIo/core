from flask import Flask
from flask.ext import restful
from docliber.storage import LibreDB

app = Flask(__name__)
db = LibreDB('../data')

class PeerResource (restful.Resource):

    def get (self):
        
        peers = [
            {
            	  'address': peer['address'],
                'port': peer['port'],
                'hostname': peer['hostname'],
                'last_seen': peer['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            } for peer in db.get_peers()
        ]

        return {'peers': peers } 

api = restful.Api(app)
api.add_resource(PeerResource, '/peers/')
