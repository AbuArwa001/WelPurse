#welpurese/routes/main_routess.py
from flask import render_template,redirect, url_for
import uuid 
from welpurse.utils import login_required
from welpurse.routes import app_routes
from welpurse import jwt
from flask_jwt_extended import jwt_required, current_user, get_current_user
import requests

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
    url = "http://127.0.0.1:5001/api/v1/welfares"
    res = requests.get(url=url)
    welfares = res.json()
    return render_template('index.html',
                           css_file=css_file,
                           cache_id=uuid.uuid4(),
                           welfares=welfares
                           )
# @app_routes.route('/login', strict_slashes=False)
# def login():
#     title = 'login'
#     return render_template('login.html',
#                            title=title,
#                            cache_id=uuid.uuid4())

@app_routes.route('/dashboard', strict_slashes=False)
@login_required  # Use custom login_required decorator
def dashboard():
   
    title = 'dashboard'
    amount_contributed = 70000
    target = 200000
    progress = (amount_contributed / target) * 100

    # Render the dashboard page if authenticated
    return render_template('dashboard.html',
                           calendar=calendar,
                           title=title,
                           total=amount_contributed,
                           progress=progress,
                           cache_id=uuid.uuid4())
# # Custom error handler for JWT errors
# @jwt.unauthorized_loader
# def unauthorized_callback(callback):
#     # Redirect unauthorized users to the login page
#     return redirect(url_for('app_routes.login'))

# @jwt.expired_token_loader
# def expired_token_callback(jwt_header, jwt_payload):
#     # Redirect users with expired tokens to the login page
#     return redirect(url_for('app_routes.login'))

# @jwt.invalid_token_loader
# def invalid_token_callback(callback):
#     # Redirect users with invalid tokens to the login page
#     return redirect(url_for('app_routes.login'))

# Handle any other JWT errors
# @app.errorhandler(NoAuthorizationError)
# def handle_no_authorization_error(error):
#     return redirect(url_for('login'))
