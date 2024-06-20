from welpurse_v2.app import create_app
from welpurse_v2.celery_config import make_celery


app = create_app()
celery = make_celery(app)
