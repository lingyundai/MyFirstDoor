import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium



st.markdown("<h1 style='text-align: center;'>Housing Navigator</h1>", unsafe_allow_html=True)

data = {
    #example data
    "Location": ["Location 1", "Location 2", "Location 3"],
    "Latitude": [37.7749, 34.0522, 40.7128],
    "Longitude": [-122.4194, -118.2437, -74.0060],
    "Price": [1000, 1500, 2000]
}
df = pd.DataFrame(data)

# Create a folium map centered around the average coordinates
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

# Add points to the map
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        popup=f"{row['Location']}: ${row['Price']}",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)
st_folium(m, width=400, height=300)

state = st.sidebar.selectbox("Select a state", ["California", "New York", "Texas"])