import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
from pymongo import *
import dns

from time import sleep

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]
cluster = MongoClient(f"mongodb+srv://{usn}:{pwd}@cluster01.0kzr6.mongodb.net/?retryWrites=true&w=majority")

def decoder(image):
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
        print(data)
def capture():
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        img = Image.open(startcam)
        print("Final Result", decoder(img))

def app():
    st.title("Initiate Camera")
    st.subheader("Switch to Back Camera")
    capture()
