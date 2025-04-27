from transformers import BertTokenizer, BertModel
import torch
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib


def get_bert_embedding(text):
    # 加载 BERT 预训练模型
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # 提取 [CLS] token 的向量作为文本的特征表示
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # shape: (768,)


def train_model():
    df=pd.read_csv('CommentRankExtension/data/amazon_reviews_with_helpfulness.csv')
    all_reviews=df['reviewText'].astype(str)
    helpfulness_index=df['helpfulness_index']

    # 生成所有评论的 BERT 向量
    X = np.array([get_bert_embedding(text) for text in all_reviews])  # (4000, 768)
    y = np.array(helpfulness_index)  # (4000,)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练 XGBoost 回归模型
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # 评估模型
    y_pred = model.predict(X_test)
    from sklearn.metrics import mean_squared_error
    print("MSE:", mean_squared_error(y_test, y_pred))

    # 保存训练好的模型
    joblib.dump(model, "helpfulness_xgb_model.pkl")
    print("模型已保存！")



def predict_helpfulness(new_review):
    # 加载模型
    model = joblib.load("helpfulness_xgb_model.pkl")
    # 1. 用 BERT 生成特征向量
    feature_vector = get_bert_embedding(new_review).reshape(1, -1)  # (1, 768)

    # 2. 用 XGBoost 预测 helpfulness index
    predicted_helpfulness = model.predict(feature_vector)[0]
    
    return f"{predicted_helpfulness:.4f}"


