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
                    current_peers.append(peer)
            self.meta.put_pickle("peers", current_peers)

    def remove_peer(self, peer):
        """
        Remove a set of peers from our database
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if self.meta.has_key("peers"):
            current_peers = self.meta.load_pickle("peers")
            if peer['address'] in current_peers:
                del current_peers[peer['address']]
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
