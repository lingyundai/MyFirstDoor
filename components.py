import streamlit as st
import folium
from streamlit_folium import st_folium
import random

def title():
    st.sidebar.title("Welcome to MyFirstDoor", anchor=False)

def main_subtitle(text):
    st.subheader(text)

def sidebar_subtitle(text):
    st.sidebar.subheader(text)

def user_input(content, placeholder, helpMessage):
    value = st.sidebar.number_input(content,
                            placeholder=placeholder,
                            help=helpMessage, step=0)
    return float(value)

def generate():
    st.sidebar.button("Generate budget")

def user_slider(content, helpMessage):
    value = st.slider(content, 
                      min_value=0, max_value=10,
                            help=helpMessage)
    return int(value)

# Function to create the map
def create_map(center_lat, center_lon, zoom_start=4):
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)
    return m

# Function to add a marker with popup
def add_marker(m, lat, lon, popup_html):
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
    ).add_to(m)

# Function to generate mock dataset
def generate_mock_data(num_properties=10):
    properties = []
    for i in range(num_properties):
        property = {
            "id": i + 1,
            "latitude": random.uniform(24, 49),  # Rough boundaries for continental US
            "longitude": random.uniform(-125, -66),
            "price": f"${random.randint(100000, 1000000):,}",
            "zip_code": f"{random.randint(10000, 99999):05d}",
            "address": f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St, Anytown, USA",
            "image_url": f"https://picsum.photos/seed/{i}/150/150"  # Random image for each property
        }
        properties.append(property)
    return properties
