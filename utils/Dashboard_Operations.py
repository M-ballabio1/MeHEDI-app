import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

from Paziente_Form.form import df

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
SHEET_NAME = "Database_Operations"
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


def dashboard_operations():
    
    st.title("Dashboard MedTech Operations")
    df = connect_to_gsheet()
    
    st.dataframe(get_data(gsheet_connector))
    
    st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
    

    cols = st.columns(2)
    sessoFil = cols[0].multiselect(
        "Select the type of Annotation:",
        options=df["Sesso"].unique(),
        default=df["Sesso"].unique()
    )

    cateFil = cols[1].multiselect(
        "Seleziona il livello di marchio:",
        options=df["Categoria Visita"].unique(),
        default=df["Categoria Visita"].unique()
    )

    df_selection = df.query(
        "Sesso == @SessoFil & Categoria Visita == @cateFil"
    )
