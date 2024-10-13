import streamlit as st
import components as cp
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import service as sr
import plotly.express as px
import requests
import io
import pandas as pd

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

st.title("Interactive US Map with Property Details")

# Generate mock dataset
properties = cp.generate_mock_data(15)  # Generate 15 random properties

# Calculate the center of all properties for initial map view
center_lat = sum(prop["latitude"] for prop in properties) / len(properties)
center_lon = sum(prop["longitude"] for prop in properties) / len(properties)

# Create the map
m = cp.create_map(center_lat, center_lon)

# Create a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers for each property
for prop in properties:
    popup_html = f"""
    <img src="{prop['image_url']}" width="100%"><br>
    <strong>Price:</strong> {prop['price']}<br>
    <strong>Zip Code:</strong> {prop['zip_code']}<br>
    <strong>Address:</strong> {prop['address']}
    """
    cp.add_marker(marker_cluster, prop["latitude"], prop["longitude"], popup_html)

# Display the map
folium_static(m)


st.title('Housing Price Trend')

# Load the data
df = sr.load_data()

# Assume the state is stored in a variable
# For demonstration, we'll use a text input to simulate this
state = st.text_input("Enter the state name (as it appears in the dataset):")

if state and state in df.columns:
    # Prepare data for the selected state
    state_df = sr.prepare_data(df, state)

    # Create the line chart
    fig = px.line(state_df, x='Date', y='Price',
                    title=f'Housing Price Trend for {state}',
                    labels={'Price': 'Housing Price', 'Date': 'Year'})

    # Customize the chart
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='Year and Month ')
    fig.update_yaxes(title_text='Housing Price ')

    # Display the chart
    st.plotly_chart(fig)
elif state:
    st.error(f"State '{state}' not found in the dataset. Please check the spelling and try again.")
else:
    st.write('Please enter a state name to display the trend.')
