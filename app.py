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

# Side bar and main area after user signed in
col1, col2 = st.columns([3, 1])

# Main content area
with col1:
    st.title("Real Estate Listings")
    if st.session_state['house']:
        for property in st.session_state['house']:
            hd.create_property_card(property)
    else:
        st.write("No properties found. Please generate a budget to see listings.")
    # st.title("Interactive US Map with Property Details")

    # # Generate mock dataset
    # properties = cp.generate_mock_data(15)  # Generate 15 random properties
    
    # # Calculate the center of all properties for initial map view
    # center_lat = sum(prop["latitude"] for prop in properties) / len(properties)
    # center_lon = sum(prop["longitude"] for prop in properties) / len(properties)

    # # Create the map
    # m = cp.create_map(center_lat, center_lon)

    # # Create a MarkerCluster
    # marker_cluster = MarkerCluster().add_to(m)

    # # Add markers for each property
    # for prop in properties:
    #     popup_html = f"""
    #     <img src="{prop['image_url']}" width="100%"><br>
    #     <strong>Price:</strong> {prop['price']}<br>
    #     <strong>Zip Code:</strong> {prop['zip_code']}<br>
    #     <strong>Address:</strong> {prop['address']}
    #     """
    #     cp.add_marker(marker_cluster, prop["latitude"], prop["longitude"], popup_html)

    # # Display the map
    # folium_static(m)


    # st.title('Housing Price Trend')

    # # Load the data
    # df = sr.load_data()

    # # Assume the state is stored in a variable
    # # For demonstration, we'll use a text input to simulate this
    # state = st.text_input("Enter the state name (as it appears in the dataset):")

    # if state and state in df.columns:
    #     # Prepare data for the selected state
    #     state_df = sr.prepare_data(df, state)

    #     # Create the line chart
    #     fig = px.line(state_df, x='Date', y='Price',
    #                     title=f'Housing Price Trend for {state}',
    #                     labels={'Price': 'Housing Price', 'Date': 'Year'})

    #     # Customize the chart
    #     fig.update_layout(showlegend=False)
    #     fig.update_xaxes(title_text='Year and Month ')
    #     fig.update_yaxes(title_text='Housing Price ')

    #     # Display the chart
    #     st.plotly_chart(fig)
    # elif state:
    #     st.error(f"State '{state}' not found in the dataset. Please check the spelling and try again.")
    # else:
    #     st.write('Please enter a state name to display the trend.')


# # Content for the right "sidebar"
# with col2:
#     st.subheader("Preferences")
#     num_bedrooms = cp.user_slider("How many bedrooms would you prefer to have?", 
#               "So we can match you with homes that closely align with your preferences.", 0)
#     num_bathrooms = cp.user_slider("How many bathrooms would you prefer to have?", 
#               "So we can match you with homes that closely align with your preferences.", 1)

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
    # st.rerun()

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

#cp.sidebar_subtitle("Preferences")



#num_bedrooms = cp.user_slider("How many bedrooms would you prefer to have?", 
#              "So we can match you with homes that closely align with your preferences.")
#num_bathrooms = cp.user_slider("How many bathrooms would you prefer to have?", 
#              "So we can match you with homes that closely align with your preferences.")
        
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
    



# Main content area

st.title("Real Estate Listings")
if st.session_state['house']:
    for property in st.session_state['house']:
        hd.create_property_card(property)
else:
    st.write("No properties found. Please generate a budget to see listings.")
