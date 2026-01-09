from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import scrape_reviews  # Function to scrape reviews from a given URL
from model import load_models, classify_reviews  # Functions to load models and classify reviews
from preprocessing import preprocess_text  # Function for text preprocessing
import pandas as pd
import os

# Initialize Flask app

app = Flask(__name__)
CORS(app)   # ⭐ THIS LINE FIXES YOUR ERROR

# Load the pre-trained Word2Vec and SVM models
word2vec_model, svm_model = load_models()

@app.route('/')
def index():
    """
    Render the home page (index.html).
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    API endpoint to analyze reviews from a given product URL.
    - Scrapes reviews using `scrape_reviews()`.
    - Preprocesses reviews using `preprocess_text()`.
    - Classifies reviews using the trained SVM model.
    - Returns the analysis results as JSON.
    """
    data = request.json
    url = data.get('url')  # Extract the URL from the request
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400  # Return error if URL is missing
    
    reviews = scrape_reviews(url)  # Scrape reviews from the given URL
    if reviews.empty:
        return jsonify({"error": "No reviews found"}), 404  # Return error if no reviews found
    
    if "Review Text" not in reviews.columns or "Rating" not in reviews.columns:
        return jsonify({"error": "Invalid reviews format"}), 400  # Return error if data format is incorrect
    
    # Preprocessing reviews before classification
    preprocessed_reviews = []
    for i, review in enumerate(reviews["Review Text"]):
        review_text = preprocess_text(review)  # Clean and preprocess review text
        rating = reviews.iloc[i]["Rating"]  # Extract rating
        preprocessed_reviews.append({"Review Text": review_text, "Rating": rating})
    
    # Predict whether reviews are real or fake
    predictions = classify_reviews(preprocessed_reviews, word2vec_model, svm_model)
    
    # Create a DataFrame to store results
    df = pd.DataFrame({
        "Review": reviews["Review Text"],
        "Rating": reviews["Rating"],
        "Prediction": predictions
    })
    
    # Map predictions to human-readable labels
    df["Prediction"] = df["Prediction"].map({1: "Fake (Computer Generated)", 0: "Real (Original)"})
    
    # Convert DataFrame to dictionary format for JSON response
    result = df.to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    """
    Run the Flask application on the assigned port.
    Uses an environment variable for port if available (for deployment),
    otherwise defaults to port 5000.
    """
    # port = int(os.environ.get("PORT", 5000))  # Get the assigned port for deployment
    # app.run(host='0.0.0.0', port=port, debug=True)  # Run the Flask app
    app.run(debug=True)
