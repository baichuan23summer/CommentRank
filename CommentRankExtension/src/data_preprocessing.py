import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('CommentRankExtension/data/amazon_reviews.csv')

# 假设有三列分别表示：评论内容(review_text)、被标记“有用”的次数(helpful_count)，被标记“没用”的次数(not_helpful_count)。
# 如果你的文件中对应的列名不同，需在此处进行相应修改：
# df.rename(columns={"原列名A": "helpful_count", "原列名B": "not_helpful_count", ...}, inplace=True)

def calculate_helpfulness_index(row):
    total_votes = row['total_vote']
    if total_votes == 0:
        return 0
    else:
        return (row['helpful_yes'] - row['helpful_no']) / total_votes

df['helpfulness_index'] = df.apply(calculate_helpfulness_index, axis=1)


# 有评价评论（helpful_count + not_helpful_count > 0）
df_rated = df[df['helpful_yes'] + df['helpful_no'] > 0].copy()

# 无评价评论（helpful_count + not_helpful_count = 0）
df_unrated = df[df['helpful_yes'] + df['helpful_no'] == 0].copy()



import nltk
import string
from nltk.corpus import stopwords

# 如果是首次使用，需要额外下载 stopwords 和 punkt：
# nltk.download('punkt')
# nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # 转小写
    text = text.lower()
    # 去标点
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 分词
    tokens = nltk.word_tokenize(text)
    # 去停用词
    tokens = [w for w in tokens if w not in stop_words]
    # 重新拼成字符串
    return ' '.join(tokens)

# 对 df_rated 和 df_unrated 的文本做预处理
df_rated['clean_text'] = df_rated['reviewText'].astype(str).apply(preprocess_text)
df_unrated['clean_text'] = df_unrated['reviewText'].astype(str).apply(preprocess_text)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 将有评价评论和无评价评论的文本合并向量化
vectorizer = TfidfVectorizer()
# 注意这里我们只需要对所有文本做一次 fit_transform
all_text = pd.concat([df_rated['clean_text'], df_unrated['clean_text']])
tfidf_matrix_all = vectorizer.fit_transform(all_text)

# 切分向量化结果：前半部分是有评价的，后半部分是无评价的
tfidf_matrix_rated = tfidf_matrix_all[:len(df_rated)]
tfidf_matrix_unrated = tfidf_matrix_all[len(df_rated):]

# 计算无评价评论 与 有评价评论 之间的相似度矩阵
similarity_matrix = cosine_similarity(tfidf_matrix_unrated, tfidf_matrix_rated)


import numpy as np

# 对每个无评价评论，找到相似度最高的那条有评价评论的索引
best_match_indices = np.argmax(similarity_matrix, axis=1)

# 取出与之对应的 helpfulness_index
matched_helpfulness_index = df_rated['helpfulness_index'].values[best_match_indices]

# 将 matched_helpfulness_index 存回 df_unrated
df_unrated['helpfulness_index'] = matched_helpfulness_index

# df_rated 已经自带 helpfulness_index，不需要更新
# df_unrated 刚刚通过相似度找到了 helpfulness_index

# 合并
df_updated = pd.concat([df_rated, df_unrated], ignore_index=True)

# 按照原顺序排序（如果需要的话），或者直接保存
df_updated.to_csv('amazon_reviews_with_helpfulness.csv', index=False)
