import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st
import os

st.title("🍷 Wine Reviews Analysis")

# Function to load data (try local CSV first, fallback to Kaggle path)
@st.cache_data
def load_data():
    local_file = "winemag-data_first150k.csv"
    kaggle_path = os.path.expanduser(
        "~/.cache/kagglehub/datasets/zynicide/wine-reviews/versions/4/winemag-data_first150k.csv"
    )
    if os.path.exists(local_file):
        return pd.read_csv(local_file)
    elif os.path.exists(kaggle_path):
        return pd.read_csv(kaggle_path, low_memory=False)
    else:
        st.error("❌ Dataset not found. Please ensure the CSV is available.")
        return pd.DataFrame()

# Load dataset
df = load_data()

if not df.empty:
    st.success(f"✅ Loaded dataset with {df.shape[0]:,} rows and {df.shape[1]} columns")

    # Show a preview
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # Country distribution
    st.subheader("🌍 Top 10 Countries by Number of Reviews")
    top_countries = df["country"].value_counts().head(10)
    st.bar_chart(top_countries)

    # Average points by country
    st.subheader("🏅 Average Points by Country (Top 10)")
    avg_points = df.groupby("country")["points"].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_points)

    # WordCloud of wine descriptions
    st.subheader("☁️ WordCloud of Wine Descriptions")
    text = " ".join(df["description"].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
