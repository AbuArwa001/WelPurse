#!/usr/bin/env python3
from os import environ
from .app import create_app

app = create_app()

if __name__ == "__main__":
    host = environ.get('API_HOST', '0.0.0.0')
    port = environ.get('API_PORT', '5001')
    app.run(host=host, port=port, threaded=True)