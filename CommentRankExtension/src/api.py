from flask import Flask, request, jsonify
from flask_cors import CORS
import scrape
import modelling

app = Flask(__name__)
CORS(app)

@app.route('/get-reviews', methods=['POST'])
def handle_reviews_request():
    try:
        # Acquire asin and cookies from the POST
        data = request.get_json()
        received_asin = data.get('asin', 'No ASIN received')
        cookies = {}
        # parse cookies
        ckies = request.get_json().get("cookieHeader")
        for i in ckies:
            name = i[0:str(i).find("=")]
            value = i[str(i).find("=")+1:]
            cookies[name] = value
        # print(cookies) 

        # scrape reviews using user's cookies on current product page
        reviewsJSON = scrape.fetch_reviews(received_asin, cookies)
        # print(reviewsJSON)

        if not reviewsJSON: 
            reviewsJSON = [{"title":"something", "comment": "this is not an bad idea", "rating": 5.0 },
                           {"title":"something", "comment": "this is not an good idea", "rating": 5.0 },
                           {"title":"something", "comment": "hope you have a wonderfulday", "rating": 5.0 }]
        
        # rank 
        body = []
        for review in reviewsJSON:
            content = review.get("comment")
            properties = {
                "review": content,
                "score": modelling.predict_helpfulness(content)
            }
            body.append(properties)
        sorted_body = sort_reviews_by_score(body)
        # print(sorted_body)

        return (jsonify({
            "message":"Ranked successfully!",
            "reviews": sorted_body
        }),200)

    except Exception as e:
        print(e)
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