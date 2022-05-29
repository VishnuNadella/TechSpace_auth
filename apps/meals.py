import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
from pymongo import *
import dns

from time import sleep

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]
cluster = MongoClient(f"mongodb+srv://{usn}:{pwd}@cluster01.0kzr6.mongodb.net/?retryWrites=true&w=majority")


db = cluster["test_TechSpace"]
collection = db["People"]


def mark(id):
    per = collection.find({"dum_id": id})
    req = None
    for i in per:
        req = i
    if req != None:
        mls = req["meals"]
        st.info(mls)
        cnt = 5
        for i in range(1, 6):
            stri = f"meal{i}"
            chk = mls[stri]
            cnt -= 1
            if chk == False:
                collection.update_one({"dum_id" : id }, {"$set" : {f"meals.{stri}" : True}})
                st.success(f"Scan Complete! More {cnt} are left.")
                break
        else:
            st.error("You have exhausted all your coupons")
    else:
        print("req is None")

def decoder(image):
    st.info("Inside decoder function")
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
        st.success(data)
        mark(data)
def capture():
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        st.info("Inside startcam condition")
        img = Image.open(startcam)
        print("Final Result", decoder(img))

def app():
    st.title("Scan for Meals")
    capture()
