"""
Authentication page for selected pages
"""


import streamlit as st
import pymongo


def auth():
    st.sidebar.title("Login")
    st.sidebar.write("Only for admins")
    username = st.sidebar.text_input('username')
    password = st.sidebar.text_input('Password', type = "password")
    # Fletch data from database and check
    if "Name" not in st.session_state:
        st.session_state["Name"] = None
        st.session_state["pwd"] = None
        st.session_state["Status"] = False
        # print(st.session_state)
    if st.sidebar.button("Login"):
        st.session_state["Name"] = username
        st.session_state["pwd"] = password
        return True, username, password