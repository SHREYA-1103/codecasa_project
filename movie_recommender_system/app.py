import streamlit as st
import pickle as pk
import pandas as pd
import requests


movies_dict=pk.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pk.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=74fbcdfad0ca220861425c7302654917'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']  

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.title('Movie Recommender System')

selected_movie=st.selectbox(
    'Find similar movies',movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommend(selected_movie)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(posters[0])
        st.caption(names[0])
        
    with col2:
        st.image(posters[1])
        st.caption(names[1])
        
    with col3:
        st.image(posters[2])
        st.caption(names[2])
        
    with col4:
        st.image(posters[3])
        st.caption(names[3])
        
    with col5:
        st.image(posters[4])
        st.caption(names[4])
        
    
       