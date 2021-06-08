from elasticsearch7 import Elasticsearch
from datetime import datetime
from helper import create_now_timestamp


class EsConnector:
    def __init__(self, hostname, port, index_name, timezone):
        self.hostname = hostname
        self.port = port
        self.index_name = index_name
        self.es = Elasticsearch([{'host': hostname, 'port': port}])
        self.timezone = timezone

        self.create_index_if_non_existent()

    def create_index_if_non_existent(self):
        if self.es.indices.exists(index=self.index_name):
            return

        self.es.indices.create(index=self.index_name)

    def insert_log(self, log):
        log_entry = {
            "start_time": log.start_time,
            "end_time": log.end_time,
            "total_time": log.total_time,
            "added": create_now_timestamp(self.timezone)
        }

        res = self.es.index(index=self.index_name, body=log_entry)
