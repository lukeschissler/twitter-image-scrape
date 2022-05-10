from dotenv import load_dotenv
import requests
import os
import time as t
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--id", help="twitter user to query")
args = parser.parse_args()

# Load env variables
load_dotenv()

# Set env variables
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

default_id = 1870785781
user_id = args.id if args.id else default_id
search_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
max_images = 2000

query_params = {
    "expansions": "attachments.media_keys",
    "media.fields": "url",
    "max_results": "100",
}


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return r


def setup_env():
    time_hash = str(t.time())[11:]
    folder = f"images_{time_hash}"

    os.mkdir(folder)
    return folder


def connect_to_endpoint(url, params):
    res = requests.get(url, auth=bearer_oauth, params=params)
    print(res.status_code)
    if res.status_code != 200:
        raise Exception(res.status_code, res.text)
    return res.json()


def extract_urls(json_response):
    valid_content = list(
        filter(lambda x: "url" in x, json_response["includes"]["media"])
    )
    return [x["url"] for x in valid_content]


def download_images(image_urls, counter, folder):
    for url in image_urls:
        res = requests.get(url)
        with open(f"{folder}/img_{counter}.png", "wb") as f:
            f.write(res.content)
        counter += 1


def main():
    pagination_token = ""
    counter = 0
    folder = setup_env()
    while counter <= max_images:
        if counter != 0:
            query_params["pagination_token"] = pagination_token

        json_response = connect_to_endpoint(search_url, query_params)
        image_urls = extract_urls(json_response)

        download_images(image_urls, counter, folder)

        pagination_token = json_response["meta"]["next_token"]
        counter += len(image_urls)


if __name__ == "__main__":
    main()
