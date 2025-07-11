import streamlit as st
import pickle
import pandas as pd
import requests
from time import sleep

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5e560991829e30cd4b660f0e518e79dc&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w185/" + poster_path
        else:
            return "https://via.placeholder.com/185x278?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/185x278?text=Error"

#def fetch_poster(movie_id):
    #response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5e560991829e30cd4b660f0e518e79dc&language=en-US'.format(movie_id))
    #data = response.json()
    #return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        sleep(0.3)
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Select a movie',
movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

