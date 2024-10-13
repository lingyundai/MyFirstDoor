from streamlit_card import card
import streamlit as st

# Function to create a card for each property
def create_property_card(property):
    col1, col2 = st.columns([2, 4])
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
            selected_school = st.selectbox("Schools", school_names)

            # Display selected school details
            if selected_school:
                school_details = next(school for school in property['schools'] if school['name'] == selected_school)
                st.write(f"School Name: {school_details['name']}")
                st.write(f"Rating: {school_details['rating']}")
                st.write(f"Distance: {school_details['distance']} miles")
                st.write(f"Grades: {school_details['grades']}")
                st.write(f"Type: {school_details['type']}")
                st.write(f"[More Info]({school_details['link']})")