from log import Log
from es_connector import EsConnector
from datetime import datetime
import requests
import time
import os


class DowntimeDetector(object):

    def __init__(self):
        es_host = os.getenv('ES_HOST')
        es_port = os.getenv('ES_PORT')
        es_index_name = os.getenv('ES_INDEX_NAME')

        if es_index_name is None:
            es_index_name = "internet_downtime"

        if es_host is None:
            es_host = "localhost"

        if es_port is None:
            es_port = 9200

        self.connector = EsConnector(es_host, es_port, es_index_name)

    def run(self):
        while True:
            if self.is_connection_active():
                print("Successful connection, waiting 10 seconds.")
                time.sleep(10)
            else:
                first_failure_time = datetime.now()

                # Check again until success
                while True:
                    # Check if connection is restored
                    if self.is_connection_active():
                        successful_time = datetime.now()
                        log = Log(first_failure_time, successful_time)
                        result = self.connector.insert_log(log)

                        break

                    # Wait two seconds before testing for resolved connection
                    time.sleep(2)

    def is_connection_active(self):
        try:
            r = requests.get("https://google.com", timeout=10)
            return r.status_code == 200
        except Exception:
            return False


if __name__ == '__main__':
    downtime_detector = DowntimeDetector()
    downtime_detector.run()

