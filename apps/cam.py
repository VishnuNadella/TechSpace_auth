import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
from pymongo import *
import dns


usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]
cluster = MongoClient(f"mongodb+srv://{usn}:{pwd}@cluster01.0kzr6.mongodb.net/?retryWrites=true&w=majority")

def decoder(image):
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
def capture():
    message = st.empty()
    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')
    if startcam:
        img = Image.open(startcam)
        data = decoder(img)
def check():
    pass
def app():
    st.title("Camera Page")
    st.subheader("If camera dosent work then try switching between and activating the rear camera")
    select_event = st.selectbox("Switch Conditions and try", ["Select an Event", "1", "2", "3"])
    if select_event != "Select an Event":
        res = capture()
        st.info(res)
        check()
