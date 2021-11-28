from flask import Flask
from twitter_api import TwitterAPI
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello_world():
    twitter_api = TwitterAPI()
    is_connected = twitter_api.check_connection()

    if is_connected:
        return "Twitter API is Connected"
    else:
        return "Twitter API is not Connected"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))