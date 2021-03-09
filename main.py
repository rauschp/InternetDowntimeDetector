from log import Log
from datetime import datetime
import requests
import time


class DowntimeDetector(object):
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
                        # CREATE LOG
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
    DowntimeDetector.run()

