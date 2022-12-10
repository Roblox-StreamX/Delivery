# Copyright 2022 StreamX Developers

# Modules
import os
import logging
from aiohttp import web
from dotenv import load_dotenv
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

# Initialization
load_dotenv()  # In production we won't use a .env file

app = web.Application()
log.info("Initialized aiohttp successfully!")

# Connect to MongoDB
try:
    host, port = os.getenv("MONGO_HOST", ""), int(os.getenv("MONGO_PORT", 27017))
    user, pasw = os.getenv("MONGO_USER", ""), os.getenv("MONGO_PASS", "")
    authstr = f"{qp(user)}:{qp(pasw)}@" if (user.strip() and pasw.strip()) else ""
    mongo = MongoClient(
        f"mongodb://{authstr}{host}",
        port = port,
        serverSelectionTimeoutMS = 1000  # ms
    )
    try:
        mongo.server_info()
        log.info(f"Connected to MongoDB at {host}!")

        app.mongo = mongo["streaming"]
        app.payment = mongo["purchases"]

    except errors.ServerSelectionTimeoutError:
        log.critical("FAILED to connect to MongoDB! Check MONGO* env and database status.")
        exit(1)

except ValueError:
    log.error("FAILED to read environment variables! Check MONGO_PORT and ensure it's an integer.")
    exit(1)

# Routes
import src.routes  # noqa
