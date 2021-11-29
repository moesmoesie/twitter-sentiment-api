import json
from flask import Flask
from twitter_api import TwitterAPI
import os
from models.keyword import Keyword
from flask import Flask, request, Response
from flask import Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    response = {
        "tweet_count": data.shape[0],
        "tweets": data.to_dict(orient="records")
    }

    return Response(json.dumps(response,indent=2), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))