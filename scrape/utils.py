from dotenv import load_dotenv
import requests
import os

# Load env variables
load_dotenv()

BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

def connect_to_endpoint(url, params):
    res = requests.get(url, auth=bearer_oauth, params=params)
    if res.status_code != 200:
        raise Exception(res.status_code, res.text)
    return res.json()

def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return r
