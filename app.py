import streamlit as st
import components as cp

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
max_home_price = loan_amount + down_payment

max_home_price = f"{max_home_price:.2f}"

#for 30 year term only rn
def show_budget():
    cp.main_subtitle(max_home_price)

#create a button and call the function if it's clicked
if st.sidebar.button("Generate Budget"):
    show_budget()

cp.sidebar_subtitle("Preferences")

num_bedrooms = cp.user_slider("How many bedrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")

num_bathrooms = cp.user_slider("How many bathrooms would you prefer to have?", 
              "So we can match you with homes that closely align with your preferences.")

#import streamlit as st
#import pandas as pd
#import numpy as np
#import folium
#from streamlit_folium import st_folium

#def filter_housing(budget, location):
#    # Placeholder function: Replace with actual filtering logic
#    data = {
#        "Location": ["Location 1", "Location 2", "Location 3"],
#        "Price": [1000, 1500, 2000]
#    }
#    df = pd.DataFrame(data)
#    filtered_df = df[(df["Location"] == location) & (df["Price"] <= budget)]
#    return filtered_df

#st.markdown("<h1 style='text-align: center;'>Housing Navigator</h1>", unsafe_allow_html=True)

##sidebar 
#state = st.sidebar.selectbox("Select a state", 'California')


#data = {
#    #example data
#    "Location": ["Location 1", "Location 2", "Location 3"],
#    "Latitude": [37.7749, 34.0522, 40.7128],
#    "Longitude": [-122.4194, -118.2437, -74.0060],
#    "Price": [1000, 1500, 2000]
#}
#df = pd.DataFrame(data)

#m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=2)
#for idx, row in df.iterrows():
#    folium.CircleMarker(
#        location=[row["Latitude"], row["Longitude"]],
#        radius=10,
#        popup=f"{row['Location']}: ${row['Price']}",
#        color='blue',
#        fill=True,
#        fill_color='blue'
#    ).add_to(m)

#For map and location specific data
#col1, col2 = st.columns([2, 1]) 
#with col1:
#   st_folium(m, width=400, height=300)

#with col2:
#    location = st.selectbox("Select a location", df["Location"].values)
    




