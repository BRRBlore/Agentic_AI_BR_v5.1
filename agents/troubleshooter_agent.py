# agents/troubleshooter_agent.py

import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure correct path regardless of where Streamlit is run
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "tech_support_sample_QA.csv")

# Load the dataset
df = pd.read_csv(CSV_PATH)

# Vectorize the questions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["question"])

def handle(query):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, X)
    idx = similarity.argmax()
    return df.iloc[idx]["answer"]
