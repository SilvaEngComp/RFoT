# ui_components/intel_lab.py
import streamlit as st
import pandas as pd
from time import sleep
from src.dashboard.cenary4.smart_contract_3 import SC3
from src.dashboard.cenary4.corruptedBlockchain import CorruptedBlockchain
from src.dashboard.cenary4.blockchain import Blockchain
class Cenary4:
    @staticmethod
    def show_data_collected():
        st.header("# Blockchain Válida")
        st.text("This is the data collected and registred in BCD (Data Blockchain)")
        blockchain = SC3.getBCD()
        
        st.write("# There are ",str(len(blockchain.chain))+" blocks")
        st.write(Blockchain.toJsonDecrypted(blockchain.chain))

    @staticmethod
    def show_corrupted_data_collected():
        
        st.header("# Blockchain Corrompida")
        nodes = CorruptedBlockchain.getBlockchainFileNames()
        print(nodes)
        if(nodes):
            for node in nodes:
                st.write(f'# Nome: {node}')
                chain = CorruptedBlockchain.getLocalBLockchainFile(node)
                st.write("### Contem ",str(len(chain['chain']))+" blocks")
                st.write(chain['chain'])
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