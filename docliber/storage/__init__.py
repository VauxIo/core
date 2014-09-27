from docliber.storage.metadata import MetaEngine
from docliber.storage.documents import DocEngine


class LibreDB(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.meta = MetaEngine(self.root_path)
        self.docs = DocEngine(self.root_path)

    def add_peer(self, peer):
        """
        Add a set of peers from our databse
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if not self.meta.has_key("peers"):
            self.meta.put_pickle("peers", {peer['address']: peer})
        else:
            current_peers = self.meta.load_pickle("peers")
            if peer['address'] not in current_peers:
                    current_peers[peer['address']] = peer
            self.meta.put_pickle("peers", current_peers)

    def remove_peer(self, peer_address):
        """
        Remove a set of peers from our database
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if self.meta.has_key("peers"):
            current_peers = self.meta.load_pickle("peers")
            if peer_address in current_peers:
                del current_peers[peer_address]
            self.meta.put_pickle("peers", current_peers)

    def get_peers(self):
        """
        Return all of our peers in a set
        :return A set of peers that we hve
        :rtype frozenset
        """
        if self.meta.has_key("peers"):
            return [peer for _, peer in self.meta.load_pickle("peers").iteritems()]
        else:
            return []

    def add_document(self, doc_path):
        return self.docs.add_documents([doc_path])

    def remove_document(self, doc_name):
        return self.docs.remove_documents([doc_name])

    def get_document(self, doc_name):
        return self.docs.get_document_path(doc_name)

    def get_all_documents(self):
        return self.docs.list_documents()

    def search_documents(self, sstring):
        return self.docs.search_documents(sstring)
