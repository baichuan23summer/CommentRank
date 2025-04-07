# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import ranking_module

app = Flask(__name__)
CORS(app)

@app.route("/rank", methods=["POST"])
def rank_reviews():
    data = request.json
    reviews = data.get('reviews', [])
    ranked_reviews = ranking_module.rank_reviews(reviews)
    return jsonify(ranked_reviews)

if __name__ == "__main__":
    app.run(port=5000)