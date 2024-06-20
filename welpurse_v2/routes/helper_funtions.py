import httpx
from asgiref.sync import async_to_sync
from os import getenv
from intasend import APIService
from intasend.exceptions import IntaSendBadRequest
import asyncio
import logging
from flask import flash
import requests
from datetime import datetime, timedelta, date

# Set up basic logging
logging.basicConfig(level=logging.INFO)

token = getenv("TOKEN")
publishable_key = getenv("PUBLISHABLE_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)


# FETCH WALLEIT ID
def fetch_wallet_id(welfare_url, headers):
    async def fetch_welfare_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=welfare_url, headers=headers)
        return req

    req = async_to_sync(fetch_welfare_async)()
    if req.status_code == 200:
        welf = req.json().get("wallet")
        return welf if welf else None
    return None


# PROCESS PAYEMENTS
def process_payment(
    current_user, wallet, email, phone, amount, event_id, type_id, contr_type
):
    from welpurse_v2.payments import initiate_payment

    try:
        response = initiate_payment(service, wallet, email, phone, amount)
        invoice_id = response["invoice"]["invoice_id"]
        if invoice_id:
            try:
                final_state = wait_for_payment_completion(invoice_id)
                if final_state == "COMPLETE":
                    if update_database(
                        current_user,
                        wallet,
                        amount,
                        event_id,
                        type_id,
                        contr_type,
                    ):
                        # flash('Payment was successful!', 'success')
                        print("Payment has been processed successfully.")
                        return True
                elif final_state == "FAILED":
                    flash("Payment was unsuccessful!", "danger")
                    print("Payment has failed.")
                else:
                    print(f"Unexpected payment status: {final_state}")
            except Exception as e:
                logging.error(f"Exception in process_payment: {e}")
                raise e
        else:
            print("Invoice ID is None")
    except IntaSendBadRequest as e:
        logging.info("ERROR_INFO_KHALFAN  %s", e)
    return False


# WAITING TO COMPLETE PAYMENT
def wait_for_payment_completion(invoice_id):
    from welpurse_v2.payments import sync_wait_for_payment_completion

    task = sync_wait_for_payment_completion.apply_async(args=[invoice_id])
    retries = 0
    max_retries = 5

    while retries < max_retries:
        try:
            if task.ready():
                return task.get(
                    timeout=1
                )  # You can adjust the timeout as needed

            async_to_sync(asyncio.sleep)(2**retries)
        except Exception as e:
            logging.error(f"Exception in wait_for_payment_completion: {e}")
            raise e
        retries += 1

    raise TimeoutError("Payment processing timed out")


# UPDATE DATABASE' GROUPS WALLET
def update_database(
    current_user, wallet, amount, event_id, type_id, contr_type
):

    wt_url = "http://127.0.0.1:5001/api/v1/transactions/"
    wallet_id = wallet.get("id")
    wallet_transactions = {
        "wallet_id": wallet_id,
        "amount": amount,
        "transaction_type": "3",
        "date_transaction": datetime.now().date().isoformat(),
    }
    try:
        if not check_wallet_exists(wallet_id):
            flash("Wallet ID does not exist. Operation failed!", "danger")
            return False
        wt_res = requests.post(wt_url, json=wallet_transactions)
        if wt_res.status_code != 201:
            return False
    except Exception as e:
        flash("Payment was unsuccessful! Please try again later", "danger")
        print("FAILED", e)
        return False

    trans_type_url = "http://127.0.0.1:5001/api/v1/transactions_ttype/"
    transaction_transaction_type = {
        "transaction_id": wt_res.json().get("id"),
        "type_id": type_id,
    }
    try:
        trans_type_res = requests.post(
            trans_type_url, json=transaction_transaction_type
        )
        if trans_type_res.status_code != 201:
            flash(
                "Payment was unsuccessful! - transaction, try again", "danger"
            )
            return False
    except Exception as e:
        flash("Payment was unsuccessful!", "danger")
        return False
    contr_url = "http://127.0.0.1:5001/api/v1/contributions/"
    contribution = {
        "member_id": current_user.get("id"),
        "amount": amount,
        "contribution_type": contr_type,
        "event_id": event_id,
        "date_contributed": datetime.now().date().isoformat(),
    }
    try:
        contr_res = requests.post(contr_url, json=contribution)
        print(contr_res)
        if contr_res.status_code != 201:
            flash("Payment was unsuccessful-contr!, try again", "danger")
            return False
    except Exception as e:
        flash("Payment was unsuccessful!, try again", "danger")
        return False

    return True


# CHECK IF WALLET EXIST
def check_wallet_exists(wallet_id):
    wallet_url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
    try:
        res = requests.get(wallet_url)
        return res.status_code == 200
    except Exception as e:
        print("Error checking wallet existence:", e)
        return False


# FETCH AN EVENT
async def fetch_an_event(headers, event_id):
    url = f"http://127.0.0.1:5001/api/v1/events/{event_id}"
    async with httpx.AsyncClient() as client:
        req = await client.get(url=url, headers=headers)
    return req.json() if req.status_code == 200 else {}


# FETCH INTASENDS WALLET CORRESPONDING TO DATABASE
async def fetch_intasend_wallet(headers, wallet_id, timeout=60.0):
    url = f"http://127.0.0.1:5001/api/v1/wallet/{wallet_id}"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
    except httpx.TimeoutException:
        print("The request timed out.")
    return None


async def fetch_wallet(headers, wallet_id):
    url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
    async with httpx.AsyncClient() as client:
        req = await client.get(url=url, headers=headers)
    return req.json() if req.status_code == 200 else {}


async def update_wallet(headers, wallet_id, wallet, timeout=60.0):
    url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.put(url, headers=headers, json=wallet)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
    except httpx.TimeoutException:
        print("The request timed out.")
    return None


# async def fetch_intasend_wallet(headers, wallet_id):
#     url = f"http://127.0.0.1:5001/api/v1/wallet/{wallet_id}"
#     async with httpx.AsyncClient() as client:
#         req = await client.get(url=url, headers=headers)
#     return req.json() if req.status_code == 200 else {}

# async def fetch_wallet(headers, wallet_id):
#     url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
#     async with httpx.AsyncClient() as client:
#         req = await client.get(url=url, headers=headers)
#     return req.json() if req.status_code == 200 else {}

# async def update_wallet(headers, wallet_id, data):
#     url = f"http://127.0.0.1:5001/api/v1/wallets/{wallet_id}"
#     async with httpx.AsyncClient() as client:
#         req = await client.put(url=url, headers=headers, json=data)
#     return req.json() if req.status_code == 200 else {}


async def async_events_view(welfare_id, event_id, headers):
    welfare_url = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"
    try:
        async with httpx.AsyncClient() as client:
            welfare_res = await client.get(welfare_url, headers=headers)
            if welfare_res.status_code == 200:
                welfare = welfare_res.json()
                wallet_id = welfare.get("wallet", {}).get("wallet_id")
                wal_id = welfare.get("wallet", {}).get("id")
                if not wallet_id:
                    return {"error": "Wallet ID not found"}
                event = await fetch_an_event(headers, event_id)
                if not event:
                    return {"error": "Event not found"}
                data_wallet = await fetch_intasend_wallet(headers, wallet_id)
                if not data_wallet:
                    return {"error": "IntaSend Wallet not found"}
                updated_wallet = await update_wallet(
                    headers, wal_id, data_wallet
                )
                if not updated_wallet:
                    return {"error": "Unable to update wallet"}
                return {
                    "welfare": welfare,
                    "event": event,
                    "updated_wallet": updated_wallet,
                }
            else:
                return {"error": "Unable to fetch welfare details"}
    except Exception as e:
        return {"error": str(e)}


# FETCH EVENTS


def fetch_events(headers):
    url = "http://127.0.0.1:5001/api/v1/events/"

    async def fetch_events_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_events_async)()
    return req.json() if req.status_code == 200 else {}


# FETCH MEMBERS
def fetch_members(headers):
    url = "http://127.0.0.1:5001/api/v1/members/"

    async def fetch_members_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_members_async)()
    return req.json() if req.status_code == 200 else {}


def fetch_a_member(headers, member_id):
    url = f"http://127.0.0.1:5001/api/v1/members/{member_id}"

    async def fetch_welfare_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_welfare_async)()
    return req.json() if req.status_code == 200 else {}


# FETCH WELFARE
def fetch_welfares(headers):
    url = "http://127.0.0.1:5001/api/v1/welfares/"

    async def fetch_welfares_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_welfares_async)()
    return req.json() if req.status_code == 200 else {}


def fetch_a_welfare(headers, welfare_id):
    url = f"http://127.0.0.1:5001/api/v1/welfares/{welfare_id}"

    async def fetch_welfare_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_welfare_async)()
    return req.json() if req.status_code == 200 else {}


# FETCH DONATION
def start_donation(headers, request_id):
    url = f"http://127.0.0.1:5001/api/v1/donation-requests/{request_id}/start"
    res = requests.put(url=url, headers=headers)
    print(res.json())
    if res.status_code == 200:
        return True
    else:
        return False


# FETCH DONATION
def join_group(headers, data):
    url = f"http://127.0.0.1:5001/api/v1/join_group"
    res = requests.post(url=url, headers=headers, json=data)
    if res.status_code == 200:
        return True
    else:
        return False


# ADD ROLE TO MEMBER
def add_role(headers, member_id, role_id):
    url = f"http://127.0.0.1:5001/api/v1/members/{member_id}/roles/{role_id}"
    res = requests.post(url=url, headers=headers)
    if res.status_code == 200:
        return True
    else:
        return False


def fetch_a_role(headers, role_id):
    url = f"http://127.0.0.1:5001/api/v1/roles/{role_id}"

    async def fetch_role_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_role_async)()
    return req.json() if req.status_code == 200 else {}


def fetch_roles(headers):
    url = f"http://127.0.0.1:5001/api/v1/roles/"

    async def fetch_roles_async():
        async with httpx.AsyncClient() as client:
            req = await client.get(url=url, headers=headers)
        return req

    req = async_to_sync(fetch_roles_async)()
    return req.json() if req.status_code == 200 else {}
