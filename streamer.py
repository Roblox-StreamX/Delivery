# Copyright 2022 StreamX Developers

# Modules
import os
from src import app
from aiohttp import web

# Launch server
if __name__ == "__main__":
    web.run_app(
        app,
        host = os.getenv("SERVHOST", "0.0.0.0"),
        port = os.getenv("SERVPORT", 8080),
    )
