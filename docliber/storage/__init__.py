from docliber.storage.metadata import MetaEngine
from docliber.storage.documents import DocEngine


class LibreDB(object):
    def __init__(self, root_path, hostname, port, db):
        self.root_path = root_path
        self.peers = MetaEngine(hostname, port, db, 'peers')
        self.docs = DocEngine(root_path, hostname, port, db)

    def add_peer(self, peer):
        """
        Add a set of peers from our databse
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if self.peers.exists({'address': peer['address']}):
            return
        else:
            self.peers.put(peer)

    def remove_peer(self, peerid):
        """
        Remove a set of peers from our database
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        self.peers.delete({'id': peerid})

    def get_peers(self):
        """
        Return all of our peers in a set
        :return A set of peers that we hve
        :rtype frozenset
        """
        return self.peers.get_all()

    def get_peer(self, address):
        return self.peers.get({'address': address})

    def add_document(self, doc_path):
        return self.docs.add_document(doc_path)

    def remove_document(self, docid):
        return self.docs.remove_document(docid)

    def get_document(self, docid):
        return self.docs.get_document_path(docid)

    def get_all_documents(self):
        return self.docs.list_documents()

    def search_documents(self, sstring):
        return self.docs.search_documents(sstring)
