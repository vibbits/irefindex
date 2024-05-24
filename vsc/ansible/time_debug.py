import csv
import shutil
import os
import time

log = open("/tmp/disk_free.csv", mode='w')
writer = csv.writer(log)

while True:
    # Get disk usage
    home = os.environ.get("HOME")
    free = shutil.disk_usage(f"{home}/.ansible").free
    writer.writerow([free])
    time.sleep(1)


