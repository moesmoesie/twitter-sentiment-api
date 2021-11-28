import requests
import os

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent?query=from:TwitterDev"
HEADER = {
    "Authorization": f"Bearer {os.environ['TWITTER_BEARER_TOKEN']}"
}

class TwitterAPI():

    def check_connection(self):
        """Checks if a connection can be made with the twitter api."""
        response = requests.get(SEARCH_URL, headers=HEADER)
        return response.status_code == 200