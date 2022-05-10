from dotenv import load_dotenv
import requests
import os
import sys
import json

# Load env variables
load_dotenv()

# Set env variables
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/users/by"

query_params = {
    "usernames": sys.argv[1]
}

def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == "__main__":
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
