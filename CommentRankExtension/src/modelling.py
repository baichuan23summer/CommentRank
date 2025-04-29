from transformers import BertTokenizer, BertModel
import torch
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib


# vectorize incoming text using bert
def get_bert_embedding(text):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # shape: (768,)


def train_model():
    df=pd.read_csv('CommentRankExtension/data/amazon_reviews_with_helpfulness.csv')
    all_reviews=df['reviewText'].astype(str)
    helpfulness_index=df['helpfulness_index']

    # vectorize texts and get its helpfulness_index prepared
    X = np.array([get_bert_embedding(text) for text in all_reviews])  # (4000, 768)
    y = np.array(helpfulness_index)  # (4000,)

    # training set with test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # Evaluating
    y_pred = model.predict(X_test)
    from sklearn.metrics import mean_squared_error
    print("MSE:", mean_squared_error(y_test, y_pred))

    # save the trained model
    joblib.dump(model, "../data/helpfulness_xgb_model.pkl")
    print("Model saved!")


# predict any text's helpfulness index with the trained model
def predict_helpfulness(new_review):
    model = joblib.load("../data/helpfulness_xgb_model.pkl")
    feature_vector = get_bert_embedding(new_review).reshape(1, -1)  # (1, 768)
    predicted_helpfulness = model.predict(feature_vector)[0]
    
    return f"{predicted_helpfulness:.4f}"


