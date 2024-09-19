import streamlit as st
from src.proposed_model.smart_contract_3 import SC3
import json
from src.proposed_model.blockchain import Blockchain
import pandas as pd
from src.current_model.pool import Pool
import matplotlib.animation as animation
from time import sleep

def def_on_change(df):
    state = st.session_state["df_editor"]
    for index, change_dict in state["edited_rows"].items():
        df.loc[df.index==index, "edited"]=True


logo = "data:image/png;base64,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"
st.set_page_config(
    page_title="RFoT Dashboard", 
                   page_icon=logo,
                   layout="wide")
st.header("RFoT Dashboard")
st.sidebar.image(logo,width=150)
if st.sidebar.button("Intel Lab Dataset "):
    st.header("Temperature from Intel Lab Dataset")
    df = pd.read_csv('../intel_lab.csv', delimiter=",")
    st.dataframe(df)
if st.sidebar.button("Current IoT Data"):
    st.header("# Registred Data")
    pool = Pool()
    transactions = pool.get('../current_model/')
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
        df = pd.read_csv('../current_model/commom_IoT_collector.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 5")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_5.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess  challenge 7")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_7.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
    with col2:
        st.header("RFoT time proccess challenge 4")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_4.csv', delimiter=",")
        if df is not None:
            st.dataframe(df.astype(str))
        
        st.header("RFoT time proccess challenge 6")
        st.text("Collect and store time registration monitored by running simulation")
        df = pd.read_csv('../proposed_model/RFoT_collector_challenge_6.csv', delimiter=",")
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
        df = pd.read_csv('prediction.csv', delimiter=",")
   


def plotGraph():
    df = pd.read_csv('prediction.csv', delimiter=",")
    fig1 = plt.figure()
    fig1.set_size_inches(10.5,8.5)

    a1 = fig1.add_subplot(513)
    a2 = fig1.add_subplot(515)
    a3 = fig1.add_subplot(511)
    animation.FuncAnimation(fig1, graphicGenarete1(Y_test,Y_pred), interval=1000)
    animation.FuncAnimation(fig1, graphicGenarete2(Y_test,Y_pred), interval=1000)
    animation.FuncAnimation(fig1, graphicGenarete3(Y_test,Y_pred), interval=1000)
    plt.show(block=False)
    plt.pause(3)
    
def graphicGenarete1(self,Y_test,Y_pred):
    print('preparing graphic...')
    self.a1.clear()
    self.a1.set_title("Predito Vs Real")
    self.a1.plot(Y_test.flatten(), marker='.', label='true')
    self.a1.plot(Y_pred.flatten(),'r',marker='.', label='predicted')
    self.a1.legend();   
    # print('graphic prepered...')
        
def graphicGenarete2(self,Y_test,Y_pred):
    size = np.min([Y_pred.shape[0],Y_test.shape[0] ])
    rmse =  mean_squared_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size], squared=False)
    mae =  mean_absolute_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
    median_mae = median_absolute_error(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
    evs = explained_variance_score(Y_test.flatten()[0:size], Y_pred.flatten()[0:size])
    
    objects = ['rmse', 'mae', 
                'median-mae']
    y_pos = np.arange(3)
    performance = [rmse,mae,median_mae]

    self.a2.clear()
    self.a2.set_title("Métricas")
    self.a2.bar(objects, performance, align='center')
    self.a2.legend(); 
    
def graphicGenarete3(self,Y_test,Y_pred):
    fper, tper, tresholds = roc_curve(Y_test.flatten(),Y_pred.flatten())
    self.a3.clear()
    self.a3.set_title("ROC")
    self.a3.plot(fper, marker='.', label='False Positive Rate')
    self.a3.plot(tper,'r',marker='.', label='True Positive Rate')
    self.a3.plot(tresholds,'g',marker='.', label='treshold')
    self.a3.legend(); 