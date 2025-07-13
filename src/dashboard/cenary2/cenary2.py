# ui_components/intel_lab.py
import streamlit as st
import pandas as pd
from time import sleep
from src.current_model.pool import Pool

class Cenary2:
    @staticmethod
    def show_data_collected():
        st.header("# Registred Data")
        pool = Pool()
        transactions = pool.get()
        st.write("# There are ",str(len(transactions))+" block of transactions")
        st.write(transactions)
    @staticmethod
    def dataset_training():
        df = pd.read_csv('dataset.csv', delimiter=",")
        st.dataframe(df)
    @staticmethod
    def training_results():
        st.header("Current IoT time proccess")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('prediction.csv', delimiter=",")
        edit_df = st.data_editor(df,key="df_editor", on_change=def_on_change, args=[df])
        
        st.line_chart(df,color=['blue','red'])
                
        while True:
            sleep(5)
            df = pd.read_csv('../prediction.csv', delimiter=",")
    # Define a function to update the dataframe based on user edits
    def def_on_change(df):
        state = st.session_state["df_editor"]
        for index, change_dict in state["edited_rows"].items():
            df.loc[df.index == index, "edited"] = True

        if st.sidebar.button("Consumer Dataset"):
            st.header("Temperature from Intel Lab Dataset")
            df = pd.read_csv('dataset.csv', delimiter=",")
            st.dataframe(df)