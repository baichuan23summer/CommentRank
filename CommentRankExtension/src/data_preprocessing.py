import pandas as pd

df = pd.read_csv('CommentRankExtension/data/amazon_reviews.csv')

# compute helpfulness index: yes - no / total
def calculate_helpfulness_index(row):
    total_votes = row['total_vote']
    if total_votes == 0:
        return 0
    else:
        return (row['helpful_yes'] - row['helpful_no']) / total_votes

df['helpfulness_index'] = df.apply(calculate_helpfulness_index, axis=1)


df_rated = df[df['helpful_yes'] + df['helpful_no'] > 0].copy()
# find unrated data and get ready to preprocess it
df_unrated = df[df['helpful_yes'] + df['helpful_no'] == 0].copy()



import nltk
import string
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# generalize text and tokenize them
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)

# sepatate the rated text and unrated text, preprocess them
df_rated['clean_text'] = df_rated['reviewText'].astype(str).apply(preprocess_text)
df_unrated['clean_text'] = df_unrated['reviewText'].astype(str).apply(preprocess_text)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# vectorize all text
vectorizer = TfidfVectorizer()
all_text = pd.concat([df_rated['clean_text'], df_unrated['clean_text']])
tfidf_matrix_all = vectorizer.fit_transform(all_text)
tfidf_matrix_rated = tfidf_matrix_all[:len(df_rated)]
tfidf_matrix_unrated = tfidf_matrix_all[len(df_rated):]

# compute the similarity of a unrated text with a rated text
similarity_matrix = cosine_similarity(tfidf_matrix_unrated, tfidf_matrix_rated)


import numpy as np

# for each untrated text, assign it with helpfulness_index of the most similar one
best_match_indices = np.argmax(similarity_matrix, axis=1)
matched_helpfulness_index = df_rated['helpfulness_index'].values[best_match_indices]
df_unrated['helpfulness_index'] = matched_helpfulness_index

df_updated = pd.concat([df_rated, df_unrated], ignore_index=True)
df_updated.to_csv('amazon_reviews_with_helpfulness.csv', index=False)
