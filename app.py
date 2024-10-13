import streamlit as st
import components as cp
import House_details as hd
import service as serv
import housing as recommender

# Inject custom CSS to remove max-width from the specific class
custom_css = """
<style>
.st-emotion-cache-13ln4jf {
    max-width: none !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

serv.load_session_state_from_json()

# Side bar and main area after user signed in
col1, col2 = st.columns([3, 12])

cp.title()

cp.main_subtitle("Recommending the right home, just for you.")

cp.sidebar_subtitle("Budget Calculator")

annual_income = cp.user_input("How much is your gross annual income?", 
              "Annual Gross Income", 
              "The amount of the income you make per year, before taxes.")

monthly_debts = cp.user_input("How much are your monthly debts?", 
              "Monthly Debts", 
              "Recurring debts you owe each month, such as car payments, student loans, etc.")

down_payment = cp.user_input("How much do you have saved for a down payment?", 
              "Down Payment", 
              "How much money you have saved for a down payment.")

credit = 0

credit = cp.user_input("(Optional) What is your credit score?", 
              "Credit Score", 
              "We use this to estimate a loan interest rate. If you choose not to provide your credit score, we will use average interest rates in your calculation.")

income = annual_income/12

#formula for maximum monthly mortgage payment
max_monthly_payment = min(0.28 * income, 0.36 * income - monthly_debts)

#estimated interest rate
if(credit == 0):
    interest_rate = 5.5/100 #sample rate
else:
    interest_rate = max(3 / 100, 8 / 100 - (credit - 500) / 100 / 100)  #3% minimum and 8% maximum

#loan term in years
loan_years = 30

# monthly interest rate
monthly_rate = interest_rate / 12

#total number of payments
n_payments = loan_years * 12

#calculate maximum affordable loan amount
loan_amount = max_monthly_payment * ((1 + monthly_rate) ** n_payments - 1) / (monthly_rate * (1 + monthly_rate) ** n_payments)

#calculate maximum affordable home price
max_home_price_numeric = loan_amount + down_payment

max_home_price = f"{max_home_price_numeric:.2f}"

#for 30 year term only rn
def show_budget():
    cp.main_subtitle(max_home_price)

main_df = recommender.read_excel_from_onedrive('Zillow.com House Price Prediction Data(1).xlsx')
main_df['unique_id'] = main_df.index + 1

# Create a button and call the function if it's clicked
if st.sidebar.button("Generate Budget"):
    show_budget()
    st.session_state['house'] = recommender.recommend_properties(main_df, 'CA', 100000, max_home_price_numeric, top_k=5)

if 'house' in st.session_state:
    for house in st.session_state['house']:
        hd.create_card(house['unique_id'], house['price'], house['bedrooms'], house['bathrooms'], house['livingArea'], house['yearBuilt'], house['city'], house['schools'])
        # hd.create_card(house['unique_id'], house['price'], house['bedrooms'], house['bathrooms'], house['livingArea'], house['yearBuilt'], house['city'], house['schools'])

import streamlit as st
import pandas as pd
import ast
from streamlit_card import card

# Sample data (you would typically load this from a file or database)
data = [
    {
        "unique_id": 2000,
        "streetAddress": "4040 Piedmont Dr SPC 332",
        "price": 137600,
        "bedrooms": 2,
        "bathrooms": 2,
        "livingArea": 1344,
        "yearBuilt": 1988,
        "longitude": -117.19638,
        "latitude": 34.1421,
        "imgSrc": "https://photos.zillowstatic.com/fp/a8793da6b48f0e692f1fc5983d2155ea-p_d.jpg",
        "state": "CA",
        "county": "San Bernardino County",
        "city": "Highland",
        "zipcode": "92346",
        "schools": "[{'link': 'https://www.greatschools.org/california/highland/5286-Oehl-Elementary-School/', 'rating': 3, 'totalCount': None, 'distance': 0.7, 'assigned': None, 'name': 'Oehl Elementary School', 'studentsPerTeacher': None, 'isAssigned': None, 'size': None, 'level': 'Elementary', 'grades': 'K-6', 'type': 'Public'}, {'link': 'https://www.greatschools.org/california/highland/5299-Serrano-Middle-School/', 'rating': 3, 'totalCount': None, 'distance': 1.3, 'assigned': None, 'name': 'Serrano Middle School', 'studentsPerTeacher': None, 'isAssigned': None, 'size': None, 'level': 'Middle', 'grades': '7-8', 'type': 'Public'}, {'link': 'https://www.greatschools.org/california/san-bernardino/5298-San-Gorgonio-High-School/', 'rating': 5, 'totalCount': None, 'distance': 2.5, 'assigned': None, 'name': 'San Gorgonio High School', 'studentsPerTeacher': None, 'isAssigned': None, 'size': None, 'level': 'High', 'grades': '9-12', 'type': 'Public'}]"
    },
    # Add more property listings here...
]

# Convert schools string to list of dictionaries for each property
for property in data:
    property['schools'] = ast.literal_eval(property['schools'])

# Set page config
# st.set_page_config(page_title="Real Estate Listings", layout="wide")

# Title
st.title("Real Estate Listings")

# Create a grid layout
col1, col2 = st.columns(2)

# Function to create a card for each property
def create_property_card(property, column):
    with column:
        card_clicked = card(
            title=property['streetAddress'],
            text=f"${property['price']:,} • {property['bedrooms']} bed • {property['bathrooms']} bath • {property['livingArea']} sqft",
            image=property['imgSrc'],
            url="#"
        )
        if card_clicked:
            st.session_state.selected_property = property['unique_id']

# Display property cards
for i, property in enumerate(data):
    create_property_card(property, col1 if i % 2 == 0 else col2)

# Display detailed information when a card is clicked
if 'selected_property' in st.session_state:
    selected_property = next((p for p in data if p['unique_id'] == st.session_state.selected_property), None)
    if selected_property:
        st.header("Property Details")
        st.subheader(selected_property['streetAddress'])
        st.write(f"**Price:** ${selected_property['price']:,}")
        st.write(f"**Bedrooms:** {selected_property['bedrooms']}")
        st.write(f"**Bathrooms:** {selected_property['bathrooms']}")
        st.write(f"**Living Area:** {selected_property['livingArea']} sq ft")
        st.write(f"**Year Built:** {selected_property['yearBuilt']}")
        st.write(f"**Location:** {selected_property['city']}, {selected_property['state']} {selected_property['zipcode']}")
        
        st.subheader("Nearby Schools")
        for school in selected_property['schools']:
            st.write(f"**{school['name']}** ({school['level']})")
            st.write(f"Rating: {school['rating']}/10 • Distance: {school['distance']} miles")
        
        # Display map
        st.subheader("Location")
        df = pd.DataFrame({
            'lat': [selected_property['latitude']],
            'lon': [selected_property['longitude']]
        })
        st.map(df)

cp.sidebar_subtitle("Preferences")

num_bedrooms = cp.user_slider("How many bedrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")

num_bathrooms = cp.user_slider("How many bathrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")

    




