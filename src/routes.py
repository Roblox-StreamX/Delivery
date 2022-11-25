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

@routes.post("/init")
async def init_server(req) -> web.Response:
    try:
        d = await req.data()
        print(d["gameid"], d["placever"])

    except KeyError:
        return mkresp(400, {"message": "Missing either GameID or Place Version."})

    return mkresp(200, {"message": "OK"})

app.add_routes(routes)
