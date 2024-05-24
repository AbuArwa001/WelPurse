#!/usr/bin/python3
from welpurse import create_app
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
import os 

app = create_app()

if __name__ == "__main__":
    app.run()

