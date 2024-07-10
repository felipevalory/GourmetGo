import pandas as pd
import streamlit as st
from utilities import (clean_data, side_bar_cuisines_config, cuisine_max_rate,
                       top_10_best_rest, best_worst_cuisine)

st.set_page_config(page_title='Cuisines', layout='wide')

st.markdown('# 🍽️ Cuisines')

df = pd.read_csv('dataset/zomato.csv')

df1 = clean_data(df)

df1 = side_bar_cuisines_config(df1)

with st.container():
    st.markdown('## Top restaurants by cuisines')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('**Italian:**')
        cuisine_max_rate(df1, 'Italian')

    with col2:
        st.markdown('**American:**')
        cuisine_max_rate(df1, 'American')

    with col3:
        st.markdown('**Arabian:**')
        cuisine_max_rate(df1, 'Arabian')

    with col4:
        st.markdown('**Japanese:**')
        cuisine_max_rate(df1, 'Japanese')

    with col5:
        st.markdown('**Brazilian:**')
        cuisine_max_rate(df1, 'Brazilian')

with st.container():
    st.markdown('## Top 10 restaurants')
    dtf = top_10_best_rest(df1)
    st.dataframe(dtf)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = best_worst_cuisine(df1, False)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    with col2:
        fig = best_worst_cuisine(df1, True)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')
