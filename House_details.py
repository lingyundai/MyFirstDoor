from streamlit_card import card
import streamlit as st
import pandas as pd
import components as cp
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


# Function to create a card for each property
def create_property_card(property):
    col1, col2 = st.columns([3, 5])
    with col1:
        card(
            title=property['streetAddress'],
            text=f"${property['price']:,} • {property['bedrooms']} bed • {property['bathrooms']} bath • {property['livingArea']} sqft",
            image=property['imgSrc']
            )
    with col2:
        # Create tabs for different sections
        tab1, tab2 = st.tabs(["Property Details", "Schools"])

        with tab1:
            st.write(f"Year Built: {property['yearBuilt']}")
            st.write(f"Address: {property['streetAddress']}, {property['county']}, {property['state']}, USA, {property['zipcode']}")
            st.write(f"Price: ${property['price']}")

        with tab2:
            # Create a dropdown for schools
            school_names = [school['name'] for school in property['schools']]
            selected_school = st.selectbox("Schools", school_names, key=f"school_{property['streetAddress']}")

            # Display selected school details
            if selected_school:
                school_details = next(school for school in property['schools'] if school['name'] == selected_school)
                st.write(f"School Name: {school_details['name']}")
                st.write(f"Rating: {school_details['rating']}")
                st.write(f"Distance: {school_details['distance']} miles")
                st.write(f"Grades: {school_details['grades']}")
                st.write(f"Type: {school_details['type']}")
                st.write(f"[More Info]({school_details['link']})")

def show_map():
        # Display property location on a map using st.session_state['house']
    if 'house' in st.session_state:
        lat_lon_list = [{'lat': h['latitude'], 'lon': h['longitude'], 'image_url': h['imgSrc'], 'price': h['price'], 'zip_code': h['zipcode'], 'address': h['streetAddress']} for h in st.session_state['house']]
        # st.map(pd.DataFrame(lat_lon_list))
        st.subheader("Interactive US Map with Property Details")

        # Calculate the center of all properties for initial map view
        center_lat = sum(prop["lat"] for prop in lat_lon_list) / len(lat_lon_list)
        center_lon = sum(prop["lon"] for prop in lat_lon_list) / len(lat_lon_list)

        # Create the map
        m = cp.create_map(center_lat, center_lon)

        # Create a MarkerCluster
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers for each property
        for prop in lat_lon_list:
            popup_html = f"""
            <img src="{prop['image_url']}" width="100%"><br>
            <strong>Price:</strong> ${prop['price']:,}<br>
            <strong>Zip Code:</strong> {prop['zip_code']}<br>
            <strong>Address:</strong> {prop['address']}
            """
            cp.add_marker(marker_cluster, prop["lat"], prop["lon"], popup_html)

        # Display the map
        folium_static(m)

