#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template
import os
import uuid

app = Flask(__name__)

calendar = [
  {
    "id": 1,
    "title": "Python Flask coding visual studio",
    "start_event": "2024-05-03T16:00:00",
    "end_event": "2024-05-04T03:00:00"
  },
  {
    "id": 2,
    "title": "PHP coding Notepad++",
    "start_event": "2024-05-08T03:17:15",
    "end_event": "2024-05-10T04:00:00"
  },
  {
    "id": 6,
    "title": "Basketball",
    "start_event": "2024-05-05T00:00:00",
    "end_event": "2024-05-05T14:30:00"
  },
  {
    "id": 7,
    "title": "Birthday Party",
    "start_event": "2024-05-12T00:00:00",
    "end_event": "2024-05-13T00:00:00"
  }
]

def css(css_file):
    return render_template(f'{css_file}.css.jinja'), 200, {'Content-Type': 'text/css'}

@app.route('/', strict_slashes=False)
def home():
    """ Prints a Message when / is called """
    css_file = 'index.css.jinja'  # The .jinja extension indicates that this is a Jinja2 template
    return render_template('index.html',
                           css_file=css_file,
                           cache_id=uuid.uuid4()
                           )

@app.route('/login', strict_slashes=False)
def login():
    title = 'login'
    return render_template('login.html',
                           title=title,
                           cache_id=uuid.uuid4())

@app.route('/dashboard', strict_slashes=False)
def dashboard():
    title = 'dashboard'
    amount_contributed = 70000
    target = 200000
    progress= (  amount_contributed  / target) * 100
    print(progress)
    return render_template('dashboard.html',
                           calendar = calendar,
                           title=title,
                           total=amount_contributed,
                           progress=progress,
                           cache_id=uuid.uuid4())

@app.route('/creategroup', strict_slashes=False)
def crete_group():
    title = 'Create Group'
    amount_contributed = 70000
    target = 200000
    progress= (  amount_contributed  / target) * 100
    print(progress)
    return render_template('creategroup.html',
                           calendar = calendar,
                           title=title,
                           total=amount_contributed,
                           progress=progress,
                           cache_id=uuid.uuid4())

def launch():
    """App Launcher"""
    # Retrieve host and port from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True, debug=True)


if __name__ == "__main__":
    """ Main Function """
    launch()
