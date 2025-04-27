from flask import Flask, request, jsonify
from flask_cors import CORS
import scrape
import forecasting

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from the extension

@app.route('/get-reviews', methods=['POST'])
def handle_reviews_request():
    try:
        data = request.get_json()
        received_asin = data.get('asin', 'No ASIN received')
        
        reviewsJSON = scrape.fetch_reviews(received_asin)
        body = []
        for review in reviewsJSON:
            properties = {
                "review": review["评论内容"],
                "score" : forecasting.predict_helpfulness(review["评论内容"])
            }
            body.append(properties)
        sorted_body = sort_reviews_by_score(body)

        return (jsonify({
            "message":"Ranked successfully!",
            "reviews": sorted_body
        }),200)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error processing request"
        }), 400

@app.route('/')
def home():
    return "Test API is running! Send POST requests to /get-reviews"

def sort_reviews_by_score(reviews_list):
    return sorted(reviews_list, 
                 key=lambda x: x['score'], 
                 reverse=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)