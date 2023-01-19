# Copyright 2022 iiPython

# Modules
import socket
from typing import Union
from requests import post
from datetime import datetime, timezone

from .config import config

# Initialization
webhook_url = config.get("webhook_url")
webhook_enabled = webhook_url is not None

# Fetch server ID
server = socket.gethostname().split("-")[-1]

# Handlers
def upload_info(code: int, apikey: str, authkey: Union[str, None], placeid: str, placever: str, error: str) -> None:
    if not webhook_enabled:
        print("Webhook error logging is disabled!")
        return

    date = datetime.now(timezone.utc).strftime("%D %H:%M UTC")
    post(webhook_url, json = {
        "embeds": [
            {
                "type": "rich",
                "title": f"StreamX {server} - Code {code}",
                "footer": {"text": f"Error code {code} generated at {date} | Powered by StreamX", "icon_url":"https://avatars.githubusercontent.com/u/117547018?s=400&u=de895b99c04ea6c7486938cbee0e424c91fc0db1&v=4"},
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
