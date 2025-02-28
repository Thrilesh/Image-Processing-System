import requests


def trigger_webhook(request_id, status):
    # Replace with the user's webhook URL
    webhook_url = "https://user-webhook-url.com"
    payload = {"request_id": str(request_id), "status": status}
    requests.post(webhook_url, json=payload)
