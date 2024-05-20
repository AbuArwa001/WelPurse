from flask import render_template
import uuid 
# from welpurse import calendar
from welpurse.routes import app_routes
from flask_jwt_extended import jwt_required

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
@app_routes.route('/', strict_slashes=False)
def home():
    """ Prints a Message when / is called """
    css_file = 'index.css.jinja'  # The .jinja extension indicates that this is a Jinja2 template
    return render_template('index.html',
                           css_file=css_file,
                           cache_id=uuid.uuid4()
                           )
# @app_routes.route('/login', strict_slashes=False)
# def login():
#     title = 'login'
#     return render_template('login.html',
#                            title=title,
#                            cache_id=uuid.uuid4())

@jwt_required()
@app_routes.route('/dashboard', strict_slashes=False)
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
