"""
To log people before and during the event (add people to database)
This page needs authentication
"""


import streamlit as st
from pymongo import *
cluster = MongoClient(f"mongodb+srv://VishnuNad:{psd}@cluster01.0kzr6.mongodb.net/test")

db = cluster["test_TechSpace"]

collection = db["People"]



def header():
    st.markdown("""
    ## Log entries here
    """)


def team_count(name):
  tm_cnt = 0
  
  col = db["People"]
  for i in col.find({}):
      ned = i["events"][0]
      if ned["tm_name"] == name:
          print(ned["tm_name"])
          tm_cnt += 1
  return tm_cnt

def find_for(_for, chk): # return true if duplicate found
  cursor = collection.find()
  for req in cursor:
    res = (req.get(_for))
    print(res)
    if res == chk:
      return True
  return False


def find_dup(to_check):
  if str(to_check).isnumeric():
    if find_for("contact", to_check):
      return True # since it did found a duplicate
  elif "@" in to_check and ".com" in to_check:
    if find_for("mail", to_check):
      return True
  return False

def app():
    header()
    cnt = collection.count_documents({})
    print(cnt)
    name = st.text_input("Enter your Name: ")
    contact = None
    try:
      cont_req = int(st.text_input("Enter your contact: "))
      if find_dup(cont_req) == False:
        contact = cont_req
      else:
        st.warning("Contact already exists, No Duplicates allowed")
    except:
      pass
    mail_req = st.text_input("Enter your mail: ")
    mail = None
    if find_dup(mail_req) == False:
      mail = mail_req
    else:
      st.warning("Email already exists, No Duplicates allowed")
    
    clg = st.selectbox("College", ["Select", "CBIT", "IARE", "JNTU"])
    if clg == "Select":
        st.error("Select a College")
    ks1 = st.checkbox("Keynote Session 1", value = False)
    ks2 = st.checkbox("Keynote Session 2", value = False)
    suc = st.checkbox("Stand Up", value = False)
    htn = st.checkbox("Hackathon", value = False)
    t_nme = None
    cnd = False
    if htn:
        tm_name = st.text_input("")
        tm_mem_cnt = team_count(tm_name)
        if tm_mem_cnt < 4 and tm_name != "":
            st.success("You are added into the team")
            t_nme = tm_name
        elif tm_name != "" and tm_mem_cnt >= 4:
            cnd = True
            st.warning("Team Limit has been exceeded; Create or Find a new team")
    isp = st.checkbox("Internship", value = False)
    w1 = st.checkbox("Workshop 1", value = False)
    w2 = st.checkbox("Workshop 2", value = False)
    print((4 - len(str(cnt))) * "0" + str(cnt + 1))
    fin = {"id" : clg + (4 - len(str(cnt))) * "0" + str(cnt), "name": name, "contact": contact, "mail" : mail, "college_name" :clg, "events" : [
    {
      "keynote1": ks1,
      "attendk1": False,
      "keynote2": ks2,
      "attendk2": False,
      "standup": suc,
      "attendsu": False,
      "hackathon": htn,
      "attendhtn": False,
      "tm_name": t_nme,
      "internship": isp,
      "attendis": False,
      "workshop1": w1,
      "attendw1": False,
      "workshop2": w2,
      "attendw2": False
    }
  ],
  "meals": {
    "meal1": False,
    "meal2": False,
    "meal3": False,
    "meal4": False,
    "meal5": False
  },
  "attend": False,
  "dum_id": None
  }
    btn = st.button("Submit")
    if btn and t_nme != None:
      collection.insert_one(fin)
      st.success("Successfully Added")
    elif btn and t_nme == None and cnd:
      st.error("Team Limit Exceeded")
