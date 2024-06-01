#!/usr/bin/python3
from dotenv import load_dotenv
load_dotenv()
from welpurse import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
 