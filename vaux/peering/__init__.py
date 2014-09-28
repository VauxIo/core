import requests
from vaux.storage.metadata import MetaEngine


"""
Possible endpoints:
'/peers/'
'/peers/<string:id>/'
'/documents/'
'/documents/<string:id>/'
"""


def SendDoc(doc, peer):
    requests.post("http://{0}:{1}/documents/".format(peer['address'], peer['port']),
                  files={'file': (doc['name'], open(doc['path']))})
    print('Sent {0} to {1}'.format(doc['name'], peer['hostname']))


class Replicator(object):
    def __init__(self, in_queue, hostname, port, db):
        self.index = MetaEngine(hostname, port, db, 'documents')
        self.peers = MetaEngine(hostname, port, db, 'peers')
        self.in_queue = in_queue

    def run(self):
        while True:
            docid = self.in_queue.get()
            document = self.index.get({'id': docid})
            for peer in self.peers.get_all():
                try:
                    SendDoc(document, peer)
                except Exception as e:
                    print('Failed to Send {0} to {1}: {2}'.format(document['name'], peer['hostname'], e))
                    self.in_queue.put(docid)
