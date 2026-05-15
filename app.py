import streamlit as st
import pickle
import pandas as pd

# ------------------- Load Data -------------------
# Load similarity matrix
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Load movie dataframe
df = pd.read_csv('tmdbdf.csv')

# Keep only first 5000 movies (optional)
df = df.head(5000)

# Reset index to avoid out-of-bounds issues
df.reset_index(drop=True, inplace=True)

# ------------------- Custom CSS -------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
    }

    .movie-title {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        color: #ffffff;
        margin-top: 8px;
    }

    .stButton>button {
        background-color: #E50914;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #f40612;
        color: #ffffff;
    }

    div[data-baseweb="select"] > div {
        background-color: #1c1c1c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- Banner -------------------
st.image('image.jpg', use_container_width=True)

st.markdown(
    "<h1 style='text-align:center; color:white;'>Netflix Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

# ------------------- Movie Selection -------------------
movie = st.selectbox(
    'Select the Movie to Watch',
    df['title'].values
)

# ------------------- Recommendation Function -------------------
def recommend(movie):
    try:
        movie_index = df[df['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in dataset!")
        return [], []

    distances = similarity[movie_index]

    # Get top 5 similar movies
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        idx = i[0]

        # Avoid out-of-bounds
        if idx >= len(df):
            continue

        movie_row = df.iloc[idx]
        recommended_movies.append(movie_row['title'])

        poster = movie_row['poster_path']
        if pd.isna(poster):
            poster = "https://via.placeholder.com/300x450?text=No+Image"
        else:
            # Fetch original image for sharpness
            poster = "https://image.tmdb.org/t/p/original" + poster

        recommended_posters.append(poster)

    return recommended_posters, recommended_movies

# ------------------- Show Recommendations -------------------
if st.button('Click here for Getting Similar Movies'):
    posters, names = recommend(movie)

    if posters and names:
        cols = st.columns(5)

        for idx, col in enumerate(cols):
            if idx < len(names):
                with col:
                    # Smaller width for sharper image
                    st.image(posters[idx], width=120)
                    st.markdown(
                        f"<p class='movie-title'>{names[idx]}</p>",
                        unsafe_allow_html=True
                    )
    else:
        st.warning("No recommendations available for this movie.")