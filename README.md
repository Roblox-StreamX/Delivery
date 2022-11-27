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

If not using systemd, and launching manually via Python, then setup a `.env` file:
```
MONGOUSER=MongoDB Username
MONGOPASS=MongoDB Password
MONGOHOST=192.168.0.x
MONGOPORT=27017
SERVHOST=0.0.0.0
SERVPORT=8080
PURCHASEIP="https://url-of-payment-server"
PURCHASEKEY="Payment Server API key"
```

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

[Install]
WantedBy=multi-user.target
```
Then `sudo systemctl enable streamx && sudo systemctl start streamx`.
