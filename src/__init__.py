# Copyright 2022 StreamX Developers

# Modules
import logging
from aiohttp import web
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

# Aiohttp setup
app = web.Application()
log.info("Initialized aiohttp successfully!")

# Connect to MongoDB

from .webhook import upload_info
upload_info(401, "69420YourMomIsFatLollllllllllllllllllllllllllll", "100000000999999999", "1234567890", "69420", "SOme detailed error message.")

user, pasw = config["mongo"]["username"], config["mongo"]["password"]
authstr = f"{qp(user)}:{qp(pasw)}@" if (user.strip() and pasw.strip()) else ""
mongo = MongoClient(
    f"mongodb://{authstr}{config['mongo']['address']}",
    serverSelectionTimeoutMS = 1000  # ms
)
try:
    mongo.server_info()
    log.info(f"Connected to MongoDB at {mongo.client.address[0]}!")

    app.mongo = mongo["streaming"]
    app.payment = mongo["purchases"]

except errors.ServerSelectionTimeoutError:
    log.critical("FAILED to connect to MongoDB! Check MONGO* env and database status.")
    exit(1)

# Routes
import src.routes  # noqa
