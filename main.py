from log import Log
from es_connector import EsConnector
from datetime import datetime
import requests
import time
import sys


class DowntimeDetector(object):

    def __init__(self):
        if len(sys.argv) < 3:
            print("You must pass an elastic search host URL. Run 'python main.py h|help' for more detail")
            sys.exit(2)

        if sys.argv[1] == "h" or sys.argv[1] == "help":
            print("How to run: python main.py <Elastic Search Host> <Elastic Search Port> <Index Name (optional)>")

        es_hostname = sys.argv[1]
        es_port = sys.argv[2]
        index_name = "internet_downtime"

        if len(sys.argv) == 4:
            index_name = sys.argv[3]

        self.connector = EsConnector(es_hostname, es_port, index_name)

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
                        difference = successful_time - first_failure_time
                        downtime_in_seconds = difference.total_seconds()
                        print("Connection re-established. Downtime (s): % 12.0f" % downtime_in_seconds)

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

