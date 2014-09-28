import rethinkdb as r


class MetaEngine(object):
    def __init__(self, hostname, port, db, table):
        self.rdb = r.connect(host=hostname, port=port, timeout=20)

        try:

            self.rdb.db_create(db).run()

        except Exception, e:

            pass

        self.rdb.close()

        self.rdb = r.connect(host=hostname, port=port, db=db, timeout=20)

        try:

            self.rdb.table_create(table).run()

        except Exception, e:

            pass

        self.table = table

    def get_all(self):
        for item in r.table(self.table).run(self.rdb):
            yield item

    def put(self, data):
        r.table(self.table).insert(data).run(self.rdb)

    def delete(self, filter_data):
        r.table(self.table).filter(filter_data).delete().run(self.rdb)

    def get(self, filter_data):
        result = list(r.table(self.table).filter(filter_data).run(self.rdb))
        if len(result) > 0:
            return result[0]
        return None

    def exists(self, filter_data):
        return len(list(r.table(self.table).filter(filter_data).run(self.rdb))) > 0

    def search(self, ffunc):
        for item in r.table(self.table).filter(ffunc).run(self.rdb):
            yield item
