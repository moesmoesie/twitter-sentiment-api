import json
from flask import Flask
from twitter_api import TwitterAPI
import os
from models.keyword import Keyword
from flask import Flask, request, Response
from flask import Response
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

def analyse_sentiment(data_row):
    random_number = random.randint(1, 3)
    if random_number == 1:
        return "positief"
    elif random_number == 2:
        return "negatief"
    else:
        return "neutraal"

def analyse_hashtags(data_row):
    if not isinstance(data_row["entities"], dict):
        return []

    if "hashtags" not in data_row["entities"]:
        return []

    return list({hashtag["tag"] for hashtag in data_row["entities"]["hashtags"]})

def analyse_hashtag_count(df):
    hashtag_data = {}
    for index, row in df.iterrows():
        for hashtag in row["hashtags"]:
            if hashtag in hashtag_data:
                hashtag_data[hashtag] += 1
            else:
                hashtag_data[hashtag] = 1
    return hashtag_data
    
@app.route("/", methods=['POST'])
def hello_world():
    request_data = request.get_json()

    if "k_groups" not in request_data:
        return Response("k-groups not found in data!", status=400)

    k_groups = request_data["k_groups"]

    keywords_data = []
    for k_group in k_groups:
        keywords = []
        for keyword in k_group:
            if "value" in keyword:
                value = keyword["value"]
                isNegated = keyword.get("isNegated","false")
                keywords.append(Keyword(value,isNegated))
            else:
                return Response("Every keyword must have a value!", status=400)
        keywords_data.append(keywords)        

    twitter_api = TwitterAPI()
    data = twitter_api.search(keywords_data)
    
    data["sentiment"] = data.apply(analyse_sentiment, axis=1)
    data["hashtags"] = data.apply(analyse_hashtags, axis=1)

    sentiment_count = data.groupby(['sentiment']).size().to_dict()
    hashtag_count = analyse_hashtag_count(data)

    response = {
        "tweet_count": data.shape[0],
        "hashtag_count" : hashtag_count,
        "sentiment_count": sentiment_count,
        "tweets": data.to_dict(orient="records"),
    }

    return Response(json.dumps(response,indent=2), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))