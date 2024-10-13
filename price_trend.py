import streamlit as st
import components as cp
import service as sr
import requests
import plotly.express as px

def trend_plot(selected_state):
    #cp.main_subtitle(f'Housing Price Trend for {selected_state}')

    # Load the data
    df = sr.load_data()

    # Assume the state is stored in a variable
    # For demonstration, we'll use a text input to simulate this
    state = selected_state

    if state and state in df.columns:
        # Prepare data for the selected state
        state_df = sr.prepare_data(df, state)

        # Create the line chart
        fig = px.line(state_df, x='Date', y='Price',
                        title=f'Housing Price Trends in {state}',
                        labels={'Price': 'Housing Price', 'Date': 'Year'})

        # Customize the chart
        fig.update_layout(showlegend=False)
        fig.update_xaxes(title_text='Year')
        fig.update_yaxes(title_text='Avergae Home Price ($)')

        fig.update_layout(title_font=dict(size=24))
        # Display the chart
        st.plotly_chart(fig)
    elif state:
        st.error(f"State '{state}' not found in the dataset. Please check the spelling and try again.")
    else:
        st.write('Please enter a state name to display the trend.')