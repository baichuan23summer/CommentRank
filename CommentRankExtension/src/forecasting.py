from modelling import *
import pandas as pd

def forecast_helpfulness():
    df=pd.read_csv('RealTimeAmazonCommentCSVfile')
    df["helpfulness_index"]=df["reviewText"].apply(predict_helpfulness)
    df.to_csv('CommentRankExtension/data/amazon_reviews_with_predicted_helpfulness.csv', index=False)

if __name__ == "__main__":
    forecast_helpfulness()