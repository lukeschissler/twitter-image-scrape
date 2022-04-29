import requests
import os

# Set environment variables
os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAABAlcAEAAAAAi%2FiM4VF9DTDLyUEcfBnDUq5zvso%3DMSUWJCqMuvV6H3dhiGPsfkqs05StBRwRFxDhED0jVpSjgSsA0q'

# Get environment variables
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

url = 'https://api.twitter.com/2/tweets/search/recent?query=from:twitterdev'
headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

r = requests.get(url, headers=headers)

print(r.text)