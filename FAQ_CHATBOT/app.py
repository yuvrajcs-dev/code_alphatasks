import streamlit as st
import pandas as pd
import nltk
import string
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')   
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Page settings
st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for UI
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #4A90E2;
    }
    .sub-text {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #eaf3ff;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4A90E2;
        font-size: 18px;
        margin-top: 15px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)
# Title
st.markdown('<div class="main-title">🤖 FAQ Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Ask any question related to our services</div>', unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("faq_data_large (1).csv")

# Preprocessing function
def preprocess_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Process questions
df["processed_question"] = df["question"].apply(preprocess_text)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(df["processed_question"])

# Get answer
def get_answer(user_input):
    processed_input = preprocess_text(user_input)
    user_vector = vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, faq_vectors)
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score < 0.25:
        return "Sorry, I couldn't understand your question. Please try asking differently."

    return df.iloc[best_match_index]["answer"]

# Input box
user_question = st.text_input("Enter your question:")

# Button
if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        answer = get_answer(user_question)
        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("About Project")
st.sidebar.info(
    "This FAQ chatbot is built using Python, NLP, TF-IDF, Cosine Similarity, and Streamlit."
)

st.sidebar.title("Sample Questions")
st.sidebar.write("- How can I reset my password?")
st.sidebar.write("- Do you provide refunds?")
st.sidebar.write("- Can I cancel my order?")
st.sidebar.write("- How long does delivery take?")
