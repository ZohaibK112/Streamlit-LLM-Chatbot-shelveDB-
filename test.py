import streamlit as st

# Set default theme (Light Mode)
st.set_page_config(page_title="Your App", page_icon="🌟", layout="centered", initial_sidebar_state="expanded")

# Toggle between Light and Dark theme using radio button
theme = st.radio("Choose Theme", ["Light", "Dark"])

if theme == "Light":
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
