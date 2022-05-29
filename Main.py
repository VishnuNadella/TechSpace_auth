import streamlit as st
from streamlit_option_menu import option_menu

class router:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        lst = [i["title"] for i in self.apps]
        selected = option_menu(
            menu_title = None,
            options = lst,
            icons = ["None", "None", "None", "None", "None", "None"],
            default_index = 0, 
            orientation = "horizontal",
        )
        self.apps[lst.index(selected)]["function"]()
        