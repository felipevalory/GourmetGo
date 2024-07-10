import pandas as pd
import streamlit as st
from utilities import (clean_data, side_bar_config, country_by_rest,
                       cities_by_country, avg_rating_country,
                       price_for_two_by_country)

st.set_page_config(page_title='Countries', layout='wide')

st.header('🌎 Countries')

df = pd.read_csv('dataset/zomato.csv')

df1 = clean_data(df)

df1 = side_bar_config(df1)

with st.container():
    fig = country_by_rest(df1)
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

with st.container():
    fig = cities_by_country(df1)
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = avg_rating_country(df1)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    with col2:
        fig = price_for_two_by_country(df1)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')
