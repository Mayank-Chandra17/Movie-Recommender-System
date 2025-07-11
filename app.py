import streamlit as st
import pandas as pd
import pickle
import bz2
import requests

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=51783ab47d9f4f01ed1603a7a0d8b277".format(movie_id),timeout=10)

    
    data=response.json()
    poster_pa=data["poster_path"]
    return f"https://image.tmdb.org/t/p/w500{poster_pa}"


def recommend(movie):
    movie_index=movies[movies["title"]==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

    
st.title("Movie Recommender System")
movies_list=pickle.load(open("movies_dict.pkl","rb"))


with bz2.BZ2File("similarities3.pbz2", "rb") as ifile:
    similarity = pickle.load(ifile)

movies=pd.DataFrame(movies_list)
selected_movie=st.selectbox(
    "Select movie",
    movies["title"].values
)


if st.button("Recommend"):
    names,posters=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
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