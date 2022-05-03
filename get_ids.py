import requests
import os
import sys
import json

# Set environment variables
os.environ[
    "BEARER_TOKEN"
] = "AAAAAAAAAAAAAAAAAAAAABAlcAEAAAAAi%2FiM4VF9DTDLyUEcfBnDUq5zvso%3DMSUWJCqMuvV6H3dhiGPsfkqs05StBRwRFxDhED0jVpSjgSsA0q"

# Get environment variables
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/users/by"


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return r


query_params = {
    "usernames": sys.argv[1]
}

print(query_params)

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
