from utils import connect_to_endpoint
from dotenv import load_dotenv
from get_id import get_id
from botocore.exceptions import ClientError
import boto3
import requests
import shutil
import os
import time as t
import argparse

# Load env variables
load_dotenv()
USERNAME = os.environ.get("USERNAME")
MAX_IMAGES = int(os.environ.get("MAX_IMAGES"))
S3_BUCKET = os.environ.get("S3_BUCKET")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", type=int, default=MAX_IMAGES, help="max images to pull")
parser.add_argument("-u", default=USERNAME, help="twitter user to query")
parser.add_argument("-s", default=False, action="store_true", help="upload to s3")
parser.add_argument("-c", default=False, action="store_true", help="remove directory")
parser.add_argument("-f", help="folder name")
args = vars(parser.parse_args())

class Scraper:
    def __init__(self, args):
        self.max_images = args["m"]
        self.username = args["u"]
        self.upload_s3 = args["s"]
        self.cleanup = args["c"]
        self.id = get_id(self.username)
        self.folder = self.set_folder()
        self.bucket = S3_BUCKET
        self.counter = 0

    def set_folder(self):
        time_hash = str(t.time())[11:]
        return f"images_{time_hash}"

    def scrape(self):
        os.mkdir(self.folder)
        query_params = {
            "expansions": "attachments.media_keys",
            "media.fields": "url",
            "max_results": "100",
        }
        pagination_token = ""

        while self.counter <= self.max_images:
            if self.counter != 0:
                query_params["pagination_token"] = pagination_token

            search_url = f"https://api.twitter.com/2/users/{self.id}/tweets"
            json_response = connect_to_endpoint(search_url, query_params)
            image_urls = self.extract_urls(json_response)

            self.download_images(image_urls)
            pagination_token = json_response["meta"]["next_token"]

        print(f'All images successfully scraped from f{self.username}')

        if (self.upload_s3):
            self.upload_files()

        if (self.cleanup):
            self.cleanup_files()

    def download_images(self, image_urls):
        for url in image_urls:
            if (self.counter >= self.max_images+1):
                break
            res = requests.get(url)
            with open(f"{self.folder}/img_{self.counter}.png", "wb") as f:
                f.write(res.content)
            self.counter += 1
        print(f"{self.counter} images scraped")

    def extract_urls(self, json_response):
        valid_content = list(
            filter(lambda x: "url" in x, json_response["includes"]["media"])
        )
        return [x["url"] for x in valid_content]

    def upload_files(self):
        s3_client = boto3.client('s3')

        if(not self.bucket):
            print("Bucket not provided")
            return

        for root, dirs, files in os.walk(self.folder, topdown=False):
            for file in files:
                path = f'{root}/{file}'
                try:
                    res = s3_client.upload_file(path, self.bucket, path)
                except ClientError as e:
                    print(e)

        print(f"Upload to {self.bucket} complete")

    def cleanup_files(self):
        shutil.rmtree(self.folder)
        print(f"{self.folder} successfully removed")

if __name__ == "__main__":
    scraper = Scraper(args)
    scraper.scrape()
