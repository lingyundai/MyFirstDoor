import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('data/historical_housing_price.csv', parse_dates=['Date'])
    return data

# Prepare the data
def prepare_data(df, state):
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df[['Date', state]]
    df = df.rename(columns={state: 'Price'})
    df['State'] = state
    return df