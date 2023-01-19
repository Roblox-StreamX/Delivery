# Copyright 2022 iiPython
# Copyright 2022 Crcoli737

# Modules
import os
import fastwsgi
from src import app

# Launch server
if __name__ == "__main__":
    fastwsgi.run(
        wsgi_app = app,
        host = os.getenv("SERVHOST", "0.0.0.0"),
        port = int(os.getenv("SERVPORT", 8080), 10),
    )
