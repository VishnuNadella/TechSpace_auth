"""
Main navigating page for the event co-ordinators
"""

import streamlit as st
from Main import router
from apps import home, attendance, log, meals, events, view, auth
import bcrypt as bc
import json
data = None


fl = open("admin_login.json")
data = json.load(fl)

fl.close()

LOGO_adr = "./apps/resources/edam-logo.png"

st.set_page_config(page_title = "TechSpace'22", page_icon = LOGO_adr, initial_sidebar_state = 'auto')

app = router()

st.markdown("""
# TechSpace'22
""")

st.sidebar.image(LOGO_adr)
st.sidebar.markdown(
    """<div style="text-align:center"><strong>e-DAM</strong><br><br></div>""", unsafe_allow_html=True)

st.sidebar.markdown(
    '''<br><br><div style="text-align: center"><small>Developed by TechSpace'22 Backend Team | May 2022 </small></div>''', unsafe_allow_html=True)


app.add_app("home", home.app)
app.add_app("attendance", attendance.app)
app.add_app("meals", meals.app)
app.add_app("events", events.app)

salt = bc.gensalt()
       
dets = auth.auth()

try:
    if dets != None or st.session_state["Status"]:
        membes = st.session_state["Name"]
        pwds = st.session_state["pwd"]
        hashed = None
        for i in data:
            if i["Name"] == membes:
                hashed = i["Password"]
        
        pwd = pwds.encode('utf-8')
        hashed = hashed.encode('utf-8')
        if (membes == "Vishnu" and bc.checkpw(pwd, hashed)) or (membes == "Hemanth" and bc.checkpw(pwd, hashed)) or (membes == "Abhishek" and bc.checkpw(pwd, hashed)): # replace with pwd
            st.session_state["Status"] = True
            st.sidebar.success(f"Logged in as {membes}")
            app.add_app("log", log.app)
            app.add_app("view", view.app)
            sts = st.sidebar.button("Log out")
            if sts:
                del st.session_state["Name"]
                del st.session_state["Status"]
                del st.session_state["Password"]
        else:
            st.sidebar.error("Invalid Admin Credentials")
except Exception as e:
    print(e)
app.run()
