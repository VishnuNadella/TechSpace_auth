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


def check(selected_event = None, id = None):

    per = collection.find({"dum_id": id})

    req = None
    for i in per:
        req = i
        break
    else:
        req = "Nothing"
    
    mapping = {"keynote speaker session 1": "keynote1", "keynote speaker session 2": "keynote2", "Stand Up Comedy" : "standup", "Hackathon" : "hackathon", "Internship Fair" : "internship", "Workshop 1" : "workshop1", "Workshop 2" : "workshop2"}
    attend_mapping = {"keynote speaker session 1": "attendk1", "keynote speaker session 2": "attendk2", "Stand Up Comedy" : "attendsu", "Hackathon" : "attendhtn", "Internship Fair" : "attendis", "Workshop 1" : "attendw1", "Workshop 2" : "attendw2"}
    st.info(req)
    if len(req) != 0 and req != "Nothing":
        nm = req["name"]
        req = req["events"][0]
        if req[mapping[selected_event]] != False: # paid or not
            if req[attend_mapping[selected_event]] == False: # present or not
                print(attend_mapping[selected_event]) 
                nd = attend_mapping[selected_event]
                collection.update_one({"dum_id" : id }, {"$set" : {f"events.0.{nd}" : True}})
                st.success(f"Welcome {nm}, Enjoy the Event") 
            elif req[attend_mapping[selected_event]] == True:
                st.warning("Duplicate Entry")
        elif req[mapping[selected_event]] == False:
            st.error("You havent paid for this event")
    else:
        st.error("User dosent Exist in DB")


def decoder(image):
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
        st.info(data)
        return data

def capture():
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        img = Image.open(startcam)
        data = decoder(img)
        return data

def app():
    st.title("Events Page")
    select_event = st.selectbox("Select Event", ["Select an Event", "keynote speaker session 1", "keynote speaker session 2", "Stand Up Comedy", "Hackathon", "Internship Fair", "Workshop 1", "Workshop 2"])
    if select_event != "Select an Event":
        res = capture()
        st.info(res)
        check(selected_event = select_event, id = res)
    elif select_event == "Select an Event":
        st.error("Please Select an Event")
