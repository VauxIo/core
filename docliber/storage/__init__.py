from docliber.storage.metadata import MetaEngine
from docliber.storage.documents import DocEngine


class LibreDB(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.meta = MetaEngine(self.root_path)
        self.docs = DocEngine(self.root_path)

    def add_peers(self, peers):
        """
        Add a set of peers from our databse
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if not self.meta.has_key("peers"):
            self.meta.put_pickle("peers", frozenset(peers))
        else:
            self.meta.put_pickle(
                "peers",
                self.meta.load_pickle("peers") + frozenset(peers))

    def remove_peers(self, peers):
        """
        Remove a set of peersfrom our database
        :param peers: a set of peers to add
        :type peers: frozenset
        """
        if self.meta.has_key("peers"):
            self.meta.put_pickle(
                "peers",
                self.meta.load_pickle("peers") - frozenset(peers))

    def get_peers(self):
        """
        Return all of our peers in a set
        :return A set of peers that we hve
        :rtype frozenset
        """
        if self.meta.has_key("peers"):
            return self.meta.load_pickle("peers")
        else:
            return frozenset(())
