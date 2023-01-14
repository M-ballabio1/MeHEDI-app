import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from htbuilder import div, big, h2, styles
from htbuilder.units import rem

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

def display_dial(title, value, color):
        st.markdown(
            div(
                style=styles(
                    text_align="center",
                    color=color,
                    padding=(rem(0.8), 0, rem(3), 0),
                )
            )(
                h2(style=styles(font_size=rem(0.8), font_weight=600, padding=0))(title),
                big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(
                    value
                ),
            ),
            unsafe_allow_html=True,
        )

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
    
    polarity_color = COLOR_BLUE
    subjectivity_color = COLOR_CYAN

    a, b = st.columns(2)

    with a:
        display_dial("POLARITY", "60", polarity_color)
    with b:
        display_dial("SUBJECTIVITY", "77", subjectivity_color)
