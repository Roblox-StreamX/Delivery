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
        authkey, upload = app.mongo.keys.find_one({"storagekey": storagekey}), False
        if authkey is None:
            authkey, upload = token_hex(16), True
            app.mongo.keys.insert_one({"storagekey": storagekey, "authkey": authkey, "apikey": apikey})

        else:
            if apikey != authkey["apikey"]:
                return mkresp(401, {"message": "API key missing permissions for requested game."})

            elif int(placever) == 0:
                app.mongo.parts[storagekey].drop()
                app.mongo.keys.delete_one({"authkey": authkey["authkey"]})
                authkey, upload = token_hex(16), True
                app.mongo.keys.insert_one({"storagekey": storagekey, "authkey": authkey, "apikey": apikey})

            else:
                authkey = authkey["authkey"]

        return mkresp(200, {"key": authkey, "upload": upload})

    except KeyError:
        return mkresp(400, {"message": "Missing either GameID or Place Version."})

@routes.post("/upload")
async def upload_part(req) -> web.Response:
    authkey = str(req.headers.get("X-StreamX-Auth", ""))
    if len(authkey) > 32:  # This is just sanitization for MongoDB
        return mkresp(400, {"message": "Invalid auth key."})

    kdata = app.mongo.keys.find_one({"authkey": authkey})
    if kdata is None:
        return mkresp(400, {"message": "Invalid auth key."})

    # Fetch part data
    try:
        tb = []
        for part in (await req.read()).decode().split(","):
            x, y, z, d = part.split(":")
            tb.append({"x": float(x), "y": float(y), "z": float(z), "d": d})

        app.mongo.parts[kdata["storagekey"]].insert_many(tb)
        return mkresp(200, {"message": "OK"})

    except Exception:
        return mkresp(400, {"message": "Invalid part information."})

@routes.post("/download")
async def download_parts(req) -> web.Response:
    authkey = str(req.headers.get("X-StreamX-Auth", ""))
    if len(authkey) > 32:  # This is just sanitization for MongoDB
        return mkresp(400, {"message": "Invalid auth key."})

    kdata = app.mongo.keys.find_one({"authkey": authkey})
    if kdata is None:
        return mkresp(400, {"message": "Invalid auth key."})

    # Calculate head position
    try:
        d = await req.json()
        (x, y, z), sd = d["HeadPosition"], d["StudDifference"]
        x, y, z = float(x), float(y), float(z)
        parts = list(app.mongo.parts[kdata["storagekey"]].find({
            "x": {"$lt": x + sd, "$gt": x - sd},
            "y": {"$lt": y + sd, "$gt": y - sd},
            "z": {"$lt": z + sd, "$gt": z - sd},
        }))
        if not parts:
            return web.Response(body = "!")

        return web.Response(body = ",".join([p["d"] for p in parts]))

    except KeyError:
        return mkresp(400, {"message": "Missing required fields: HeadPosition + StudDifference."})

app.add_routes(routes)
