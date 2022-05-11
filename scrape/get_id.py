from utils import connect_to_endpoint
import argparse

# Set env variables
SEARCH_URL = "https://api.twitter.com/2/users/by"

def parse_response(res):
    try:
        return res["data"][0]["id"]
    except:
        print("Corrupted data object.")

def get_id(username):
    if not username:
        print('Please enter a username to query.')
    else:
        res = connect_to_endpoint(SEARCH_URL, {"usernames": username})
        return parse_response(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="twitter user to query")
    args = parser.parse_args()

    print(get_id(args.username))
