"""
This is to view the database data in aa tabular form
or
Visual representation of the data
This page is in need of authentication
"""

import streamlit as st
from pymongo import *
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]
cluster = MongoClient(f"mongodb+srv://{usn}:{pwd}@cluster01.0kzr6.mongodb.net/?retryWrites=true&w=majority")

db = cluster["test_TechSpace"]

collection = db["People"]

def commit(id, whr = None, column = None, Key = None):
    per = collection.find({"id": id})
    req = None
    for i in per:
        req = i
    if whr == "events":
        req = req["events"][0]
        # come up with an algorithm For Now its done
        if column == "attendance":
            keys = [k for k in req.keys()]
            prev = keys.index(Key)
            Key = keys[prev + 1]
        cng = not req[Key]
        collection.update_one({"id" : id }, {"$set" : {f"events.0.{Key}" : cng}})
        st.success("Commited Changes!!")
    elif whr == "meals":
        req = req["meals"][0]
        print(req, "\n\n\n")
        print(req[whr])


def which_one(dict1, dict2):
    if len(dict1) == len(dict2):
        l = len(dict1)
        for i in range(l):
            if dict1[i] != dict2[i]:
                return i

def database_find(id):
    collection = db["People"]
    fnd = collection.find({"id" : id})
    entries=list(fnd)
    entries[:]
    df=pd.DataFrame(entries)
    events_df = df.events[0][0]
    meals_df = df.meals[0]
    return events_df, meals_df

def custom(eve):
    main_tbl = eve
    eve_tbl = pd.DataFrame(main_tbl)
    atten_tbl = pd.DataFrame(main_tbl)
    
    atten_tbl.drop("keynote1", axis = 0, inplace = True)
    atten_tbl.drop("keynote2", axis = 0, inplace = True)
    atten_tbl.drop("standup", axis = 0, inplace = True)
    atten_tbl.drop("hackathon", axis = 0, inplace = True)
    atten_tbl.drop("internship", axis = 0, inplace = True)
    atten_tbl.drop("workshop1", axis = 0, inplace = True)
    atten_tbl.drop("workshop2", axis = 0, inplace = True)

    eve_tbl.drop("attendk1", axis = 0, inplace = True)
    eve_tbl.drop("attendk2", axis = 0, inplace = True)
    eve_tbl.drop("attendsu", axis = 0, inplace = True)
    eve_tbl.drop("attendhtn", axis = 0, inplace = True)
    eve_tbl.drop("attendis", axis = 0, inplace = True)
    eve_tbl.drop("attendw1", axis = 0, inplace = True)
    eve_tbl.drop("attendw2", axis = 0, inplace = True)
    eve_tbl.insert(0, "id", range(1, len(eve_tbl) + 1))
    atten_tbl.insert(0, "id", range(1, len(atten_tbl) + 1))
    atten_tbl.rename(columns = {"Status" : "Attendance"}, inplace = True)
    eve_tbl.rename(columns = {"Status" : "Paid"}, inplace = True)
    atten_tbl.drop("Events", axis = 1, inplace = True)

    eve_tbl.Events[eve_tbl.Events == "keynote1"] = "KeyNote 1"
    eve_tbl.Events[eve_tbl.Events == "keynote2"] = "KeyNote 2"
    eve_tbl.Events[eve_tbl.Events == "standup"] = "Stand Up Comedy"
    eve_tbl.Events[eve_tbl.Events == "hackathon"] = "Hackathon"
    eve_tbl.Events[eve_tbl.Events == "internship"] = "Internship Fair"
    eve_tbl.Events[eve_tbl.Events == "workshop1"] = "Workshop 1"
    eve_tbl.Events[eve_tbl.Events == "workshop2"] = "Workshop 2"
    req = pd.merge(eve_tbl, atten_tbl, on = ["id"])
    grid = AgGrid(req, editable = True, update_mode = GridUpdateMode.MODEL_CHANGED, theme = "dark")
    paid_cng = grid["data"]["Paid"]
    atten_cng = grid["data"]["Attendance"]
    
    return dict(paid_cng), dict(atten_cng)

def check_change(id, eve):
    paid_d, _ = database_find(id)
    paid_c, atten_c = custom(eve)
    del paid_d["tm_name"]
    new_atten = {}
    new_paid = {}
    c = 0
    cnt = 0
    for k, v in paid_d.items():
        if c % 2 != 0:
            new_atten[cnt] = str(v).capitalize()
            cnt += 1
        c += 1
    c = 0
    cnt = 0
    for k, v in paid_d.items():
        if c % 2 == 0:
            new_paid[cnt] = str(v).capitalize()
            cnt += 1
        c += 1
    paid_cn = {}
    atten_cn = {}
    for k, v in paid_c.items():
        paid_cn[k] = str(v).capitalize()
    for k, v in atten_c.items():
        atten_cn[k] = str(v).capitalize()
    which = {0 : "keynote1", 1 : "keynote2", 2 : "standup", 3 : "hackathon", 4 : "internship", 5 : "workshop1", 6 : "workshop2"}
    if new_paid != paid_cn and st.button("Commit Changes"):
        Key = which_one(new_paid, paid_cn)
        Key = which[Key]
        commit(id, whr = "events", column = "paid", Key = Key)
    elif new_atten != atten_cn and st.button("Commit Changes"):
        Key = which_one(new_atten, atten_cn)
        Key = which[Key]
        commit(id, whr = "events", column = "attendance", Key = Key)

    

def header():
    st.markdown("""
    ## Welcome Admin
    """)

def app():
    header()

    cursor = collection.find()
    entries=list(cursor)
    entries[:]
    df=pd.DataFrame(entries)
    df.drop("_id", axis = 1, inplace = True)
    df.drop("events", axis = 1, inplace = True)
    df.drop("meals", axis = 1, inplace = True)
    df.drop("dum_id", axis = 1, inplace = True)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled = True)
    gb.configure_default_column(editable = True, groupable = True)

    what = gb.configure_selection(use_checkbox = True)
    grid_options = gb.build()
    grid = AgGrid(df, editable = False, gridOptions = grid_options, update_mode = GridUpdateMode.SELECTION_CHANGED, theme = "dark")
    her_req = None
    try:
        her_req = grid["selected_rows"][0]
        her_req = her_req["id"]
    except:
        pass
    try:
        eve, mls = database_find(her_req)
        eve = pd.DataFrame(eve, index = [0])
        mls = pd.DataFrame(mls, index = [0])
        eve.drop("tm_name", axis = 1, inplace = True)
        lst_eve = [i for i in eve]
        lst_mls = [i for i in mls]
        eve, mls = eve.T, mls.T
        eve.columns = ["Status"]
        mls.columns = ["Status"]
        eve.insert(0, "Events", lst_eve)
        mls.insert(0, "Meals", lst_mls)
        # custom(eve)
        check_change(her_req, eve)
        AgGrid(mls, editable = True , theme = "dark")
    except:
        pass
