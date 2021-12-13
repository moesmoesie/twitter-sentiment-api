import requests
import os
from models.keyword import Keyword
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
HEADER = {
    "Authorization": f"Bearer {os.environ['TWITTER_BEARER_TOKEN']}"
}



class TwitterAPI():

    def check_connection(self):
        """Checks if a connection can be made with the twitter api."""
        response = requests.get(SEARCH_URL, headers=HEADER)
        return response.status_code == 200

    def create_params(self,keyword_groups: list[list[Keyword]],next_token):
        query_params = {
            "tweet.fields" : "created_at,public_metrics,entities,author_id",
            "max_results": 100 if os.environ.get('IS_PRODUCTION',"TRUE") == "TRUE" else 20,
        }

        if next_token:
            query_params["next_token"] = next_token
        
        query = ""

        for index,group in enumerate(keyword_groups):
            if index > 0 and index != len(keyword_groups):
                query += " OR "
            query += "("
            for index,keyword in enumerate(group):
                if index == 0:
                    query += "-is:retweet "
                query += keyword.get_processed_value()
                if index < len(group) - 1:
                    query += " "
            query += ")"

        query_params["query"] = query
        return query_params

    def get_user_data(self,ids):
        amount = len(ids)
        current = 0
        data  = []
        while True:
            if current >= amount:
                break;

            url = f"https://api.twitter.com/2/users?ids={','.join(ids[current:current + 100])}&user.fields=profile_image_url,verified"
            current += 100
            response = requests.get(url, headers=HEADER)
            data.extend(response.json()["data"])
        return data


    def search(self, keywords : list[list[Keyword]]):
        data = []
        next_token = None
        while True:
            if len(data) >= 250:
                break;
                
            query_params = self.create_params(keywords, next_token)
            response = requests.get(SEARCH_URL, headers=HEADER,params=query_params)

            if response.status_code != 200:
                raise Exception(response.status_code, response.text)

            json_data = response.json()

            if "data" not in json_data:
                break;

            data.extend(response.json()["data"])

            meta = json_data["meta"]

            if "next_token" not in meta:
                break;

            next_token = meta["next_token"]

        df = pd.DataFrame(data)

        user_data = pd.DataFrame(self.get_user_data(df["author_id"].tolist()))
        df["name"] = user_data["name"]
        df["username"] = user_data["username"]
        df["verified"] = user_data["verified"]
        df["profile_image_url"] = user_data["profile_image_url"]

        df = df.fillna(
            {
                'name':'.', 
                'username':'.',
                'verified': False,
                'profile_image_url': 'none'
            }
        ).fillna(0)

        print(df.describe())

        return df