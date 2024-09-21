import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
from src.proposed_model.smart_contract_3 import SC3
from src.current_model.pool import Pool
from time import sleep
import base64




def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

logo = image_to_base64("images/logo_url.png")

logo2 = image_to_base64("images/wiser.png")

# Custom CSS to inject for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define a function to update the dataframe based on user edits
def def_on_change(df):
    state = st.session_state["df_editor"]
    for index, change_dict in state["edited_rows"].items():
        df.loc[df.index == index, "edited"] = True

# Set Streamlit page configuration
st.set_page_config(page_title="RFoT Dashboard", page_icon=logo, layout="wide")

# Apply custom CSS for styling
local_css("style.css")

st.header("RFoT Dashboard")
# st.sidebar.image(logo, width=150)

# Inject custom HTML for the top right image
st.markdown("""
    <div class="top-right-image">
        <img src="/images/wiser.png" alt="Top Right Image">
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
if st.sidebar.button("Current IoT Data"):
    st.header("# Registred Data")
    pool = Pool()
    transactions = pool.get("../src/current_model")
    st.write("# There are ",str(len(transactions))+" block of transactions")
    st.write(transactions)

if st.sidebar.button("Blockchain Data"):
    st.header("# Data Blockchain")
    st.text("This is the data collected and registred in BCD (Data Blockchain)")
    blockchain = SC3.getBCD("h1")
    
    st.write("# There are ",str(len(blockchain.chain))+" blocks")
    st.write(blockchain.toJsonDecrypted())

if st.sidebar.button("No Blockchain Data"):
    st.header("# Data Blockchain")
    st.text("This is the data collected and registred in BCD (Data Blockchain)")
    pool = Pool()
    chain = pool.getDecrypted()
    st.write("# There are ",str(len(chain))+" blocks")
    st.write(chain)
if st.sidebar.button("Consumer Dataset"):
    st.header("Temperature from Intel Lab Dataset")
    df = pd.read_csv('dataset.csv', delimiter=",")
    st.dataframe(df)
if st.sidebar.button("Comparing Time operation"):
    col1,col2 = st.columns(2)
    with col1:
        st.header("Current IoT time proccess")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../../current_model/commom_IoT_collector.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 5")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../../proposed_model/RFoT_collector_challenge_5.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 7")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../../proposed_model/RFoT_collector_challenge_7.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
    with col2:
        st.header("RFoT time proccess challenge 4")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../../proposed_model/RFoT_collector_challenge_4.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess challenge 6")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../../proposed_model/RFoT_collector_challenge_6.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))

if st.sidebar.button("Training results"):
    st.header("Current IoT time proccess")
    st.text("Collect and store time registration monitored by running simulation")
    df = pd.read_csv('prediction.csv', delimiter=",")
    edit_df = st.data_editor(df,key="df_editor", on_change=def_on_change, args=[df])
    
    st.line_chart(df,color=['blue','red'])
            
    while True:
        sleep(5)
        df = pd.read_csv('../prediction.csv', delimiter=",")
   
