# StreamX Streaming Engine

### Requirements

- A central MongoDB instance with authentication enabled
    - This user needs the `readWriteAnyDatabase` permission
- Launching system capable of sending environment variables
- All python requirements installed via `requirements.txt`
- Python interpreter of version 3.9 or greater
- A non-root user account to run the backend under

### Installation

```
git clone https://github.com/Roblox-StreamX/Delivery
cd Delivery
python3 -m pip install -r requirements.txt
```

If you aren't using systemd and are launching manually via Python, ensure you use a `.env` file in the current working directory.

### Configuration via STREAMX_UPSTREAM

To ease configuration in multi-server setups, StreamX has a `STREAMX_UPSTREAM` environment variable which can set either to the IP and port  
of a [StreamX Configuration Server](https://github.com/Roblox-StreamX/Configuration) or set to `file` to load a local `config.json` file inside the StreamX folder.

To see the `config.json` format, please see [StreamX Configuration Server](https://github.com/Roblox-StreamX/Configuration).

### Launching

Launch via `python3 streamer.py` to run with the inbuilt `.env` file, otherwise systemd or another init system is highly recommended.  
To run with systemd, create a `/lib/systemd/system/streamx.service`:
```
[Unit]
Description=StreamX Delivery Server
After=network-online.target
Wants=network-online.target

[Service]
User=streamx
Group=streamx
ExecStart=python3 streamer.py
WorkingDirectory=/home/streamx/Delivery
Environment="STREAMX_UPSTREAM=10.0.0.1:4070"

[Install]
WantedBy=multi-user.target
```
Then `sudo systemctl enable streamx && sudo systemctl start streamx`.
