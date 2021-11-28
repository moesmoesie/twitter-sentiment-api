from flask import Flask
from twitter_api import TwitterAPI
import os
from models.keyword import Keyword

app = Flask(__name__)

@app.route("/")
def hello_world():
    twitter_api = TwitterAPI()

    data = {
        "keyword_groups": [
            [
                {"value" : "from:hugodejonge", "isNegated": False},
                {"value" : "replies", "isNegated": True},
            ]
        ]
    }

    keyword_groups = []
    for group in data["keyword_groups"]:
        keywords = []
        for keyword in group:
            keywords.append(Keyword(keyword["value"], keyword["isNegated"]))
        keyword_groups.append(keywords)

    data = twitter_api.search(keyword_groups)

    return data.to_json(orient="records",indent=2)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))