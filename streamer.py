# Copyright 2022 StreamX Developers

# Modules
import os
from src import app
from aiohttp import web

# Launch server
if __name__ == "__main__":
    web.run_app(
        app,
        port = os.getenv("PORT", 8080)
    )
