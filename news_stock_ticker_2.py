import streamlit as st
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt

# ----------------------------
# 🔑 Set your NewsAPI key here
# Or use Streamlit secrets if deploying securely
NEWS_API_KEY = "4147de8227744a4e80ec3c7cb194ff5d"
# ----------------------------

# 📥 Fetch headlines from NewsAPI
@st.cache_data(show_spinner=False)
def fetch_news_headlines(query):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to fetch news: {e}")
        return []

    data = response.json()
    articles = data.get("articles", [])
    return [article["title"] for article in articles]

# 🧠 Analyze sentiment using TextBlob
def analyze_sentiment(headlines):
    positive = []
    negative = []

    for headline in headlines:
        polarity = TextBlob(headline).sentiment.polarity
        if polarity >= 0.1:
            positive.append(headline)
        else:
            negative.append(headline)
    return positive, negative

# 📊 Plot sentiment results
def plot_sentiment_chart(positive, negative):
    fig, ax = plt.subplots()
    ax.bar(["Positive", "Negative"], [len(positive), len(negative)])
    ax.set_ylabel("Number of Headlines")
    ax.set_title("News Sentiment")
    st.pyplot(fig)

# 🚀 Streamlit UI
st.set_page_config(page_title="Stock News Sentiment", page_icon="📰")
st.title("📰 Stock News Sentiment Analyzer")

ticker = st.text_input("Enter company name or stock ticker (e.g., AAPL, Tesla):")

if ticker:
    with st.spinner("Fetching news and analyzing sentiment..."):
        headlines = fetch_news_headlines(ticker)

        if headlines:
            positive, negative = analyze_sentiment(headlines)
            plot_sentiment_chart(positive, negative)

            st.subheader("✅ Positive Headlines")
            for h in positive:
                st.success(h)

            st.subheader("❌ Negative Headlines")
            for h in negative:
                st.error(h)
        else:
            st.warning("No headlines found.")