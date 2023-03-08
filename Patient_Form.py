# -*- coding: utf-8 -*-

#import libraries
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
from utils.addition.graphs import graph_pes

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

# impostazione grafica iniziale
st.set_page_config(page_title="MeHEDI", page_icon="🏥", layout="wide")

@st.cache_resource()
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
    a, b, = st.columns([1, 1])
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
        
        #serve per allargare margini da block-container
        st.markdown("""
        <style>
               .css-k1ih3n {
                    padding-top: 0rem;
                    padding-bottom: 4rem;
                    padding-left: 4em;
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
        i,a,b,c,d = st.columns([0.2,7,0.1,2,1.5])
        with i:
            st.write("")
        with a:
            with st.expander("ℹ️ Istruzioni generali compilazione form", expanded=False):
                st.markdown(
                    """
                    ### Framework Return on Experience of MeHEDI
                    Questo framework serve alla struttura sanitaria per raccogliere il feedback riguardo i servizi erogati ai suoi pazienti. Per qualsiasi problematica alla fine della compilazione del form sarà possibile contattare la struttura tramite e-mail.
                    """
                )
                st.markdown(
                    """
                    ### Istruzioni alla compilazione del Form
                    Gentile paziente,
                    
                    Il suo medico l'ha indirizzata al reparto di Radiologia per alcuni esami. Ora, al termine degli esami e mentre lascia il nostro reparto, vorremmo farle alcune domande sul nostro reparto e sulla sua esperienza. Le sue risposte ci permetteranno di migliorare la qualità del servizio offerto a lei come paziente. Teniamo molto alla sua opinione.
                    
                    Ci vorranno solo pochi minuti del vostro tempo. Leggete attentamente ogni domanda, scegliete la vostra risposta e contrassegnatela. Se ritenete di non essere in grado di rispondere a una domanda specifica, passate alla successiva.
                    
                    Per alcune domande vorremmo che ci desse un punteggio, che va da 1 a 5: 5 significa che è molto soddisfatto e 1 che è molto insoddisfatto. Potete darci qualsiasi punteggio che ritenete corretto. Un punteggio come 3,5 va bene e può essere dato *[5=molto soddisfatto, 4=soddisfatto, 3=neutro, né soddisfatto né insoddisfatto, 2=insoddisfatto, 1=molto insoddisfatto]*.
                    
                    ### Perchè vogliamo misurare la Patient Satisfaction?
                    1. Miglioramento dei servizi offerti dalla struttura mirata nelle aree segnalate 
                    2. Far risparmiare il tempo dei nostripazienti tramite una migliore Patient Experience della nostra struttura
                    3. Monitoraggio dei punti di forza e punti di miglioramento della nostra struttura
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
            st.info("Ciao, sono Cleo il tuo assistente personale!")
            st.info('Posso aiutarti a compilare il nostro form di Patient Satisfaction. Se hai dubbi non esitare a consultare la sezione "Istruzioni generali compilazione form"')
        with d:
            st.image(img2)
        if slider<4:
            col1,  col2 = st.columns([1, 0.50])
            with col1:
                new_title = '<b style="font-family:serif; color:#FF0000; font-size: 40px;">📋 MEDi Experience Form:</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.info("➡️ 1. Come ha preso l'appuntamento?")
                cols = st.columns((1, 1))
                #APPUNTAMENTO
                var_a1 = cols[0].selectbox("Ho preso un appuntamento:",  ["Personalmente",  "Telefono",  "Sito Web", "E-mail",  "Tramite medico",  "Altro"])
                var_a2= cols[1].slider("Quanto è soddisfatto della facilità di fissare un appuntamento?", 1, 5, 1)

                #ACCOGLIENZA
                st.info("➡️ 2. Sull'accoglienza del nostro dipartimento")
                cols2 = st.columns((2))
                var_c1 = cols2[0].slider("Quanto è soddisfatto dell'accoglienza del nostro reparto?", 1, 5, 1)
                var_c2 = cols2[1].slider("Quanto è soddisfatto del tempo che ha dovuto attendere per essere aiutato alla reception?", 1, 5, 1)
                
            #PROCEDURA
            st.info("➡️ Sulla procedura che le è stata prescritta")
            cols3 = st.columns((1, 1, 1))
            var_d1 = cols3[0].selectbox("A quale procedura di imaging medico si è sottoposto?", ["RMN", "CT", "Ultrasuoni", "Raggi X", "Mammografia", "Artrografia/Mielografia", "Interventi/Biopsie", "Altro"])
            var_d2 = cols3[1].slider("Quanto è soddisfatto del tempo di attesa nel reparto prima dell'inizio della procedura?", 1, 5, 1)
            var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita?", options=[1, 2, 3, 4,5,10,15,20,25,30,35,40,45,50,55,60,70,80,90])
            
            #SPIEGAZIONE RISULTATI
            st.info("➡️ Spiegazioni risultati del dipartimento")
            cols3 = st.columns((1, 1, 1))
            var_f1 = cols3[0].selectbox("Si è rivolto a un operatore sanitario dopo la visita in reparto?", ["NO", "Si, radiologo (medico)", "Si, radiografo", "Altro specialista"])
            var_f2 = cols3[1].selectbox("Ha consultato un professionista della salute per farsi spiegare i risultati?", ["NO", "Si, radiologo (medico)", "Si, radiografo", "Altro specialista"])
            var_f3 = cols3[2].slider("Quanto è soddisfatto della spiegazione fornita dal radiologo?", 1,  5,  1)
            
            #ESPERIENZA COME PAZIENTE
            st.info("➡️ Com'è stata la sua esperienza nel reparto come paziente")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_h1 = cols3[0].slider("Quanto è soddisfatto della disponibilità di servizi igienici? ", 1,  5,  1)
            var_h2 = cols3[1].slider("Quanto è soddisfatto della pulizia del reparto? ", 1,  5,  1)
            var_h5 = cols3[2].slider("Quanto è soddisfatto della cordialità del personale ", 1,  5,  1)
            var_h7 = cols3[3].slider("Ha ritenuto che la sua privacy sia stata rispettata? ", 1,  5,  1)
            var_h9 = cols3[4].slider("Consiglierebbe il nostro reparto di radiologia", 1,  5,  1)
            submitted = st.button(label="Submit")
            with col2:
                med_accoglienza=(var_c1+var_c2)/2
                med_experience=(var_h1+var_h2+var_h5+var_h7+var_h9)/5
                DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                            {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                            {"taste": "PROCEDURE", "Peso Area": var_d2},
                            {"taste": "RISULTATI", "Peso Area": var_f3},
                            {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                graph_pes(DATA)
                
            if submitted==True:
                datetime_object = datetime.datetime.now()
                st.success("Successfully")
                add_row_to_gsheet(
                df, [[var_a1, var_a2, "",
                        "", "", "",
                        var_c1, var_c2, "",
                        var_d1, var_d2, var_d3, "","", "", "",
                        "", "", 
                        var_f1, var_f2, var_f3,
                        "","", "", "","",
                        var_h1, var_h2, "","", var_h5, "", var_h7,"", var_h9, 
                        "", "", 
                        "", 
                        str(datetime_object)]])
                st.balloons()
        if slider>3 and slider<8:
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
        
        if slider>7:
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
