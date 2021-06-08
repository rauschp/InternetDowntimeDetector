from log import Log
from es_connector import EsConnector
from helper import create_now_timestamp
import requests
import time
import os


class DowntimeDetector(object):

    def __init__(self):
        es_host = os.getenv('ES_HOST')
        es_port = os.getenv('ES_PORT')
        es_index_name = os.getenv('ES_INDEX_NAME')
        self.timezone = os.getenv('TIMEZONE')

        if es_index_name is None:
            es_index_name = "internet_downtime"

        if es_host is None:
            es_host = "localhost"

        if es_port is None:
            es_port = 9200

        if self.timezone is None:
            self.timezone = "America/Indianapolis"

        self.connector = EsConnector(es_host, es_port, es_index_name, self.timezone)

    def run(self):
        while True:
            if self.is_connection_active():
                time.sleep(10)
            else:
                first_failure_time = create_now_timestamp(self.timezone)

                # Check again until success
                while True:
                    # Check if connection is restored
                    if self.is_connection_active():
                        successful_time = create_now_timestamp(self.timezone)
                        log = Log(first_failure_time, successful_time)
                        result = self.connector.insert_log(log)

                        print("[Outage Detected] Start: " + first_failure_time + " | End: " + successful_time)

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

