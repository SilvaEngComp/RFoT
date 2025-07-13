# ui_components/intel_lab.py
import streamlit as st
import pandas as pd

def show_intel_lab_dataset():
    st.header("Temperature from Intel Lab Dataset")
    df = pd.read_csv('data/intel_lab.csv', delimiter=",")
    st.dataframe(df)