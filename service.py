import streamlit as st
import json

def load_session_state_from_json(file_path="state.json"):
    try:
        with open(file_path, 'r') as f:
            session_data = json.load(f)
        for key, value in session_data.items():
            if key not in st.session_state:
                st.session_state[key] = value
    except FileNotFoundError:
        st.write("No session state saved yet.")
    except json.JSONDecodeError:
        st.write("Error loading session state from JSON.")