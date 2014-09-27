import falcon


class PeeringResource(object):
    def on_get(self, req, resp):
        """
        Return our list of peers
        """

    def on_put(self, req, resp):
        """
        Merge out peer list with someone elses
        """
