# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
from PIL import Image
import time
from statistics import mean
import datetime

import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest


image = Image.open('images/Medical_Logo.png')
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()


# impostazione grafica iniziale

st.set_page_config(page_title="MeHEDI", page_icon="📌", layout="wide")
#st.sidebar.header("Feedback reporting")

t1, t2 = st.columns((0.07,1)) 

t1.image(image, width = 180)
t2.title("MedTech Expereince Dashboard - MedMIB Hospital")
t2.markdown("Vediamo alcune informazioni sul tool Patient Satisfaction Analyzer")

df = connect_to_gsheet()
st.write(df)

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


#st.write(df)


def CustomerSatisf(a):
    k=mean(a)
    return k

#df = pd.read_csv(data)

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
        add_row_to_gsheet(
        df, [[author, bug_type, comment, str(date), satisf, engagment, str(datetime_object)]])


        #soddMean=round(mean(df['Soddisfazione']))
        #marcMean=round(mean(df['Marchio']))
        #engaMean=round(mean(df['Engagment']))
        #prov2=len(df)
        #CustomSatisf=round((soddMean+marcMean+engaMean)/(3))
        

        st.write("## Results analysis")
        a, b = st.columns(2)

        with a:
            st.write("CUSTOMER SATISFACTION")
        with b:
            st.write("NUMERO REPORT FATTI")
        st.balloons()
