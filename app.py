import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


def main_page():
    st.markdown("<h1 style='text-align: center;'>Housing Navigator</h1>",
                unsafe_allow_html=True)


    state = st.sidebar.selectbox("Select a state", 'California')

    data = {
        # example data
        "Location": ["Location 1", "Location 2", "Location 3"],
        "Latitude": [37.7749, 34.0522, 40.7128],
        "Longitude": [-122.4194, -118.2437, -74.0060],
        "Price": [1000, 1500, 2000]
    }
    df = pd.DataFrame(data)

    m = folium.Map(location=[df["Latitude"].mean(),df["Longitude"].mean()], zoom_start=2)
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Location']}: ${row['Price']}",
            #change size of marker
            icon=folium.Icon(icon="home", prefix="fa", color="red")

        ).add_to(m)

    # For map and location specific data
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Map")
        st_folium(m, width=400, height=300)

    with col2:
        st.subheader("City Details")

    if st.sidebar.button("Go to Budget Calculator"):
            st.session_state.page = "BudgetCalculator"



def budget_calculator():
    st.markdown("<h1 style='text-align: center;'>Budget Calculator</h1>", unsafe_allow_html=True)
    
    # Budget calculation logic here
    income = st.number_input("Enter your monthly income", min_value=0)
    expenses = st.number_input("Enter your monthly expenses", min_value=0)


# Navigation logic
if 'page' not in st.session_state:
    st.session_state.page = "Main"

if st.session_state.page == "Main":
    main_page()
elif st.session_state.page == "BudgetCalculator":
    budget_calculator()














def filter_housing(budget, location):
    # Placeholder function: Replace with actual filtering logic
    data = {
        "Location": ["Location 1", "Location 2", "Location 3"],
        "Price": [1000, 1500, 2000]
    }
    df = pd.DataFrame(data)
    filtered_df = df[(df["Location"] == location) & (df["Price"] <= budget)]
    return filtered_df