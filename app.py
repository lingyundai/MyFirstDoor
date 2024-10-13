import streamlit as st
import components as cp
import requests
import House_details as hd
import service as serv
import housing as recommender
import pandas as pd
import ast
from streamlit_card import card
# serv.load_session_state_from_json()
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import service as sr
import plotly.express as px
import requests
import io

# Initialize session state
if 'house' not in st.session_state:
    st.session_state['house'] = []

house = []



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

main_df = recommender.read_excel_from_onedrive('data/Zillow.com House Price Prediction Data(1).xlsx')
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

col1, col2 = st.columns([3, 1])

# Create the dropdown menu with state acronyms
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


#create a button and call the function if it's clicked
# Generate Budget button
if st.sidebar.button("Generate Budget"):
    show_budget()
    house = recommender.recommend_properties(main_df, selected_state, 100000, max_home_price, top_k=5)
    st.session_state['house'] = serv.parse_property_data(house)

# Main content area
with col1:
    st.title("Real Estate Listings")
    if st.session_state['house']:
        for property in st.session_state['house']:
            hd.create_property_card(property)
            # Display property location on a map using st.session_state['house']
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            hd.show_map()
    else:
        st.write("No properties found. Please generate a budget to see listings.")

#HMDA data
url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/aggregations"
years = [2023, 2022, 2021, 2020]
#dictionary to store results by year
yearly_data = {}
for year in years:
    total_approvals_for_year = 0
    total_applications_for_year = 0

    params = {
    "years": year,
    "states": selected_state,
    "actions_taken": "1,2,3,4,5,6,7,8" #total applications
    }
    try:
        #GET request
        response = requests.get(url, params=params)
        #print status code and response for debugging
        print(f"Year {year} - Status code: {response.status_code}")
        #check if the request was successful (status code 200)
        if response.status_code == 200:
            #parse JSON response
            data = response.json()
            for entry in data.get('aggregations', []):
                if entry.get('actions_taken') in ['1', '2']:
                    #only count approvals
                    total_approvals_for_year += entry.get('count', 0)
                #count all applications
                total_applications_for_year += entry.get('count', 0)
            #store data for the year
            approval_rate = (total_approvals_for_year / total_applications_for_year) * 100 if total_applications_for_year > 0 else 0
            yearly_data[year] = {
                "total_approvals": total_approvals_for_year,
                "total_applications": total_applications_for_year,
                "approval_rate": approval_rate
            }
            print(f"Data received for {year}: {yearly_data[year]}")
        else:
            print(f"Error for year {year}: {response.status_code} {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for year {year}: {e}")

for year, data in yearly_data.items():
    print(f"Year: {year}")
    print(f"  Total Approvals: {data['total_approvals']}")
    print(f"  Total Applications: {data['total_applications']}")
    print(f"  Approval Rate: {data['approval_rate']:.2f}%\n")