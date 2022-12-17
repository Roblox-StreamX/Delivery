# Copyright 2022 StreamX Developers

# Modules
import os
import gzip
from datetime import datetime, timedelta

# Initialization
logs_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.isdir(logs_folder):
    os.mkdir(logs_folder)

# Handlers
def compress_old() -> None:
    for file in os.listdir(logs_folder):
        fp = os.path.join(logs_folder, file)
        if ".gz" in file:
            continue

        if datetime.now() - datetime.strptime(file, "%m-%d-%y.log") > timedelta(days = 7):
            with gzip.open(fp + ".gz", "wb") as fh:
                with open(fp, "rb") as fh_:
                    data = fh_.read()

                fh.write(data)

            os.remove(file)

def write_log(text: str, date: str = None) -> None:
    logfile = os.path.join(logs_folder, (date or datetime.now().strftime("%m-%d-%y")) + ".log")
    with open(logfile, "a") as fh:
        fh.write(f"{text}\n")

    compress_old()
