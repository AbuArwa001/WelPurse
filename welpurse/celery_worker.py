from welpurse.app import create_app
from welpurse.celery_config import make_celery


app = create_app()
celery = make_celery(app)
