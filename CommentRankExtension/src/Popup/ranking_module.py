# rank_module.py
import re
import numpy as np
from gensim.downloader import load

words_model = None  # Load once

def sentence_to_vector(sentence, model):
    words = sentence.split()
    vectors = [model[word] for word in words if word in model]
    return np.mean(vectors, axis=0) if vectors else np.zeros(300)

def txt_to_constants(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
    constants = [float(num) for num in re.findall(r'[-+]?[0-9]*\.?[0-9]+', line)]
    return np.array(constants)

def rank_reviews(reviews):
    global words_model
    if words_model is None:
        words_model = load("word2vec-google-news-300")
    
    file_path = "data.txt" 
    constants = txt_to_constants(file_path)
    ranked = []
    
    for review in reviews:
        sentence_vector = sentence_to_vector(review, words_model)
        score = np.dot(sentence_vector, constants)
        ranked.append({'review': review, 'score': score})
    
    # Sort by score descending
    ranked.sort(key=lambda x: x['score'])
    return ranked