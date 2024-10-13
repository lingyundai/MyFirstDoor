import streamlit as st
import components as cp
import House_details as hd
import service as serv
import housing as recommender
import pandas as pd
import ast
from streamlit_card import card

# Initialize session state
if 'house' not in st.session_state:
    st.session_state['house'] = []

house = []

# serv.load_session_state_from_json()

custom_css = """
<style>
.st-emotion-cache-13ln4jf {
    padding-left: 2rem;
    padding-right: 4rem;
    max-width: none !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

main_df = recommender.read_excel_from_onedrive('Zillow.com House Price Prediction Data(1).xlsx')
main_df['unique_id'] = main_df.index + 1

state_acronyms = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
]

cp.title()

cp.main_subtitle("Recommending the right home, just for you.")

# Sidebar content
cp.sidebar_subtitle("Location")
selected_state = st.sidebar.selectbox("What state would you like to live in?", state_acronyms)
cp.sidebar_subtitle("Budget Estimator")
annual_income = cp.user_input("How much is your gross annual income?", 
              "Annual Gross Income", 
              "The amount of the income you make per year, before taxes.")
monthly_debts = cp.user_input("How much are your monthly debts?", 
              "Monthly Debts", 
              "Recurring debts you owe each month, such as car payments, student loans, etc.")
down_payment = cp.user_input("How much do you have saved for a down payment?", 
              "Down Payment", 
              "How much money you have saved for a down payment.")
credit = cp.user_input("(Optional) What is your credit score?", 
              "Credit Score", 
              "We use this to estimate a loan interest rate. If you choose not to provide your credit score, we will use average interest rates in your calculation.")

# Budget calculation
income = annual_income/12
max_monthly_payment = min(0.28 * income, 0.36 * income - monthly_debts)
interest_rate = 5.5/100 if credit == 0 else max(3 / 100, 8 / 100 - (credit - 500) / 100 / 100)
loan_years = 30
monthly_rate = interest_rate / 12
n_payments = loan_years * 12
loan_amount = max_monthly_payment * ((1 + monthly_rate) ** n_payments - 1) / (monthly_rate * (1 + monthly_rate) ** n_payments)
max_home_price = loan_amount + down_payment
display_home_price = f"{max_home_price:.2f}"

def show_budget():
    cp.sidebar_subtitle(f"Estimated Max Home Price: ${display_home_price}")

# Generate Budget button
if st.sidebar.button("Generate Budget"):
    show_budget()
    house = recommender.recommend_properties(main_df, selected_state, 100000, max_home_price, top_k=5)
    st.session_state['house'] = serv.parse_property_data(house)
    # st.rerun()

# Main content area
col1, col2 = st.columns([5, 1])

with col1:
    st.title("Real Estate Listings")
    if st.session_state['house']:
        for property in st.session_state['house']:
            hd.create_property_card(property, col1)
    else:
        st.write("No properties found. Please generate a budget to see listings.")
    # if st.session_state['house']:
    #     for i, property in enumerate(st.session_state['house']):
    #         hd.create_property_card(property, col1 if i % 2 == 0 else col2)
    # else:
        # st.write("No properties found. Please generate a budget to see listings.")

# Preferences in the right column
with col2:
    st.subheader("Preferences")
    num_bedrooms = cp.user_slider("How many bedrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")
    num_bathrooms = cp.user_slider("How many bathrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")

# # Display selected property details (if any)
# if 'selected_property' in st.session_state:
#     selected_property = next((p for p in st.session_state['house'] if p['unique_id'] == st.session_state.selected_property), None)
    # if selected_property:
        # hd.display_property_details(selected_property)