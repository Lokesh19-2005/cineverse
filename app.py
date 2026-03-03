import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import LabelEncoder

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Cineverse", layout="wide")

# ---------------- PREMIUM MINIMAL CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #121212; }
.block-container { padding-top: 2rem; }

.hero {
    text-align:center;
    padding:50px 20px;
    border-radius:12px;
    background: linear-gradient(135deg,#1f1c2c,#928dab);
    color:white;
    margin-bottom:30px;
}

.movie-card {
    padding:20px;
    background:#1e1e1e;
    border-radius:12px;
    border:1px solid #2c2c2c;
    margin-bottom:20px;
    transition:0.3s ease;
    animation:fadeIn 0.6s ease-in-out;
}

.movie-card:hover {
    border:1px solid #ff4b2b;
    transform:translateY(-4px);
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

.stButton>button {
    background-color:#ff4b2b;
    color:white;
    border-radius:8px;
    border:none;
    padding:0.6em 1.5em;
    font-weight:500;
}

section[data-testid="stSidebar"] {
    background-color:#181818;
}

footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
data = pd.read_csv("movies_cleaned.csv")

# ---------------- SIMULATED DATA ----------------
platforms = ["Netflix", "Amazon Prime", "Disney+ Hotstar", "Hulu"]
languages = ["English", "Hindi", "Telugu", "Spanish", "French"]

data["platform"] = [random.choice(platforms) for _ in range(len(data))]
data["language"] = [random.choice(languages) for _ in range(len(data))]

# ---------------- ENCODE GENRE ----------------
le = LabelEncoder()
data["genre_encoded"] = le.fit_transform(data["genre"])

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <h1 style="font-size:48px;margin-bottom:10px;">🎬 CINEVERSE</h1>
    <p style="font-size:18px;color:#eeeeee;">
        AI-Powered Movie Recommendation Engine
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🎬 CINEVERSE")
st.sidebar.markdown("---")

selected_genre = st.sidebar.selectbox("Genre", le.classes_)
selected_language = st.sidebar.selectbox("Language", ["All"] + languages)
selected_platform = st.sidebar.selectbox("Platform", ["All"] + platforms)
min_imdb = st.sidebar.slider("Minimum IMDb Rating", 7.0, 9.5, 7.5)

# ---------------- TRENDING SECTION ----------------
st.subheader("🔥 Trending Now")

top_overall = data.sort_values(by="imdb", ascending=False).head(5)
cols_trending = st.columns(5)

for i, (_, row) in enumerate(top_overall.iterrows()):
    with cols_trending[i]:
        st.markdown(f"""
        <div class='movie-card'>
        <b>{row['title']}</b><br>
        ⭐ {row['imdb']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- RECOMMEND BUTTON ----------------
if st.button("🔥 Generate Recommendations"):

    filtered = data[data["genre"] == selected_genre]

    if selected_language != "All":
        filtered = filtered[filtered["language"] == selected_language]

    if selected_platform != "All":
        filtered = filtered[filtered["platform"] == selected_platform]

    if len(filtered) > 10:
        filtered = filtered[filtered["imdb"] >= min_imdb]

    if filtered.empty:
        st.warning("Not enough movies with strict filters. Showing best available.")
        filtered = data[data["genre"] == selected_genre]

    # Simple ranking instead of TensorFlow
    top_movies = filtered.sort_values(
        by="imdb",
        ascending=False
    ).head(10)

    st.subheader("🍿 Recommended For You")

    cols = st.columns(3)

    for idx, (_, row) in enumerate(top_movies.iterrows()):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class='movie-card'>
            <h4>{row['title']}</h4>
            <p>
            🌍 {row['language']} <br>
            📺 {row['platform']}
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(float(row["imdb"]) / 10)
            st.caption(f"IMDb Rating: {row['imdb']}")

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style='text-align:center;color:gray;font-size:14px;'>
Built with Deep Learning (Training Phase) • Streamlit Deployment
</div>
""", unsafe_allow_html=True)