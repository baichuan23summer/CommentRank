from flask import Flask, request, jsonify
from flask_cors import CORS
import scrape
import modelling

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from the extension

@app.route('/get-reviews', methods=['POST'])
def handle_reviews_request():
    try:
        data = request.get_json()
        received_asin = data.get('asin', 'No ASIN received')

        cookies = {}
        ckies = request.get_json().get("cookieHeader")
        for i in ckies:
            name = i[0:str(i).find("=")]
            value = i[str(i).find("=")+1:]
            cookies[name] = value
        # print(cookies) 

        reviewsJSON = scrape.fetch_reviews(received_asin, cookies)
        # print(reviewsJSON)

        if not reviewsJSON: 
            reviewsJSON = [{"标题":"something", "评论内容": "this is not an bad idea", "评分": 5.0 },
                           {"标题":"something", "评论内容": "this is not an good idea", "评分": 5.0 },
                           {"标题":"something", "评论内容": "hope you have a wonderfulday", "评分": 5.0 }]
        
        body = []
        for review in reviewsJSON:
            content = review.get("评论内容")
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