import streamlit as st
import requests
from transformers import pipeline
import matplotlib.pyplot as plt

# Replace this with your actual NewsAPI key
NEWS_API_KEY = "4147de8227744a4e80ec3c7cb194ff5d"

@st.cache_data(show_spinner=False)
def fetch_news_headlines(query):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"❌ Failed to fetch news. Status code: {response.status_code}")
        st.code(response.text, language="json")
        return []

    data = response.json()
    articles = data.get("articles", [])
    return [article["title"] for article in articles]

@st.cache_resource
def get_classifier():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(headlines, classifier):
    sentiments = classifier(headlines)
    pos, neg = [], []

    for h, s in zip(headlines, sentiments):
        if s["label"] == "POSITIVE":
            pos.append(h)
        else:
            neg.append(h)
    return pos, neg

def plot_chart(positive, negative):
    fig, ax = plt.subplots()
    ax.bar(["Positive", "Negative"], [len(positive), len(negative)])
    ax.set_ylabel("Number of Headlines")
    ax.set_title("News Sentiment")
    st.pyplot(fig)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Stock News Sentiment", page_icon="📰")
st.title("📰 Stock News Sentiment Analyzer")

ticker = st.text_input("Enter company name or stock ticker (e.g., AAPL, Tesla):")

if ticker:
    with st.spinner("Fetching news and analyzing..."):
        headlines = fetch_news_headlines(ticker)
        if headlines:
            classifier = get_classifier()
            positive, negative = analyze_sentiment(headlines, classifier)

            plot_chart(positive, negative)

            st.subheader("✅ Positive Headlines")
            for h in positive:
                st.success(h)

            st.subheader("❌ Negative Headlines")
            for h in negative:
                st.error(h)
        else:
            st.warning("No headlines found.")