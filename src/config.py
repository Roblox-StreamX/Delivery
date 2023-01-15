# Copyright 2022 iiPython

# Modules
import os
import sys
import json
import logging
import requests

# Initialization
log, upstream_url = logging.getLogger("rich"), os.getenv("STREAMX_UPSTREAM", "")
def e(message: str) -> None:
    log.critical(message)
    sys.exit(1)

if not upstream_url.strip():
    e("Missing upstream configuration URL!")

# Load configuration
if upstream_url != "file":
    try:
        config = requests.get(f"http://{upstream_url}", timeout = 3).json()
        log.info(f"Loaded configuration from {upstream_url}!")

    except requests.exceptions.Timeout:
        e("Timed out while connecting to config server!")

    except Exception:
        e("Configuration server is offline!")

else:
    fl = os.path.dirname(__file__ if not getattr(sys, "frozen", False) else sys.executable)
    fp = os.path.join(fl, "config.json")
    if not os.path.isfile(fp):
        e("Config upstream set to file but no configuration file exists!")

    with open(fp, "r") as fh:
        config = json.loads(fh.read())
