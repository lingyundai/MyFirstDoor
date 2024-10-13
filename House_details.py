from streamlit_card import card
import streamlit as st

# Function to create a card for each property
def create_property_card(property, column):
    with column:
        card_clicked = card(
            title=property['streetAddress'],
            text=f"${property['price']:,} • {property['bedrooms']} bed • {property['bathrooms']} bath • {property['livingArea']} sqft",
            image=property['imgSrc'],
            url="#"
        )
        # if card_clicked:
        #     st.session_state.selected_property = property['unique_id']