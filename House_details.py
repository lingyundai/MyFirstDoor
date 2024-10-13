import streamlit as st

# Function to create a card
def create_card(title, price, bedrooms, bathrooms, living_area, year_built, location, schools):
    card_html = f"""
    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between;">
        <h4>{title}</h4>
        <p><strong>Price:</strong> {price}</p>
        <p><strong>Bedrooms:</strong> {bedrooms}</p>
        <p><strong>Bathrooms:</strong> {bathrooms}</p>
        <p><strong>Living Area:</strong> {living_area}</p>
        <p><strong>Year Built:</strong> {year_built}</p>
        <p><strong>Location:</strong> {location}</p>
        <p><strong>Schools:</strong> {schools}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

#    hd.create_card(house['unique_id'], house['price'], house['bedrooms'], house['bathrooms'], house['livingArea'], house['yearBuilt'], house['city'], house['schools'])

