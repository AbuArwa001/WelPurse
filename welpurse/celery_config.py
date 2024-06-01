
# welpurse/celery_config.py
from celery import Celery

def make_celery(app):
    # from welpurse.payments import async_wait_for_payment_completion 
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.conf.update(
        CELERY_IMPORTS=[
            'welpurse.payments'
        ]
    )
    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    app.extensions['celery'] = celery

    # from welpurse import payments

    return celery
