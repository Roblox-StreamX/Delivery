# Copyright 2022 StreamX Developers

# Modules
import json
import falcon
import logging
from src import app
from secrets import token_hex
from datetime import datetime, timezone

from .webhook import upload_info

# Initialization
log = logging.getLogger("rich")

# API key handlers
def validate_key(key: str) -> bool:
    if not key.strip():
        return False

    user = app.payment["data"].find_one({"apikeys": {"key": key, "reason": None}})
    if user is None:
        return False

    return user["quota"] > 0

# Routing
class Index:
    def on_get(self, req, resp) -> None:
        resp.text = """This is a StreamX Production Server.
        You can GET /dogwithabanana to see a dog with a banana.

        You can also use /init, /upload, and /download like normal people.

        NOTICE:
        StreamX developers are not responsible for your plastic USB drives melting.
        Nor are we responsible for any depression, anxiety, or overall sadness StreamX may cause you."""

class DogWithABanana:
    def on_get(self, req, resp) -> None:
        raise falcon.HTTPFound("https://www.youtube.com/watch?v=21HNPnjjcZE")

    def on_post(self, req, resp) -> None:
        resp.text = "https://www.youtube.com/watch?v=21HNPnjjcZE"

class Initialize:
    def on_post(self, req, resp) -> None:
        apikey = req.get_header("X-StreamX-Key", True, "")
        if not validate_key(apikey):
            raise falcon.HTTPUnauthorized(title = "401", description = "Invalid API key.")

        placeid, placever = req.get_header("X-StreamX-PlaceID", True, ""), req.get_header("X-StreamX-PlaceVer", True, "")

        # Check if game is whitelisted
        user = app.payment["data"].find_one({"whitelist": placeid, "apikeys": {"key": apikey, "reason": None}})
        if user is None:
            upload_info(401, apikey, None, placeid, placever, "Game not whitelisted")
            raise falcon.HTTPUnauthorized(title = "401", description = "You do not have access to this game.")

        # Reduce user's quota
        dt = datetime.now(timezone.utc).strftime("%D")
        if dt != user["lastusage"]:
            app.payment["data"].update_one({"userid": user["userid"]}, {"$set": {"quota": user["quota"] - 1}})
            app.payment["data"].update_one({"userid": user["userid"]}, {"$set": {"lastusage": dt}})

        # Generate storage key
        storagekey = f"{placeid}{placever}"
        authkey, upload = app.mongo.keys.find_one({"storagekey": storagekey}), False
        if authkey is None:
            authkey, upload = token_hex(16), True
            app.mongo.keys.insert_one({"storagekey": storagekey, "authkey": authkey, "apikey": apikey})

        else:
            if apikey != authkey["apikey"]:
                upload_info(401, apikey, storagekey, placeid, placever, "API key does not match auth key's cached value")
                raise falcon.HTTPUnauthorized(title = "401", description = "API key missing permissions for requested game.")

            elif int(placever) == 0:
                app.mongo.parts[storagekey].drop()
                app.mongo.keys.delete_one({"authkey": authkey["authkey"]})
                authkey, upload = token_hex(16), True
                app.mongo.keys.insert_one({"storagekey": storagekey, "authkey": authkey, "apikey": apikey})

            else:
                authkey = authkey["authkey"]

        return {"key": authkey, "upload": upload}

class Upload:
    def on_post(self, req, resp) -> None:
        authkey = req.get_header("X-StreamX-Auth", True, "")
        if len(authkey) > 32:  # This is just sanitization for MongoDB
            raise falcon.HTTPBadRequest(title = "Invalid authentication key", description = "Authentication keys are at most 32 characters long.")

        kdata = app.mongo.keys.find_one({"authkey": authkey})
        if kdata is None:
            raise falcon.HTTPUnauthorized(title = "Invalid authentication key", description = "The authentication key you provided is invalid.")

        # Fetch part data
        try:
            tb = []
            for part in (req.stream.read()).decode("utf8").split(","):
                x, y, z, d = part.split(":")
                tb.append({"x": float(x), "y": float(y), "z": float(z), "d": d})

            app.mongo.parts[kdata["storagekey"]].insert_many(tb)
            return {"message": "OK"}

        except Exception:
            raise falcon.HTTPBadRequest(title = "Invalid request", description = "The server could not understand the provided part information.")

class Download:
    def on_post(self, req, resp) -> None:
        authkey = req.get_header("X-StreamX-Auth", True, "")
        if len(authkey) > 32:  # This is just sanitization for MongoDB
            raise falcon.HTTPBadRequest(title = "Invalid authentication key", description = "Authentication keys are at most 32 characters long.")

        kdata = app.mongo.keys.find_one({"authkey": authkey})
        if kdata is None:
            raise falcon.HTTPUnauthorized(title = "Invalid authentication key", description = "The authentication key you provided is invalid.")

        # Load JSON
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest(title = "Empty request body", description = "A valid JSON document is required.")

        try:
            d = json.loads(body.decode("utf8"))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPBadRequest(title = "Malformed JSON", description = "StreamX was unable to decode the request body.")

        # Calculate head position
        try:
            (x, y, z), sd = d["HeadPosition"], d["StudDifference"]
            x, y, z = float(x), float(y), float(z)
            parts = list(app.mongo.parts[kdata["storagekey"]].find({
                "x": {"$lt": x + sd, "$gt": x - sd},
                "y": {"$lt": y + sd, "$gt": y - sd},
                "z": {"$lt": z + sd, "$gt": z - sd},
            }))
            resp.text = ",".join([p["d"] for p in parts]) if parts else "!"

        except KeyError:
            raise falcon.HTTPBadRequest(title = "Required fields missing", description = "A required field was missing from the request body.")

app.add_route("/", Index())
app.add_route("/dogwithabanana", DogWithABanana())
app.add_route("/init", Initialize())
app.add_route("/upload", Upload())
app.add_route("/download", Download())
