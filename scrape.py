import requests
import os
import time as t
import json
import hashlib

# Set environment variables
os.environ[
    "BEARER_TOKEN"
] = "AAAAAAAAAAAAAAAAAAAAABAlcAEAAAAAi%2FiM4VF9DTDLyUEcfBnDUq5zvso%3DMSUWJCqMuvV6H3dhiGPsfkqs05StBRwRFxDhED0jVpSjgSsA0q"

# Get environment variables
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/users/1870785781/tweets"
max_images = 2000

def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return r


query_params = {
    "expansions": "attachments.media_keys",
    "media.fields": "url",
    "max_results": "100",
}

def setup_env():
    time_hash = str(t.time())[11:]
    folder = f"images_{time_hash}"

    os.mkdir(folder)
    return folder


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def extract_urls(json_response):
    valid_content = list(
        filter(lambda x: "url" in x, json_response["includes"]["media"])
    )
    return [x["url"] for x in valid_content]

def download_images(image_urls, counter):
    for url in image_urls:
        res = requests.get(url)
        with open(f"{folder}/img_{counter}.png", "wb") as f:
            f.write(res.content)
        counter += 1


def main():
    pagination_token = ""
    counter = 0
    while counter <= max_images:
        folder = setup_env()
        if counter != 0:
            query_params["pagination_token"] = pagination_token

        json_response = connect_to_endpoint(search_url, query_params)
        image_urls = extract_urls(json_response)
        download_images(image_urls, counter)

        pagination_token = json_response["meta"]["next_token"]
        counter += len(image_urls)


if __name__ == "__main__":
    main()
