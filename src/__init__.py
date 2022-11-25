# Copyright 2022 StreamX Developers

# Modules
import os
import logging
from aiohttp import web
from dotenv import load_dotenv
from pymongo import MongoClient
from rich.logging import RichHandler
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
    host = os.getenv("MONGOHOST")
    app.mongo = MongoClient(
        f"mongodb://{qp(os.getenv('MONGOUSER'))}:{qp(os.getenv('MONGOPASS'))}@{host}",
        int(os.getenv("MONGOPORT"))
    ).streaming
    log.info(f"Connected to MongoDB at {host}!")

except Exception as e:
    print(type(e), e)
    raise e

# Routes
import src.routes  # noqa
