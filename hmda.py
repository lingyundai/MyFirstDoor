import streamlit as st
import components as cp
import requests
import plotly.express as px

def hmda_plot(selected_state, state_name):
    #HMDA data
    url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/aggregations"
    years = [2023, 2022, 2021, 2020, 2019, 2018]
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
            #print(f"Year {year} - Status code: {response.status_code}")
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
                #print(f"Data received for {year}: {yearly_data[year]}")
            else:
                print(f"Error for year {year}: {response.status_code} {response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred for year {year}: {e}")

    years = list(yearly_data.keys())
    approval_rates = [yearly_data[year]['approval_rate'] for year in years]

    # Create a DataFrame for Plotly Express
    data = {
        'Year': years,
        'Approval Rate (%)': approval_rates
    }

    # Create a Plotly Express line chart
    #cp.main_subtitle(f'Mortgage Approval Rates by Year in {state_name}')
    title=f'Mortgage Approval Rates by Year in {selected_state}'
    fig = px.line(data_frame=data, x='Year', y='Approval Rate (%)', markers=True, title=title)

    #fig.update_yaxes(range=[0, 100])
    fig.update_xaxes(tickmode='array', tickvals=years)
    fig.update_layout(title_font=dict(size=24))

    # Show the plot in Streamlit
    st.plotly_chart(fig)