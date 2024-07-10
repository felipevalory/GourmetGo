import pandas as pd
import streamlit as st
from utilities import (clean_data, side_bar_config, rest_by_city,
                       city_rest_rating, cuisine_per_city)

st.set_page_config(page_title='Cities', layout='wide')

st.markdown('# 🌆 Cities')

df = pd.read_csv('dataset/zomato.csv')

df1 = clean_data(df)

df1 = side_bar_config(df1)

with st.container():
    fig = rest_by_city(df1)
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = city_rest_rating(df1, 'best')
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    with col2:
        fig = city_rest_rating(df1, 'worst')
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

with st.container():
    fig = cuisine_per_city(df1)
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')
