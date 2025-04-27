from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from the extension

@app.route('/get-reviews', methods=['POST'])
def handle_reviews_request():
    try:
        data = request.get_json()
        received_asin = data.get('asin', 'No ASIN received')
        
        # Return test response with received ASIN
        return jsonify({
            "message": "ASIN received successfully!",
            "received_asin": received_asin,
            "test_reviews": [
                {
                    "review": f"Test review 1 for {received_asin}",
                    "score": 0.95
                },
                {
                    "review": f"Test review 2 for {received_asin}",
                    "score": 0.82
                }
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error processing request"
        }), 400

@app.route('/')
def home():
    return "Test API is running! Send POST requests to /get-reviews"

if __name__ == '__main__':
    app.run(debug=True, port=5000)