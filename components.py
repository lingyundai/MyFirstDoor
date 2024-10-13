import streamlit as st

def title():
    st.sidebar.title("Welcome to MyFirstDoor", anchor=False)

def main_subtitle(text):
    st.subheader(text)

def sidebar_subtitle(text):
    st.sidebar.subheader(text)

def user_input(content, placeholder, helpMessage):
    value = st.sidebar.number_input(content,
                            placeholder=placeholder,
                            help=helpMessage, step=0)
    return float(value)

def generate():
    st.sidebar.button("Generate budget")

def user_slider(content, helpMessage):
    value = st.slider(content, 
                      min_value=0, max_value=10,
                            help=helpMessage)
    return int(value)