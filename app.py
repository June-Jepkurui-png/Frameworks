import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("metadata_cleaned.csv", low_memory=False)
    return df

df = load_data()

# -------------------------------
# App Layout
# -------------------------------
st.title("📊 CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

# Year filter
years = df['year'].dropna().unique()
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['year'].min()),
    int(df['year'].max()),
    (2019, 2021)
)

# Filter data
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# -------------------------------
# Show Data Sample
# -------------------------------
st.subheader("Sample of the Dataset")
st.write(filtered_df.head(10))

# -------------------------------
# Publications by Year
# -------------------------------
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis", ax=ax)
ax.set_title("Number of Publications per Year")
st.pyplot(fig)

# -------------------------------
# Top Journals
# -------------------------------
st.subheader("Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(y=top_journals.index, x=top_journals.values, palette="magma", ax=ax)
ax.set_title("Top 10 Journals Publishing COVID-19 Research")
st.pyplot(fig)

# -------------------------------
# Abstract Word Count Distribution
# -------------------------------
st.subheader("Abstract Word Count Distribution")
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(filtered_df['abstract_word_count'], bins=50, kde=True, ax=ax)
ax.set_title("Distribution of Abstract Word Counts")
st.pyplot(fig)
