# StreamX Streaming Engine

### Requirements

- A central MongoDB instance (preferably with authentication enabled)
    - If using auth, the user needs the `readWriteAnyDatabase` permission
- Launching system capable of sending environment variables
- All python requirements installed via `requirements.txt`
- Python interpreter of version **3.8 or greater**
    - For full support from us, please use Python 3.10 or greater
- A non-root user account to run the backend under
    - StreamX **can** run as root, but it's not recommended

### Installation

```
git clone https://github.com/Roblox-StreamX/Delivery
cd Delivery
python3 -m pip install -r requirements.txt
```

If you aren't using systemd and are launching manually via Python, ensure you pass `STREAMX_UPSTREAM` like so:
```sh
STREAMX_UPSTREAM=file python3 streamer.py
```

### Configuration via STREAMX_UPSTREAM

To ease configuration in multi-server setups, StreamX has a `STREAMX_UPSTREAM` environment variable which can set either to the IP and port  
of a [StreamX Configuration Server](https://github.com/Roblox-StreamX/Configuration) or set to `file` to load a local `config.json` file inside the StreamX folder.

To see the `config.json` format, please see [StreamX Configuration Server](https://github.com/Roblox-StreamX/Configuration).

### Launching

You can launch StreamX via `python3 streamer.py` for development, otherwise systemd or another init system is highly recommended.  
To run with systemd, create a `/lib/systemd/system/streamx.service`:
```
[Unit]
Description=StreamX Delivery Server
After=network-online.target
Wants=network-online.target

[Service]
User=streamx
Group=streamx

ExecStart=python3 /path/to/streamer.py
# If you downloaded the streamx binary (also uncomment it):
#ExecStart=/path/to/streamx

# This should be set to either the IP of your config server,
# or set to 'file' if you wish to use config.json instead
Environment="STREAMX_UPSTREAM=file"

# WorkingDirectory is only required if you use STREAMX_UPSTREAM=file
# Must be set to the parent folder of your ExecStart, in this example it would be
# /path/to, please adapt to whatever you're using.
WorkingDirectory=/home/streamx/Delivery

[Install]
WantedBy=multi-user.target
```
Then `sudo systemctl enable streamx && sudo systemctl start streamx`.
