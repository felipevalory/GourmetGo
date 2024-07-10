import pandas as pd
import streamlit as st
from PIL import Image
from utilities import (clean_data, map_maker,
                       side_bar_config, format_number)

st.set_page_config(page_title='Main', layout='wide')

df = pd.read_csv('dataset/zomato.csv')

df1 = clean_data(df)

df1 = side_bar_config(df1)

image = Image.open('logo.png')
st.image(image, width=180)

st.write('# GourmetGo')
st.write('### The best place to find out your new fav restaurant!')
st.write("""---""")


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        restaurants = df1['Restaurant ID'].nunique()
        col1.metric('Restaurants', restaurants)
    with col2:
        countries = df1['Country Code'].nunique()
        col2.metric('Countries', countries)
    with col3:
        cities = df1['City'].nunique()
        col3.metric('Cities', cities)
    with col4:
        total_ratings = df1['Votes'].sum()
        total_ratings = format_number(total_ratings)
        col4.metric('Total Ratings', total_ratings)
    with col5:
        cuisine = len(df1.loc[:, 'Cuisines'].unique())
        col5.metric('Cuisines', cuisine)
with st.container():
    map_maker(df1)
