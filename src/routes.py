# Copyright 2022 StreamX Developers

# Modules
import os
import logging
from src import app
from aiohttp import web
from requests import get
from secrets import token_hex

# Initialization
def mkresp(code: int, data: dict) -> web.Response:
    return web.json_response({"code": code} | data, status = code)

routes = web.RouteTableDef()
log = logging.getLogger("rich")

# API key handlers
apikey_url, apikey_token = f"{os.getenv('PURCHASEIP')}/active/", os.getenv("PURCHASEKEY")
if not apikey_token.strip():
    log.error("No API key for purchase server set in environment!")

def validate_key(key: str) -> bool:
    return get(f"{apikey_url}{key}", headers = {"X-StreamX-Token": apikey_token}).json()

# Routing
@routes.get("/")
async def status(req) -> web.Response:
    return web.Response(text = "OK", status = 200)

@routes.post("/init")
async def init_server(req) -> web.Response:
    try:
        apikey = req.headers.get("X-StreamX-Key", "")
        if not validate_key(apikey):
            return mkresp(401, {"message": "Invalid API key."})

        d = await req.json()
        gameid, placever = d["gameid"], d["placever"]

        # Generate storage key
        storagekey = str(gameid) + str(placever)
        authkey = app.mongo.keys.find_one({"storagekey": storagekey})
        if authkey is None:
            authkey = token_hex(16)
            app.mongo.keys.insert_one({"storagekey": storagekey, "authkey": authkey, "apikey": apikey, "count": 0})

        else:
            if apikey != authkey["apikey"]:
                return mkresp(401, {"message": "API key missing permissions for requested game."})

            authkey = authkey["authkey"]
            app.mongo.keys.update_one({"storagekey": storagekey}, {"$set": {"count": authkey["count"] + 1}})

        return mkresp(200, {"key": authkey})

    except KeyError:
        return mkresp(400, {"message": "Missing either GameID or Place Version."})

app.add_routes(routes)
