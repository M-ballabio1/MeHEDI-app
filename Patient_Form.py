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

t1, t2 = st.columns((1, 0.15)) 

t1.title("MedTech Hospital Experience Dashboard - MedMIB Hospital")
t1.markdown("### This section shows some information about MeHEDI - Tool of Patient Satisfaction")
t2.image(image, width = 150)

#append pages
#st.sidebar.success("Select a page above.")

# connect and append data
df = connect_to_gsheet()
expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(df))

with st.expander("ℹ️ Istruzioni generali", expanded=False):
    st.markdown(
        """
        ## Informazioni Tool MeHEDI
        L'obiettivo di questo tool è quello di fornire uno strumento per una misurazione
        della soddsifazione dei pazienti
        """
    )
    st.markdown("")
    st.markdown(
        """
        ## Perchè misurare Patients Satisfaction?
        L'efficacia di un'iniziativa di business non è data solo dalla misurazione degli outcome (es. revenue),
        1. Miglioramento percepito della Customer Experience dei prodotti e servizi creati e lanciati rispetto al passato
        2. Miglioramento dell'Employee Experience portata dal nuovo framework operativo
        3. Miglioramento della performance di business (Outcome) - revenue, costi ecc
        """
    )
    st.markdown("")
    #st.image(image)
st.write("")


# creazione webform

form = st.form(key="annotation", clear_on_submit = True,)
with form:
    cols = st.columns((1, 1, 1))
    
    #info paziente
    author = cols[0].text_input("Nome del paziente:")
    eta = cols[1].text_input("Età anagrafica:")
    sesso = cols[2].selectbox(
        "Sesso:", ["Maschio", "Femmina", "Non specificato"], index=2)
    #email = cols[3].text_input("Età anagrafica:")
    
    cols2 = st.columns((4))
    #infrastruttura fisica tecnologica
    date = cols2[0].date_input("Quando è stato in ospedale:")
    infras = cols2[1].slider("Qualità della struttura ospedaliera :", 1, 100, 1)
    proces = cols2[2].slider("Qualità dei processi clinici amministrativi :", 1, 100, 1)
    sicurezza = cols2[3].slider("Sicurezza ospedale :", 1, 100, 1)
    
    cols3 = st.columns((1, 1, 1, 1))
    #risorse umane e accoglienza
    qualita = cols3[0].slider("Qualità del personale :", 1, 100, 1)
    pulizia = cols3[1].slider("Pulizia degli ambienti :", 1, 100, 1)
    empatia = cols3[2].slider("Grado di empatia personale :", 1, 100, 1)
    info_terapeutiche = cols3[3].slider("Chiarezze delle informazioni terapeutiche :", 1, 100, 1)
    submitted = st.form_submit_button(label="Submit")
    if submitted==True:
        datetime_object = datetime.datetime.now()
        st.success("Successfully")
        add_row_to_gsheet(
        df, [[author, eta, sesso,
              str(date), infras, proces, sicurezza,
              qualita, pulizia, empatia, info_terapeutiche, str(datetime_object)]])

        #df_new=getdata(df)
        #soddMean=round(mean(df['Soddisfazione']))
        #marcMean=round(mean(df['Marchio']))
        #engaMean=round(mean(df['Engagment']))
        #prov2=len(df_new)
        #CustomSatisf=round((soddMean+marcMean+engaMean)/(3))
        

        st.write("## Results analysis")
        a, b = st.columns(2)

        with a:
            st.write("CUSTOMER SATISFACTION: 80")
        with b:
            st.write("NUMERO REPORT FATTI: ",df_new)
        st.balloons()
