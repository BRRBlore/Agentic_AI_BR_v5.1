# agents/troubleshooter_agent.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
CSV_PATH = "/content/drive/My Drive/AI_Agent_4/tech_support_sample_QA.csv"
df = pd.read_csv(CSV_PATH)

# Fit the TF-IDF vectorizer on the questions
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['question'])

def find_answer(user_input):
    input_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(input_vec, tfidf_matrix)
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score < 0.3:
        return "🤖 Sorry, I couldn’t find a close match. Can you please rephrase?"

    return f"💡 {df.iloc[best_match_index]['answer']}"
