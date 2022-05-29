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


def check(id):
    per = None
    if id != "None" or id != False:
        per = collection.find({"id": id})
    req = None
    for i in per:
        req = i
    nm = None
    if req == None:
        st.error("User Dosent Exists or Scan once again")
        return "UDE"
    elif len(req) != 0:
        nm = req["name"]
        if req["attend"] == False:
            collection.update_one({"id" : id }, {"$set" : {"attend" : True}})
            st.success(f"Welcome {nm}; Enjoy")
        elif req["attend"] == True:
            st.warning("Person Already Exist")
            return "PAE"
        else:
            st.error("Person Dosent Exists in Database")
    return nm   

def decoder(image):
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
        if len(data) > 0 and "dup" not in data:
            print("Bar code", qrCode)
            st.success("Attendance allocated")
            sleep(5)
            return data
        elif "dup" in data:
            print("dup", data)
            st.success("ID card has been successfully allocated")
            sleep(5)
            return data

def capture():
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        st.info("Inside capture")
        img = Image.open(startcam)
        data = decoder(img)
        st.info(data)
        if "id" not in st.session_state:
            st.session_state["id"] = None
        if "dum" not in st.session_state:
            st.session_state["dum"] = None
        st.info(st.session_state)

        if data != None:
            st.info("Inside if data cond")
            if st.session_state["id"] == None:
                st.session_state["id"] = data
                
            elif "dup" in data and st.session_state["id"] != None:
                st.session_state["dum"] = data
                needed = {"id" : st.session_state["id"], "dum" : st.session_state["dum"]}
                del st.session_state["id"]
                del st.session_state["dum"]
                st.info(needed)
                return needed
            elif "dup" in data and st.session_state["id"] == None:
                st.error("Please folllow the sequence\n    1.Scan Person's QR\n    2.Scan ID Card QR")

def app():
    st.title("QR Code Scanner")
    st.text("Scan the person's QR code")   
    cap1 = capture()
    if cap1 != None:
        cap_id = cap1["id"]
        cap_dup = cap1["dup"]
        if cap1 == None:
            st.error("Either Invalid QR code or Scan it again")
        elif cap1:
            nm = check(cap_id)
            if nm != "PAE" and nm != "UDE":
                cap2 = cap_dup
                collection.update_one({"id" : cap_id }, {"$set" : {f"dum_id" : cap2}}) # Replace True with ID card id

                st.success(f"Welcome {nm}")
