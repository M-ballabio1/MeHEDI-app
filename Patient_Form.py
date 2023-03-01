# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
from PIL import Image
import time
import datetime
import database as db
import streamlit_authenticator as stauth

import google_auth_httplib2
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

from utils.Dashboard_Operations import dashboard_operations
from utils.Dashboard import dashboard_patient_satisf
from utils.Dashboard_Economics import dashboard_economics

#css_file="style.css"
image = Image.open('images/logo_form4.png')
image2 = Image.open('images/Mehedi_logo.png')
image3 = Image.open('images/Mehedi_logo2.png')
img = Image.open('images/background.jpg')
img2 = Image.open('images/med_bot.png')

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

data="DatasetOperations_Economics.xlsx"
#df_data=pd.DataFrame(data)

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

# --- USER AUTHENTICATION ---

users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login - Web application MEHEDI Patient's satisfaction", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.write('<base target="_blank">', unsafe_allow_html=True)
    prev_time = [time.time()]
    a, b = st.columns([1, 1])
    with a:
        st.image(image2, width=300)      
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
        st.markdown(hide_img_fs, unsafe_allow_html=True)
    with b:
        st.info(
        """
        Questa è una webapp creata da che consente di valutare la Patient Satisfaction in un'azienda sanitaria di medie dimensioni.
        
        ACCESSO PAZIENTE - username: guest | password: paz123
        
        ACCESSO MANAGEMENT - username: mballabio | password: mat123
        """
    ) 

if authentication_status:
    #placeholder.empty()

    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    
    def form_pazienti():
        
        st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 4rem;
                    padding-left: 4rem;
                    padding-right: 4rem;
                }
        </style>
        """, unsafe_allow_html=True)
        
        t1, t2 = st.columns((1, 0.10)) 

        t1.image(image, width=1000)
        hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
        st.markdown(hide_img_fs, unsafe_allow_html=True)
        #t1.markdown("### This section shows some information about MeHEDI - Tool of Patient Satisfaction")
        t2.write("")

        #append pages
        #st.sidebar.success("Select a page above.")

        # connect and append data
        df = connect_to_gsheet()
        
        st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
        st.sidebar.info(
        """
        Questa è una webapp creata da che consente di valutare la Patient Satisfaction
        
        Web App URL: <https://xxx.streamlitapp.com>
        """
        )
    
        st.sidebar.title("Support")
        st.sidebar.info(
            """
            Per eventuali problemi nell'utilizzo app rivolgersi a: matteoballabio99@gmail.com
            """
        )
        a, b, c = st.sidebar.columns([0.2,1,0.2])
        with a:
            st.write("")
        with b:
            st.image(image3, width=170)
        with c:
            st.write("")
        
        # creazione webform
        i,a,b,c = st.columns([0.2,7,0.1,2])
        with i:
            st.write("")
        with a:
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
                    """)
                st.markdown("")
            st.write("")
            new_title = '<b style="font-family:serif; color:#6082B6; font-size: 28px;">📌 Quanto tempo hai a disposizione per compilare il form?</b>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write("")
            slider = st.slider(label='Trascina lo slider', min_value=1,max_value=10, value=1, key='Form5')
        with b:
            st.write("")
        with c:
            st.image(img2, width=200)
        if slider<2:
            form = st.form(key="annotation1", clear_on_submit = True,)
            with form:
                #new_title = '<b style="font-family:serif; color:#6082B6; font-size: 35px;">MEDi Form:</b>'
                #st.markdown(new_title, unsafe_allow_html=True)
                new_title = '<b style="font-family:serif; color:#6082B6; font-size: 18px;">Informazioni Generali Pazienti</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                cols = st.columns((1, 1, 1, 1))
                #info paziente
                author = cols[0].text_input("Nome del paziente:")
                eta = cols[1].text_input("Età anagrafica:")
                sesso = cols[2].selectbox(
                    "Sesso:", ["Maschio", "Femmina", "Non specificato"], index=2)
                date = cols[3].date_input("Quando è stato in ospedale:")
    
                #infrastruttura fisica tecnologica
                new_title = '<b style="font-family:serif; color:#6082B6; font-size: 18px;">Informazioni Infrastruttura e Processi</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                cols2 = st.columns((3))
                infras = cols2[0].slider("Qualità della struttura ospedaliera :", 1, 100, 1)
                proces = cols2[1].slider("Qualità dei processi clinici amministrativi :", 1, 100, 1)
                sicurezza = cols2[2].slider("Sicurezza ospedale :", 1, 100, 1)
                
                #risorse umane e accoglienza
                new_title = '<b style="font-family:serif; color:#6082B6; font-size: 18px;">Informazioni Risorse umane e Qualità percepita</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                cols3 = st.columns((1, 1, 1, 1))
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
                    st.balloons()
        if slider>1 and slider<6:
            form = st.form(key="annotation2", clear_on_submit = True,)
            with form:
                
                st.write("Informazioni Generali Pazienti")
                cols = st.columns((1, 1, 1, 1))
                #info paziente              
                author = cols[0].text_input("Nome del paziente:")
                eta = cols[1].text_input("Età anagrafica:")
                sesso = cols[2].selectbox(
                    "Sesso:", ["Maschio", "Femmina", "Non specificato"], index=2)
                date = cols[3].date_input("Quando è stato in ospedale:")
    
                #infrastruttura fisica tecnologica
                st.write("Informazioni Infrastruttura e Processi")
                cols2 = st.columns((3))
                infras = cols2[0].slider("Qualità della struttura ospedaliera :", 1, 100, 1)
                proces = cols2[1].slider("Qualità dei processi clinici amministrativi :", 1, 100, 1)
                sicurezza = cols2[2].slider("Sicurezza ospedale :", 1, 100, 1)
                
                #risorse umane e accoglienza
                st.write("Informazioni Risorse umane e Qualità percepita")
                cols3 = st.columns((1, 1, 1, 1))
                qualita = cols3[0].slider("Qualità del personale :", 1, 100, 1)
                pulizia = cols3[1].slider("Pulizia degli ambienti :", 1, 100, 1)
                empatia = cols3[2].slider("Grado di empatia personale :", 1, 100, 1)
                info_terapeutiche = cols3[3].slider("Chiarezze delle informazioni terapeutiche :", 1, 100, 1)
                
                #prestazione ambulatoriale ricevuta
                st.write("Informazioni attese Prestazione Ricevuta")
                cols3 = st.columns((3))
                type_vis = cols3[0].selectbox("A quale macro area afferisce la prestazione che ha ricevuto:", ("RISONANZA","ELETTROMIOGRAFIA","TOMOGRAFIA","ECOGRAFIA","RADIOGRAFIA","ECODOPPLER"))
                durata_vis = cols3[1].selectbox("Quanto è durata la visita:",options=[0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
                durata_attesa_vis = cols3[2].selectbox("Quanto è durata il tempo di attesa prima della visita:",options=[0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
                
                submitted = st.form_submit_button(label="Submit")
                if submitted==True:
                    datetime_object = datetime.datetime.now()
                    st.success("Successfully")
                    add_row_to_gsheet(
                    df, [[author, eta, sesso,
                          str(date), infras, proces, sicurezza,
                          qualita, pulizia, empatia, info_terapeutiche, str(datetime_object),
                          type_vis, durata_vis, durata_attesa_vis]])
                    st.balloons()
        
        if slider>5 and slider<10:
            form = st.form(key="annotation3", clear_on_submit = True,)
            with form:
                
                st.write("Informazioni Generali Pazienti")
                cols = st.columns((1, 1, 1, 1))
                #info paziente              
                author = cols[0].text_input("Nome del paziente:")
                eta = cols[1].text_input("Età anagrafica:")
                sesso = cols[2].selectbox(
                    "Sesso:", ["Maschio", "Femmina", "Non specificato"], index=2)
                date = cols[3].date_input("Quando è stato in ospedale:")
    
                #infrastruttura fisica tecnologica
                st.write("Informazioni Infrastruttura e Processi")
                cols2 = st.columns((3))
                infras = cols2[0].slider("Qualità della struttura ospedaliera :", 1, 100, 1)
                proces = cols2[1].slider("Qualità dei processi clinici amministrativi :", 1, 100, 1)
                sicurezza = cols2[2].slider("Sicurezza ospedale :", 1, 100, 1)
                
                #risorse umane e accoglienza
                st.write("Informazioni Risorse umane e Qualità percepita")
                cols3 = st.columns((1, 1, 1, 1))
                qualita = cols3[0].slider("Qualità del personale :", 1, 100, 1)
                pulizia = cols3[1].slider("Pulizia degli ambienti :", 1, 100, 1)
                empatia = cols3[2].slider("Grado di empatia personale :", 1, 100, 1)
                info_terapeutiche = cols3[3].slider("Chiarezze delle informazioni terapeutiche :", 1, 100, 1)
                
                #prestazione ambulatoriale ricevuta
                st.write("Informazioni attese Prestazione Ricevuta")
                cols3 = st.columns((3))
                type_vis = cols3[0].selectbox("A quale macro area afferisce la prestazione che ha ricevuto:", ("RISONANZA","ELETTROMIOGRAFIA","TOMOGRAFIA","ECOGRAFIA","RADIOGRAFIA","ECODOPPLER"))
                durata_vis = cols3[1].selectbox("Quanto è durata la visita:",options=[0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
                durata_attesa_vis = cols3[2].selectbox("Quanto è durata il tempo di attesa prima della visita:",options=[0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
                
                #tempi di attesa trattamenti
                st.write("Prezzo e Utilità Prestazione Ricevuta")
                cols3 = st.columns((2))
                utili_vis = cols3[0].selectbox("Ritieni che la visita effettuata ti sia servita:",options=["Molto Utile","Utile","Equo","Poco utile","Inutile"])
                pay_vis = cols3[1].selectbox("Ritieni di aver pagato per la visita un prezzo:",options=["Troppo alto","Equo","Troppo basso"])
                
                submitted = st.form_submit_button(label="Submit")
                if submitted==True:
                    datetime_object = datetime.datetime.now()
                    st.success("Successfully")
                    add_row_to_gsheet(
                    df, [[author, eta, sesso,
                          str(date), infras, proces, sicurezza,
                          qualita, pulizia, empatia, info_terapeutiche, str(datetime_object),
                          type_vis, durata_vis, durata_attesa_vis, utili_vis, pay_vis]])
                    st.balloons()
        if slider==10:
            form = st.form(key="annotation4", clear_on_submit = True,)
            with form:
                
                st.write("Informazioni Generali Pazienti")
                cols = st.columns((1, 1, 1, 1))
                #info paziente              
                author = cols[0].text_input("Nome del paziente:")
                eta = cols[1].text_input("Età anagrafica:")
                sesso = cols[2].selectbox(
                    "Sesso:", ["Maschio", "Femmina", "Non specificato"], index=2)
                date = cols[3].date_input("Quando è stato in ospedale:")
    
                #infrastruttura fisica tecnologica
                st.write("Informazioni Infrastruttura e Processi")
                cols2 = st.columns((3))
                infras = cols2[0].slider("Qualità della struttura ospedaliera :", 1, 100, 1)
                proces = cols2[1].slider("Qualità dei processi clinici amministrativi :", 1, 100, 1)
                sicurezza = cols2[2].slider("Sicurezza ospedale :", 1, 100, 1)
                
                #risorse umane e accoglienza
                st.write("Informazioni Risorse umane e Qualità percepita")
                cols3 = st.columns((1, 1, 1, 1))
                qualita = cols3[0].slider("Qualità del personale :", 1, 100, 1)
                pulizia = cols3[1].slider("Pulizia degli ambienti :", 1, 100, 1)
                empatia = cols3[2].slider("Grado di empatia personale :", 1, 100, 1)
                info_terapeutiche = cols3[3].slider("Chiarezze delle informazioni terapeutiche :", 1, 100, 1)
                
                #prestazione ambulatoriale ricevuta
                st.write("Informazioni attese Prestazione Ricevuta")
                cols3 = st.columns((3))
                type_vis = cols3[0].selectbox("A quale macro area afferisce la prestazione che ha ricevuto:", ("RISONANZA","ELETTROMIOGRAFIA","TOMOGRAFIA","ECOGRAFIA","RADIOGRAFIA","ECODOPPLER"))
                durata_vis = cols3[1].selectbox("Quanto è durata la visita:",options=[0,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
                durata_attesa_vis = cols3[2].selectbox("Quanto è durata il tempo di attesa prima della visita:",options=[0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,40,50,60])
                
                #tempi di attesa trattamenti
                st.write("Prezzo e Utilità Prestazione Ricevuta")
                cols3 = st.columns((2))
                utili_vis = cols3[0].selectbox("Ritieni che la visita effettuata ti sia servita:",options=["Molto Utile","Utile","Equo","Poco utile","Inutile"])
                pay_vis = cols3[1].selectbox("Ritieni di aver pagato per la visita un prezzo:",options=["Troppo alto","Equo","Troppo basso"])
                
                #feedback
                st.write("Feedback miglioramenti")
                cols3 = st.columns((4))
                valut_vis = cols3[0].selectbox("Come valuti nel complesso la tua visita nel nostro centro?",options=[0,1,2,3,4,5,6,7,8,9,10])
                valut_pos_area_vis = cols3[1].selectbox("Qual è il punto di forza del nostro centro?",options=['Empatia personale', 'Prezzi', 'Sicurezza trasmessa', 'Pulizia ambienti', 'Competenza personale', 'Reperimento informazioni da moltemplici fonti (telefono, sito)', 'Tempi di attesa'])
                valut_neg_area_vis = cols3[2].selectbox("Qual è il punto di debolezza del nostro centro?",options=['Empatia personale', 'Orari struttura', 'Prezzi', 'Sicurezza trasmessa', 'Pulizia ambienti', 'Competenza personale', 'Reperimento informazioni da moltemplici fonti (telefono, sito)', 'Tempi di attesa'])
                feed_vis = cols3[3].text_area("Scrivici che cosa miglioreresti del nostro centro. La tua opinione per noi conta!")
                
                submitted = st.form_submit_button(label="Submit")
                if submitted==True:
                    datetime_object = datetime.datetime.now()
                    st.success("Successfully")
                    add_row_to_gsheet(
                    df, [[author, eta, sesso,
                          str(date), infras, proces, sicurezza,
                          qualita, pulizia, empatia, info_terapeutiche, str(datetime_object),
                          type_vis, durata_vis, durata_attesa_vis, utili_vis, pay_vis,
                          valut_vis, valut_pos_area_vis, valut_neg_area_vis, feed_vis]])
                    st.balloons()
                
    if name=="Matteo Ballabio" or name=="Federico Facoetti" or name=="Luca Cappellini":
        page_names_to_funcs = {
            "Form Patient Satisfaction": form_pazienti,
            "Dashboard Operations": dashboard_operations,
            "Dashboard Patient Satisfaction": dashboard_patient_satisf,
            "Dashboard Economics": dashboard_economics}
    elif name=="Gentile paziente":
        page_names_to_funcs = {
            "Form Patient Satisfaction": form_pazienti}

    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys(), key ="value")
    page_names_to_funcs[selected_page]()
