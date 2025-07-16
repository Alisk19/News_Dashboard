import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Ali's News Dashboard", page_icon="📰", layout="wide")

st.markdown("<h1 style='text-align: center;'>Ali's News Dashboard</h1>", unsafe_allow_html=True)

# It's recommended to use st.secrets for API keys
api_key = "97b4e7e12b894adfbc1bdc91500fa67b"

# --- Advanced Search Filters ---
st.sidebar.header("Filter News")

query = st.sidebar.text_input("Search for a topic", "Technology")

# Date range selector
today = datetime.now()
last_month = today - timedelta(days=30)
date_range = st.sidebar.date_input(
    "Select a date range",
    (last_month, today),
    min_value=today - timedelta(days=60),
    max_value=today,
    format="YYYY-MM-DD"
)

# Language dropdown
languages = {"English": "en", "German": "de", "French": "fr", "Spanish": "es", "Italian": "it"}
lang_selection = st.sidebar.selectbox("Choose a language", options=list(languages.keys()))
language = languages[lang_selection]

# Sort by options
sort_by_options = {"Published At": "publishedAt", "Popularity": "popularity", "Relevancy": "relevancy"}
sort_selection = st.sidebar.selectbox("Sort by", options=list(sort_by_options.keys()))
sort_by = sort_by_options[sort_selection]


# --- Performance Boost with Caching ---
@st.cache_data
def get_news(query, from_date, to_date, language, sort_by):
    """Fetch news from NewsAPI and return JSON data."""
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"from={from_date.strftime('%Y-%m-%d')}&"
        f"to={to_date.strftime('%Y-%m-%d')}&"
        f"language={language}&"
        f"sortBy={sort_by}&"
        f"apiKey={api_key}"
    )
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching news: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

if st.sidebar.button("Get News"):
    if query and len(date_range) == 2:
        from_date, to_date = date_range
        data = get_news(query, from_date, to_date, language, sort_by)

        if data and data["status"] == "ok":
            articles = data.get("articles", [])
            if articles:
                st.subheader(f"Here are the top headlines for '{query}':")
                # --- Richer Article Display ---
                for article in articles:
                    with st.expander(f"**{article['title']}**"):
                        if article.get("urlToImage"):
                            st.image(article["urlToImage"], caption="Article Image")
                        st.write(article.get("description", "No description available."))
                        st.write(f"[Read more]({article['url']})")
            else:
                st.warning("No articles found for your query with the selected filters.")
        elif data:
            st.error(f"Error from API: {data.get('message', 'Unknown error')}")
    else:
        st.warning("Please enter a topic and select a valid date range.") 