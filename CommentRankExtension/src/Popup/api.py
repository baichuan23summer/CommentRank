# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import json
# import ranking_module

app = Flask(__name__)
CORS(app)

@app.route("/rank", methods=["GET", "POST"])
def rank_reviews():
    # data = request.get_json()
    # reviews = data.get('reviews', [])
    # ranked_reviews = ranking_module.rank_reviews(reviews)
    # print(data)
    # return jsonify(reviews)

    with open('amazon_reviews.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reviews = [row for row in reader]
        reviews = reviews[1:] # cut off the header row
    print(jsonify(reviews))
    return jsonify(reviews)

if __name__ == "__main__":
    app.run(port=5000)
    