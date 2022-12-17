# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
from PIL import Image
import sqlite3
from sqlite3 import Error
import time
from statistics import mean
import datetime

from pyecharts.charts import Bar
from pyecharts import options as opts
import streamlit.components.v1 as components

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

data = "database_patients.csv"

# impostazione grafica iniziale

st.set_page_config(page_title="Customer Satisfaction", page_icon="📌", layout="centered")
#st.sidebar.header("Feedback reporting")

st.title("Customer Satisfaction CX")
st.write("Vediamo alcune informazioni sul tool Customer Satisfaction Analyzer")


with st.expander("ℹ️ Istruzioni generali", expanded=False):
    st.markdown(
        """
        ## Informazioni Tool CSA
        L'obiettivo di questo tool è quello di fornire uno strumento per una misurazione
        della soddsifazione dei pazienti
        """
    )
    st.markdown("")
    st.markdown(
        """
        ## Perchè misurare Customer Satisfaction?
        L'efficacia di un'iniziativa di business non è data solo dalla misurazione degli outcome (es. revenue),
        1. Miglioramento percepito della Customer Experience dei prodotti e servizi creati e lanciati rispetto al passato
        2. Miglioramento dell'Employee Experience portata dal nuovo framework operativo
        3. Miglioramento della performance di business (Outcome) - revenue, costi ecc
        """
    )
    st.markdown("")
    #st.image(image)
st.write("")

def CustomerSatisf(a):
    k=mean(a)
    return k

df = pd.read_csv(data)

# creazione webform

form = st.form(key="annotation", clear_on_submit = True,)
with form:
    cols = st.columns((1, 1))
    author = cols[0].text_input("Autore feedback:")
    bug_type = cols[1].selectbox(
        "Tipologia Annotazione:", ["Feedback", "Suggerimento", "Segnalazione Errore", "Altro"], index=2)
    comment = st.text_area("Commenti:")
    cols = st.columns(2)
    date = cols[0].date_input("Quando è avvenuto l'annotazione o il problema:")
    satisf = cols[1].slider("Grado di soddisfazione dei tool :", 1, 100, 2)
    cols = st.columns(2)
    marchio = cols[0].slider("Riconoscibilità marchio:", 1, 100, 2)
    engagment = cols[1].slider("Engagment del User:", 1, 100, 2)
    submitted = st.form_submit_button(label="Submit")
    if submitted==True:
        datetime_object = datetime.datetime.now()
        st.success("Successfully")
        new_data={"Timestamp": str(datetime_object),
                  "Author":author, 
                  "Annotazione":bug_type,
                  "Commenti": comment,
                  "Date": date,
                  "Soddisfazione": satisf,
                  "Marchio": marchio,
                  "Engagment": engagment}
        df = df.append(new_data, ignore_index=True)
        df.to_csv(data, index=False)

        if bug_type=="Feedback":
            #df_count = df.iloc[1:]
            #st.write(df)
            soddMean=round(mean(df['Soddisfazione']))
            marcMean=round(mean(df['Marchio']))
            engaMean=round(mean(df['Engagment']))
            prov2=len(df)
            CustomSatisf=round((soddMean+marcMean+engaMean)/(3))
        

            st.write("## Results analysis")
            st.write(prov2)
            st.balloons()
