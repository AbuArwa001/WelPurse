#!/usr/bin/python3
""" Run the app"""
import os
from welpurse import app

def launch():
    """App Launcher"""
    # Retrieve host and port from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True, debug=True)


if __name__ == "__main__":
    """ Main Function """
    launch()
