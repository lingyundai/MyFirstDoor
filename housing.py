import os
import pandas as pd
import streamlit as st
import json

# Define the path to the OneDrive folder

# Read the data from the excel file and convert it to a pandas DataFrame
def read_excel_from_onedrive(file_name):
    # Define the path to the specific file within the OneDrive folder
    # Read the data into a pandas DataFrame
    df = pd.read_excel(file_name)

    #convert the data to a pandas DataFrame
    df = pd.DataFrame(df)

    # Display the first few rows of the DataFrame
    return df
# Function to recommend properties based on state and price range
def recommend_properties(df, state, min_price, max_price, top_k=5):
    # Filter properties by state
    filtered_df = df[df['state'] == state]
    
    # Further filter properties by price range
    filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]
    
    # Sort by price (or any other metric you prefer) and get top K properties
    recommendations = filtered_df.sort_values(by='price').head(top_k)
    
    # Select relevant columns to display
    output_columns = ['unique_id', 'streetAddress', 'price', 'bedrooms', 'bathrooms', 
                      'livingArea', 'yearBuilt', 'longitude', 'latitude', 'imgSrc', 'state','county','city','zipcode','schools']
    
    # Prepare the result
    result = recommendations[output_columns]
    result_json = result.to_json(orient='records')
    
    # Convert to JSON format if needed
    return result_json

