import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

#from Patient_Form import form_pazienti

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

df_operations=connect_to_gsheet()
df_operations=pd.DataFrame(data=df_operations)

def dashboard_operations():
    
    st.title("Dashboard MedTech Operations")
    expander = st.expander("See all records")
    with expander:
        st.write(f"Open original [Google Sheet]({GSHEET_URL})")
        st.dataframe(get_data(df_operations))
    
    st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
    
    g1, g2, g3 = st.columns(3)
    g1.metric(label = "Safety", value = ("96 %"),)
    g2.metric(label = "Drugs treatment cost",
    value = ("500.230 €"),
    delta = ("210€"))
    g3.metric(label = "Accessi giornalieri",
    value = ("150"),
    delta = ("12"))

    col1, col2 = st.columns(2)

    with col1:
        st.header("Patient satisfaction")
        st.image("https://www.datapine.com/images/patient-satisfaction-dashboard.png")

    with col2:
        st.header("Health data")
        st.image("https://www.datapine.com/images/hospital-kpi-dashboard.png")
    
    st.write(df_operations["Incassato trattamento"].mean)
    
