import streamlit as st
from results import show_results_page
from inputs import show_input_page

st.set_page_config(
    page_title="UK Financial Planning Tool", page_icon="£", layout="wide"
)

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Input", "Results"])

# Show the selected page
if page == "Input":
    show_input_page()
elif page == "Results":
    show_results_page()