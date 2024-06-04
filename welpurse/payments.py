from flask import jsonify, current_app
from welpurse.routes import app_routes
from os import getenv
from intasend import APIService
import asyncio
from welpurse.celery_worker import celery

token = getenv("TOKEN")
publishable_key = getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)

def get_celery():
    return current_app.extensions['celery']

@app_routes.route('/check_status/<task_id>', methods=['GET'])
async def check_status(task_id):
    celery = get_celery()
    task = celery.AsyncResult(task_id)
    if task.state == 'PROGRESS':
        return jsonify({'state': task.info.get('current', 'UNKNOWN')})
    elif task.state == 'SUCCESS':
        final_state = task.result
        return jsonify({'state': final_state})
    else:
        return jsonify({'state': task.state})

# Function to initiate the payment
def initiate_payment(service, wallet, email, phone, amount):
    wallet_id = wallet.get('wallet_id')
    response = service.wallets.fund(
        wallet_id=wallet_id,
        email=email,
        phone_number=phone,
        amount=amount,
        currency="KES",
        narrative="Deposit",
        mode="MPESA-STK-PUSH"
    )
    return response

# Function to check the payment status
def check_payment_status(invoice_id):
    response = service.collect.status(invoice_id=invoice_id)
    return response

# Synchronous Celery task wrapper for async work
@celery.task(bind=True)
def sync_wait_for_payment_completion(self, invoice_id):
    return asyncio.run(wait_for_payment_completion(self, invoice_id))

# Asynchronous function to wait for the payment to complete
async def wait_for_payment_completion(self, invoice_id):
    while True:
        payment_status = check_payment_status(invoice_id)
        state = payment_status['invoice']['state']
        if state == 'COMPLETE':
            return state
        elif state == 'FAILED':
            return state
        else:
            self.update_state(state='PROGRESS', meta={'current': state})
        await asyncio.sleep(5)  # Reduce sleep time for faster checks
