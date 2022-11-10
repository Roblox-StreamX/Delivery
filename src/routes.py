# Copyright 2022 StreamX Developers

# Modules
from src import app
from aiohttp import web

# Initialization
def mkresp(code: int, data: dict) -> web.Response:
    return web.json_response({"code": code} | data, status = code)

routes = web.RouteTableDef()

# Routing
@routes.get("/")
async def status(req) -> web.Response:
    return mkresp(200, {"message": "OK"})

app.add_routes(routes)
