import os
import json
import streamlit as st
import pandas as pd
import base64

def def_on_change(df):
        state = st.session_state["df_editor"]
        for index, change_dict in state["edited_rows"].items():
            df.loc[df.index == index, "edited"] = True

        if st.sidebar.button("Consumer Dataset"):
            st.header("Temperature from Intel Lab Dataset")
            df = pd.read_csv('dataset.csv', delimiter=",")
            st.dataframe(df)

def readFile(fileName):
    prefix = os.path.dirname(os.path.abspath(__file__))
    path = str(prefix+"/"+fileName)
    try:
        with open(path) as file:
            if os.path.getsize(path) > 0:
                return json.load(file)
            else:
                return []
    except Exception as e:
        print(e)

# Function to get base64 encoding of local image file
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return str("data:image/png;base64,"+base64.b64encode(img_file.read()).decode('utf-8'))