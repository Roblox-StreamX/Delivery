# Copyright 2022 StreamX Developers

# Modules
from aiohttp import web

# Initialization
app = web.Application()

# Routes
import src.routes  # noqa
