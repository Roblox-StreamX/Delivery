# Copyright 2022 iiPython

# Modules
import socket
from requests import post
from types import NoneType
from datetime import datetime, timezone

from .config import config

# Initialization
webhook_url = config.get("webhook_url")
webhook_enabled = webhook_url is not None

# Fetch server ID
server = socket.gethostname().split("-")[-1]

# Handlers
def upload_info(code: int, apikey: str, authkey: str | NoneType, placeid: str, placever: str, error: str) -> None:
    if not webhook_enabled:
        return

    date = datetime.now(timezone.utc).strftime("%D %H:%M UTC")
    post(webhook_url, json = {
        "embeds": [
            {
                "type": "rich",
                "title": f"StreamX {server} - Code {code}",
                "footer": {"text": f"Error code {code} generated at {date}"},
                "fields": [
                    {"name": "API Key", "value": apikey, "inline": False},
                    {"name": "Place ID", "value": placeid, "inline": True},
                    {"name": "Place Version", "value": placever, "inline": True},
                    {"name": "Error message", "value": error, "inline": False}
                ],
                "color": 0xDC3545
            }
        ]
    })
