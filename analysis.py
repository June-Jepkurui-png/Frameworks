"""
Analysis and Cleaning Script for CORD-19 Metadata
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
df = pd.read_csv("data/metadata.csv")

# --- Cleaning ---
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))
df = df.dropna(subset=['title'])  # Drop rows without titles

# Save cleaned version
df.to_csv("data/cleaned_metadata.csv", index=False)
print("✅ Cleaned dataset saved to data/cleaned_metadata.csv")

# --- Visualizations ---
# Publications by Year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title("Publications by Year")
plt.xticks(rotation=45)
plt.savefig("data/publications_by_year.png")
plt.close()

# Top Journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(y=top_journals.index, x=top_journals.values)
plt.title("Top Journals Publishing COVID-19 Research")
plt.savefig("data/top_journals.png")
plt.close()

# Word Cloud
text = " ".join(df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("data/title_wordcloud.png")
plt.close()

print("📊 Visualizations saved in data/ folder")
