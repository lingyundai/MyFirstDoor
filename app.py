import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium


def filter_housing(budget, location):
    # Placeholder function: Replace with actual filtering logic
    data = {
        "Location": ["Location 1", "Location 2", "Location 3"],
        "Price": [1000, 1500, 2000]
    }
    df = pd.DataFrame(data)
    filtered_df = df[(df["Location"] == location) & (df["Price"] <= budget)]
    return filtered_df

st.markdown("<h1 style='text-align: center;'>Housing Navigator</h1>", unsafe_allow_html=True)

#sidebar 
state = st.sidebar.selectbox("Select a state", 'California')


data = {
    #example data
    "Location": ["Location 1", "Location 2", "Location 3"],
    "Latitude": [37.7749, 34.0522, 40.7128],
    "Longitude": [-122.4194, -118.2437, -74.0060],
    "Price": [1000, 1500, 2000]
}
df = pd.DataFrame(data)

m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=2)
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        popup=f"{row['Location']}: ${row['Price']}",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

#For map and location specific data
col1, col2 = st.columns([2, 1]) 
with col1:
    st_folium(m, width=400, height=300)

with col2:
    location = st.selectbox("Select a location", df["Location"].values)
    




