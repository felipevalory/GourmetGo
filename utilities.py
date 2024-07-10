# Libraries

import folium
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image
import plotly.graph_objects as go
from folium.plugins import MarkerCluster


CUISINES = ['African', 'American', 'Andhra', 'Argentine', 'Armenian', 'Asian',
            'Asian Fusion', 'Assamese', 'Author', 'Awadhi', 'Bakery', 'Balti',
            'Bar Food', 'BBQ', 'Belgian', 'Bengali', 'Beverages', 'Biryani',
            'Brazilian', 'Breakfast', 'British', 'Burger', 'Burmese', 'Cafe',
            'Cafe Food', 'California', 'Canadian', 'Cantonese', 'Caribbean',
            'Cajun', 'Charcoal Chicken', 'Chettinad', 'Chinese', 'Coffee',
            'Coffee and Tea', 'Continental', 'Contemporary', 'Creole',
            'Crepes', 'Cuban', 'Deli', 'Desserts', 'Dimsum', 'Dim Sum',
            'Diner', 'Donuts', 'Drinks Only', 'Döner', 'Durban',
            'Eastern European', 'Egyptian', 'European', 'Fast Food',
            'Finger Food', 'Filipino', 'Fish and Chips', 'Fresh Fish',
            'French', 'Fusion', 'German', 'Giblets', 'Goan',
            'Gourmet Fast Food', 'Greek', 'Grill', 'Gujarati', 'Hawaiian',
            'Healthy Food', 'Home-made', 'Hyderabadi', 'Ice Cream', 'Indian',
            'Indonesian', 'International', 'Iranian', 'Irish', 'Italian',
            'Izgara', 'Japanese', 'Juices', 'Kebab', 'Kerala', 'Khaleeji',
            'Kiwi', 'Kokoreç', 'Korean', 'Korean BBQ', 'Kumpir',
            'Latin American', 'Lebanese', 'Lucknowi', 'Malaysian', 'Malwani',
            'Mandi', 'Mangalorean', 'Mediterranean', 'Mexican',
            'Middle Eastern', 'Mineira', 'Mithai', 'Modern Australian',
            'Modern Indian', 'Mongolian', 'Moroccan', 'Momos', 'Mughlai',
            'Naga', 'Nepalese', 'New American', 'New Mexican', 'North Eastern',
            'North Indian', 'Old Turkish Bars', 'Ottoman', 'Pacific Northwest',
            'Pakistani', 'Pan Asian', 'Parsi', 'Patisserie', 'Peruvian',
            'Pizza', 'Polish', 'Portuguese', 'Pub Food', 'Rajasthani', 'Ramen',
            'Restaurant Cafe', 'Roast Chicken', 'Rolls', 'Russian', 'Salad',
            'Sandwich', 'Scottish', 'Seafood', 'Singaporean', 'South African',
            'South Indian', 'Southern', 'Southwestern', 'Spanish',
            'Sri Lankan', 'Steak', 'Street Food', 'Sunda', 'Sushi', 'Taco',
            'Taiwanese', 'Tapas', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan',
            'Turkish', 'Turkish Pizza', 'Ukrainian', 'Vegetarian',
            'Vietnamese', 'Western', 'World Cuisine', 'Yum Cha', 'Arabian']

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "UAE",
    215: "England",
    216: "USA",
}

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}


def clean_data(df):
    df1 = df.copy()
    if 'Switch to order menu' in df1.columns:
        df1 = df1.drop('Switch to order menu', axis=1)
    if 'Restaurant ID' in df1.columns:
        df1 = df1.drop_duplicates(subset=['Restaurant ID'], keep='first')
    df1 = df1.dropna()
    df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

    return df1


def side_bar_config(df1):

    # image_path = 'projetos/logo.png'
    image = Image.open('logo.png')
    st.sidebar.image(image, width=120)

    st.sidebar.markdown('# GourmetGo')
    st.sidebar.markdown('#### Find out your new fav restaurant')
    st.sidebar.markdown("""---""")

    st.sidebar.markdown('### Filters')

    df1['Country Name'] = df1.loc[:, 'Country Code'].apply(lambda x:
                                                           country_name(x))

    select_countries = st.sidebar.multiselect(
        'Countries',
        ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland",
         "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka",
         "Turkey", "UAE", "England", "USA"],
        default=["India", "Brazil", "Canada", "New Zeland", "Philippines",
                 "Qatar", "Singapure", "South Africa", "Turkey",
                 "UAE", "England", "USA"])

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('#### Powered by Felipe Valory')

    # Country Filter
    linhas_selecionadas = df1['Country Name'].isin(select_countries)
    df1 = df1.loc[linhas_selecionadas, :]

    return df1


def side_bar_cuisines_config(df1):

    # image_path = 'projetos/logo.png'
    image = Image.open('logo.png')
    st.sidebar.image(image, width=120)

    st.sidebar.markdown('# GourmetGo')
    st.sidebar.markdown('#### Find out your new fav restaurant')
    st.sidebar.markdown("""---""")

    st.sidebar.markdown('### Filters')

    df1['Country Name'] = df1.loc[:, 'Country Code'].apply(lambda x:
                                                           country_name(x))

    select_countries = st.sidebar.multiselect(
        'Countries',
        ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland",
         "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka",
         "Turkey", "UAE", "England",
         "USA"],
        default=["India", "Brazil", "Canada", "New Zeland", "Philippines",
                 "Qatar", "Singapure", "South Africa", "Turkey",
                 "UAE", "England", "USA"])

    st.sidebar.markdown("""---""")

    select_cuisines = st.sidebar.multiselect(
        'Cuisines',
        ['African', 'American', 'Andhra', 'Arabian', 'Argentine', 'Armenian',
         'Asian', 'Asian Fusion', 'Assamese', 'Author', 'Awadhi', 'Bakery',
         'Balti', 'Bar Food', 'BBQ', 'Belgian', 'Bengali', 'Beverages',
         'Biryani', 'Brazilian', 'Breakfast', 'British', 'Burger', 'Burmese',
         'Cafe', 'Cafe Food', 'California', 'Canadian', 'Cantonese',
         'Caribbean', 'Cajun', 'Charcoal Chicken', 'Chettinad', 'Chinese',
         'Coffee', 'Coffee and Tea', 'Continental', 'Contemporary', 'Creole',
         'Crepes', 'Cuban', 'Deli', 'Desserts', 'Dimsum', 'Dim Sum',
         'Diner', 'Donuts', 'Drinks Only', 'Döner', 'Durban',
         'Eastern European', 'Egyptian', 'European', 'Fast Food',
         'Finger Food', 'Filipino', 'Fish and Chips', 'Fresh Fish',
         'French', 'Fusion', 'German', 'Giblets', 'Goan', 'Gourmet Fast Food',
         'Greek', 'Grill', 'Gujarati', 'Hawaiian', 'Healthy Food', 'Home-made',
         'Hyderabadi', 'Ice Cream', 'Indian', 'Indonesian', 'International',
         'Iranian', 'Irish', 'Italian', 'Izgara', 'Japanese', 'Juices',
         'Kebab', 'Kerala', 'Khaleeji', 'Kiwi', 'Kokoreç', 'Korean',
         'Korean BBQ', 'Kumpir', 'Latin American', 'Lebanese', 'Lucknowi',
         'Malaysian', 'Malwani', 'Mandi', 'Mangalorean', 'Mediterranean',
         'Mexican', 'Middle Eastern', 'Mineira', 'Mithai', 'Modern Australian',
         'Modern Indian', 'Mongolian', 'Moroccan', 'Momos', 'Mughlai',
         'Naga', 'Nepalese', 'New American', 'New Mexican', 'North Eastern',
         'North Indian', 'Old Turkish Bars', 'Ottoman', 'Pacific Northwest',
         'Pakistani', 'Pan Asian', 'Parsi', 'Patisserie', 'Peruvian',
         'Pizza', 'Polish', 'Portuguese', 'Pub Food', 'Rajasthani', 'Ramen',
         'Restaurant Cafe', 'Roast Chicken', 'Rolls', 'Russian', 'Salad',
         'Sandwich', 'Scottish', 'Seafood', 'Singaporean', 'South African',
         'South Indian', 'Southern', 'Southwestern', 'Spanish', 'Sri Lankan',
         'Steak', 'Street Food', 'Sunda', 'Sushi', 'Taco', 'Taiwanese',
         'Tapas', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan', 'Turkish',
         'Turkish Pizza', 'Ukrainian', 'Vegetarian', 'Vietnamese', 'Western',
         'World Cuisine', 'Yum Cha'],
        default=['North Indian', 'American', 'Arabian', 'Cafe', 'Italian',
                 'Pizza', 'Chinese', 'Burger', 'Fast Food', 'Continental',
                 'Seafood', 'Japanese', 'Brazilian'])

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('#### Powered by Felipe Valory')

    # Cousines Filter
    linhas_selecionadas = df1['Cuisines'].isin(select_cuisines)
    df1 = df1.loc[linhas_selecionadas, :]

    # Country Filter
    linhas_selecionadas = df1['Country Name'].isin(select_countries)
    df1 = df1.loc[linhas_selecionadas, :]

    return df1


def format_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f} M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f} K"
    else:
        return f"{round(num)}"


def country_name(country_id):
    return COUNTRIES[country_id]


def color_name(color_code):
    return COLORS[color_code]


def map_maker(df1):

    df_aux = (df1.loc[:, ['Restaurant ID', 'Restaurant Name', 'City',
                          'Average Cost for two', 'Currency', 'Longitude',
                          'Latitude', 'Cuisines', 'Aggregate rating']]
                 .groupby(['Restaurant ID']).max().reset_index())

    df_aux = df_aux.sample(n=500)

    map = (folium.Map(location=[df_aux['Latitude'].mean(), df_aux['Longitude']
                                .mean()], zoom_start=2))
    marker_cluster = MarkerCluster(name="Restaurants").add_to(map)

    def get_marker_color(rating):
        if rating >= 4.5:
            return 'green'
        elif rating >= 4.0:
            return 'lightgreen'
        elif rating >= 3.5:
            return 'orange'
        else:
            return 'red'

    for _, location_info in df_aux.iterrows():
        popup_content = (f"<b>{location_info['Restaurant Name']}</b><br>"
                         f"Cost for Two: {location_info['Currency']}\
                            {location_info['Average Cost for two']}<br>"
                         f"Rating: {location_info['Aggregate rating']}/5.0")
        popup = folium.Popup(popup_content, max_width=300)

        folium.Marker(
            location=[location_info['Latitude'], location_info['Longitude']],
            popup=popup,
            icon=folium.Icon(color=get_marker_color(
                location_info['Aggregate rating']), icon='info-sign')
        ).add_to(marker_cluster)

    folium_static(map, width=1024, height=550)


def country_by_rest(df1):
    df_aux = (df1[['Country Name', 'Restaurant ID']].groupby('Country Name')
              .nunique().sort_values(by='Restaurant ID', ascending=False)
              .reset_index())
    df_aux.columns = ['Countries', 'Restaurants']

    fig = go.Figure(data=[go.Bar(x=df_aux['Countries'],
                                 y=df_aux['Restaurants'],
                                 marker=dict(color='rgb(101, 46, 134)'),
                                 text=df_aux['Restaurants'],
                                 textposition='outside',
                                 textfont=dict(size=14))])
    fig.update_layout(title='Registered Restaurants by Country',
                      xaxis_title='Countries', yaxis_title='Restaurants',
                      title_font=dict(size=24),
                      xaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      yaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      height=500)

    return fig


def cities_by_country(df1):
    df_aux = (df1[['Country Name', 'City']].groupby('Country Name').nunique()
              .sort_values(by='City', ascending=False).reset_index())
    df_aux.columns = ['Countries', 'Cities']

    fig = go.Figure(data=[go.Bar(x=df_aux['Countries'],
                                 y=df_aux['Cities'],
                                 marker=dict(color='rgb(101, 46, 134)'),
                                 text=df_aux['Cities'],
                                 textposition='outside',
                                 textfont=dict(size=14))])
    fig.update_layout(title='Registered Cities by Country',
                      xaxis_title='Countries', yaxis_title='Cities',
                      title_font=dict(size=24),
                      xaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      yaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      height=500)
    return fig


def avg_rating_country(df1):
    df_aux = round(df1[['Country Name', 'Aggregate rating']]
                   .groupby('Country Name').mean()
                   .sort_values(by='Aggregate rating', ascending=False)
                   .reset_index(), 2)
    df_aux.columns = ['Countries', 'Avg Rating']
    fig = go.Figure(data=[go.Bar(x=df_aux['Countries'],
                                 y=df_aux['Avg Rating'],
                                 marker=dict(color='rgb(101, 46, 134)'),
                                 text=df_aux['Avg Rating'],
                                 textposition='outside',
                                 textfont=dict(size=14))])
    fig.update_layout(title='Avg rating by Country',
                      xaxis_title='Countries', yaxis_title='Avg Rating',
                      title_font=dict(size=24),
                      xaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      yaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      height=500)
    return fig


def price_for_two_by_country(df1):
    df_aux = (df1.loc[:, ['Country Name', 'Average Cost for two']]
              .groupby('Country Name').mean()
              .sort_values(by='Average Cost for two', ascending=False)
              .reset_index())
    df_aux.columns = ['Countries', 'Cost for two']

    # Format numbers 'Cost for two' columns
    df_aux['Formatted Cost'] = df_aux['Cost for two'].apply(format_number)

    fig = go.Figure(data=[go.Bar(
        x=df_aux['Countries'],
        y=df_aux['Cost for two'],
        marker=dict(color='rgb(101, 46, 134)'),
        text=df_aux['Formatted Cost'],
        textposition='outside',
        textfont=dict(size=14)
    )])

    fig.update_layout(
        title='Avg Cost for two by Country',
        xaxis_title='Countries',
        yaxis_title='Cost for two',
        title_font=dict(size=24),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12),
                   tickangle=45),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        margin=dict(l=50, r=50, b=150, t=50, pad=4),  # Ajustar margens
        bargap=0.15,
        height=600)

    return fig


def rest_by_city(df1):
    df_aux = (df1[['Restaurant ID', 'City', 'Country Name']]
              .groupby(['City', 'Country Name'])
              .count().sort_values(by='Restaurant ID', ascending=False)
              .reset_index())
    df_aux = df_aux.head(10)

    color_discrete_map = {
        'India': 'rgb(58, 26, 76)',
        'Australia': 'rgb(69, 31, 91)',
        'Brazil': 'rgb(81, 36, 106)',
        'Canada': 'rgb(94, 42, 122)',
        'Indonesia': 'rgb(105, 47, 137)',
        'New Zeland': 'rgb(117, 52, 152)',
        'Philippines': 'rgb(129, 57, 167)',
        'Qatar': 'rgb(151, 73, 193)',
        'Singapure': 'rgb(159, 88, 198)',
        'South Africa': 'rgb(168, 103, 203)',
        'Sri Lanka': 'rgb(177, 118, 208)',
        'Turkey': 'rgb(194, 149, 219)',
        'UAE': 'rgb(211, 179, 229)',
        'England': 'rgb(228, 209, 239)',
        'USA': 'rgb(198, 221, 240)'
    }

    fig = px.bar(df_aux, x='City', y='Restaurant ID',
                 title='Top 10 Cities with more restaurants',
                 color='Country Name',
                 color_discrete_map=color_discrete_map,
                 text='Restaurant ID')

    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Number of Restaurants',
        title_font=dict(size=24),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        height=500
    )

    return fig


def city_rest_rating(df1, best_worst):

    if best_worst == 'worst':
        rating = 'worst'
        linhas = df1['Aggregate rating'] <= 2.5
    elif best_worst == 'best':
        rating = 'best'
        linhas = df1['Aggregate rating'] >= 4

    df_aux = (df1.loc[linhas, ['City', 'Restaurant ID', 'Country Name']]
              .groupby(['City', 'Country Name']).count()
              .sort_values(by='Restaurant ID', ascending=False)
              .reset_index())
    df_aux = df_aux.head(5)

    color_discrete_map = {
        'India': 'rgb(58, 26, 76)',
        'Australia': 'rgb(69, 31, 91)',
        'Brazil': 'rgb(81, 36, 106)',
        'Canada': 'rgb(94, 42, 122)',
        'Indonesia': 'rgb(105, 47, 137)',
        'New Zeland': 'rgb(117, 52, 152)',
        'Philippines': 'rgb(129, 57, 167)',
        'Qatar': 'rgb(151, 73, 193)',
        'Singapure': 'rgb(159, 88, 198)',
        'South Africa': 'rgb(168, 103, 203)',
        'Sri Lanka': 'rgb(177, 118, 208)',
        'Turkey': 'rgb(194, 149, 219)',
        'UAE': 'rgb(211, 179, 229)',
        'England': 'rgb(228, 209, 239)',
        'USA': 'rgb(198, 221, 240)'
    }

    fig = px.bar(df_aux, x='City', y='Restaurant ID',
                 title=f'Top 5 Cities with {rating} rating restaurants',
                 color='Country Name',
                 color_discrete_map=color_discrete_map,
                 text='Restaurant ID')

    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Number of Restaurants',
        title_font=dict(size=24),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        height=500
    )

    return fig


def cuisine_per_city(df1):

    # Count number of cuisines types by city by country
    df_aux = (df1.groupby(['City', 'Country Name'])['Cuisines']
              .nunique().reset_index())

    # Order by cuisines types and get the top 10 cities
    df_aux = df_aux.sort_values(by='Cuisines', ascending=False).head(10)

    color_discrete_map = {
        'India': 'rgb(58, 26, 76)',
        'Australia': 'rgb(69, 31, 91)',
        'Brazil': 'rgb(81, 36, 106)',
        'Canada': 'rgb(94, 42, 122)',
        'Indonesia': 'rgb(105, 47, 137)',
        'New Zealand': 'rgb(117, 52, 152)',
        'Philippines': 'rgb(129, 57, 167)',
        'Qatar': 'rgb(151, 73, 193)',
        'Singapore': 'rgb(159, 88, 198)',
        'South Africa': 'rgb(168, 103, 203)',
        'Sri Lanka': 'rgb(177, 118, 208)',
        'Turkey': 'rgb(194, 149, 219)',
        'UAE': 'rgb(211, 179, 229)',
        'England': 'rgb(228, 209, 239)',
        'USA': 'rgb(198, 221, 240)'
    }

    fig = px.bar(df_aux, x='City', y='Cuisines',
                 title='Top 10 cities with the most distinct cuisine types',
                 color='Country Name',
                 color_discrete_map=color_discrete_map,
                 text='Cuisines')

    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Number of cuisines',
        title_font=dict(size=24),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        height=500
    )

    fig.update_traces(texttemplate='%{text}', textposition='outside')

    return fig


def cuisine_max_rate(df1, cuisine):

    if cuisine in df1['Cuisines'].unique():
        colunas = ['Restaurant ID', 'Restaurant Name', 'Aggregate rating',
                   'Cuisines', 'Country Name', 'City', 'Currency',
                   'Average Cost for two']

        df_filtered = df1[df1['Cuisines'] == cuisine][colunas]
        df_sorted = (df_filtered.sort_values('Aggregate rating',
                                             ascending=False).head(1))

        for _, row in df_sorted.iterrows():
            st.metric(
                label=f'{row["Restaurant Name"]}',
                value=f'{row["Aggregate rating"]}/5.0',
                help=f"""
                    Restaurant: {row["Restaurant Name"]}\n
                    Country: {row["Country Name"]}\n
                    City: {row["City"]}\n
                    Price for two: {row["Currency"]}
                                   {row["Average Cost for two"]}
                """
            )
    else:
        st.write(f'No restaurants found for cuisine: {cuisine}')


def top_10_best_rest(df1):
    df_aux = (df1[['Restaurant Name', 'Country Name', 'City', 'Cuisines',
                   'Aggregate rating', 'Currency', 'Average Cost for two']]
              .groupby('Restaurant Name').max()
              .sort_values(by='Aggregate rating', ascending=False)
              .reset_index())

    df_aux.columns = ['Restaurant Name', 'Country', 'City', 'Cuisines',
                      'Avg Rating', 'Currency', 'Avg Cost for two']

    df_aux = df_aux.head(10)

    return df_aux


def best_worst_cuisine(df1, top_asc):

    if top_asc:
        text = 'worst'
    else:
        text = 'best'

    df_aux = (df1[['Aggregate rating', 'Cuisines']].groupby('Cuisines')
              .max().sort_values(by='Aggregate rating', ascending=top_asc)
              .reset_index())

    df_aux = df_aux.head(10)

    fig = go.Figure(data=[go.Bar(x=df_aux['Cuisines'],
                                 y=df_aux['Aggregate rating'],
                                 marker=dict(color='rgb(101, 46, 134)'),
                                 text=df_aux['Aggregate rating'],
                                 textposition='outside',
                                 textfont=dict(size=14))])
    fig.update_layout(title=f'Top 10 {text} cuisines',
                      xaxis_title='Cuisines', yaxis_title='Avg Ratings',
                      title_font=dict(size=24),
                      xaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      yaxis=dict(title_font=dict(size=16),
                                 tickfont=dict(size=12)),
                      height=600)

    fig.update_xaxes(tickangle=-90)

    return fig
