import pandas as pd
import numpy as np
from gensim.downloader import load
from tqdm import tqdm

# Load pretrained Word2Vec model (Google News 300D)
print("Loading Word2Vec model...")
word_vectors = load("word2vec-google-news-300")

# Function to convert a sentence into a vector
def sentence_to_vector(sentence, model):
    words = sentence.split()
    vectors = [model[word] for word in words if word in model]
    return np.mean(vectors, axis=0) if vectors else np.zeros(300)  # 300D vector

# Read CSV file (assuming second column has text data)
input_csv = "input.csv"
output_csv = "output_vectors.csv"
df = pd.read_csv(input_csv)

# Convert sentences to vectors
tqdm.pandas()
vectors = df.iloc[:, 1].progress_apply(lambda text: sentence_to_vector(str(text), word_vectors))

# Convert list of vectors into a DataFrame
vector_df = pd.DataFrame(vectors.tolist(), columns=[f"dim_{i}" for i in range(300)])

# Save the vectors into a new CSV file without scientific notation
vector_df.to_csv(output_csv, index=False, float_format='%.6f')
print(f"Vectors saved to {output_csv}")