from flask import render_template,redirect, url_for, request, session
import uuid 
from welpurse.utils import login_required
from welpurse.routes import app_routes
import requests
from datetime import datetime, timedelta

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
    session['access_token_cookie']
    session['csrf_access_token'] 
    wami = "http://127.0.0.1:5001/auth/who_am_i"
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}
    req = requests.get(url=wami, headers=headers)
    if req.status_code == 200:
        member_id = req.json().get('id') # This will return the current user's ID
    else:
        user_id = None
        pass
        # Handle the case where there is no authenticated user
    css_file = 'index.css.jinja'  # The .jinja extension indicates that this is a Jinja2 template
    url = "http://127.0.0.1:5001/api/v1/welfares"
    res = requests.get(url=url)
    welfares = res.json()
    data = welfares.get('data')
    welfare_ids = []
    print(member_id)
    for welf in data:
        if welf.get('members'):
            welfare_ids.append(welf.get('id'))
            print(welf.get('id'))
    return render_template('index.html',
                           css_file=css_file,
                           cache_id=uuid.uuid4(),
                           welfares=welfares,
                           member_id=member_id,
                           welfare_ids=welfare_ids
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
    response = requests.get('http://127.0.0.1:5001/api/v1/events/')
    events = response.json()
    if response.status_code == 200:
      # Format the data for FullCalendar
      formatted_events = []
      for event in events:
          formatted_events.append({
              'id': event['id'],
              'title': event['title'],
              # 'start': datetime.strptime(event['start_date'], '%Y-%m-%dT%H:%M:%S.%f').isoformat(),
              # 'end': datetime.strptime(event['end_date'], '%Y-%m-%dT%H:%M:%S.%f').isoformat()
          })
    # Render the dashboard page if authenticated
    return render_template('dashboard.html',
                           events=formatted_events,
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
