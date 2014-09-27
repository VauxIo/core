import gevent
import gevent.monkey
gevent.monkey.patch_all()
import requests
from docliber.storage import LibreDB
import os.path


ldb = LibreDB("/tmp")
paths = []


def DownloadSingle(link):
    name = link.split('/')[-1]
    path = os.path.join('/tmp', name)
    with open(path, 'w') as fd:
        resp = requests.get(link, stream=True)
        for chunk in resp.iter_content(2048):
            fd.write(chunk)
    paths.append(path)
    print("Downloaded {0}".format(name))


def IngestAllTheThings(*links):
    greenlets = []
    for link in links:
        greenlets.append(gevent.spawn(DownloadSingle, link))
    gevent.joinall(greenlets)
    ldb.docs.add_documents(paths)
