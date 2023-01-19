# Copyright 2022 StreamX Developers

# Modules
import os
import falcon
import logging
from rich.logging import RichHandler
from pymongo import MongoClient, errors
from urllib.parse import quote_plus as qp

# Setup logging
logging.basicConfig(
    level = "INFO",
    format = "%(message)s",
    datefmt = "[%X]",
    handlers = [RichHandler()]
)
log = logging.getLogger("rich")

# Load configuration (after rich)
from .config import config

# Falcon setup
app = falcon.App()
log.info("Initialized Falcon successfully!")

# Connect to MongoDB
user, pasw = config["mongo"]["username"], config["mongo"]["password"]
authstr = f"{qp(user)}:{qp(pasw)}@" if (user.strip() and pasw.strip()) else ""
mongo = MongoClient(
    f"mongodb://{authstr}{config['mongo']['address']}",
    serverSelectionTimeoutMS = 1000  # ms
)
try:
    if os.getenv("SXPYINSTALLER") != "1":
        mongo.server_info()
        log.info(f"Connected to MongoDB at {mongo.client.address[0]}!")

        app.mongo = mongo["streaming"]
        app.payment = mongo["purchases"]

except errors.ServerSelectionTimeoutError:
    log.critical("FAILED to connect to MongoDB! Check MONGO* env and database status.")
    exit(1)

# Routes
import src.routes  # noqa
