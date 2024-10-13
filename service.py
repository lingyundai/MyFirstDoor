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

def parse_property_data(data_string):
    if not data_string:
        return []
    else:
        # Remove the outer brackets and split by "},{"
        items = data_string.strip('[]').split('},{')
        
        # Add back the curly braces that were removed in the split
        items = ['{' + item + '}' for item in items]
        items[0] = items[0].lstrip('{')
        items[-1] = items[-1].rstrip('}')
        
        # Parse each item as a dictionary
        parsed_data = []
        for item in items:
            try:
                parsed_item = json.loads(item)
                
                # Handle the parsing error in the schools field
                if 'schools' in parsed_item:
                    try:
                        # Replace single quotes with double quotes and ensure proper JSON format
                        schools_str = parsed_item['schools'].replace("'", '"')
                        schools_str = schools_str.replace('None', 'null')  # Replace None with null for JSON compatibility
                        parsed_item['schools'] = json.loads(schools_str)
                    except json.JSONDecodeError:
                        st.error(f"Error parsing schools data for property {parsed_item['unique_id']}: {parsed_item['schools']}")
                        parsed_item['schools'] = []
                
                parsed_data.append(parsed_item)
            except json.JSONDecodeError:
                st.error(f"Error parsing item: {item}")
    
    return parsed_data