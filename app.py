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
from feel_it import EmotionClassifier, SentimentClassifier

from utils.Dashboard_Operations import dashboard_operations
from utils.Dashboard import dashboard_patient_satisf
from utils.Dashboard_Economics import dashboard_economics
from utils.Info_Page import landing_page
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

@st.cache_data()
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

#users = db.fetch_all_users()

#usernames = [user["key"] for user in users]
#names = [user["name"] for user in users]
#hashed_passwords = [user["password"] for user in users]

#authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'some_cookie_name','some_signature_key',cookie_expiry_days=30)
#name, authentication_status, username = authenticator.login("Login - Web application MEHEDI Patient's satisfaction", "main")

#if st.session_state["authentication_status"] == False:
#    st.error("Username/password is incorrect")

#if st.session_state["authentication_status"] == None:
#    st.write('<base target="_blank">', unsafe_allow_html=True)
#    prev_time = [time.time()]
#    a, b, = st.columns([1, 1])
#    with a:
#        st.image(image2, width=300)      
#        hide_img_fs = '''
#        <style>
#        button[title="View fullscreen"]{
#            visibility: hidden;}
#        </style>
#        '''
#        st.markdown(hide_img_fs, unsafe_allow_html=True)
#    with b:
#        st.info(#Questa è una webapp creata da che consente di valutare la Patient Satisfaction in un'azienda sanitaria di medie dimensioni.ACCESSO PAZIENTE - username: guest | password: paz123 ACCESSO MANAGEMENT - username: mballabio | password: mat123) 

#if st.session_state["authentication_status"]:

senza_auth=True
if senza_auth==True:
    #placeholder.empty()

    # ---- SIDEBAR ----
    #authenticator.logout("Logout", "sidebar")
    st.sidebar.title("Welcome 👋")
    
    def form_pazienti():
        
        # Add the markdown code to hide the header element
        st.markdown(
            """
            <style>
            header[data-testid="stHeader"] {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
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

        reduce_header_height_style = """
            <style>
                div.block-container {padding-top:1rem;}
            </style>
        """
        st.markdown(reduce_header_height_style, unsafe_allow_html=True)

        # connect and append data
        df = connect_to_gsheet()
        
        #SIDEBAR
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
            st.markdown("""
            <div align=center><small>
            Page views interaction: <img src="https://www.cutercounter.com/hits.php?id=hxndpfn&nd=6&style=52" border="0" alt="hit counter"><br>
            GitHub <a href="https://github.com/M-ballabio1/MeHEDI-app"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/M-ballabio1/MeHEDI-app?style=social"></a>
            </small></div>
            """, unsafe_allow_html=True)
        with c:
            st.write("")
        
        # INTRODUCTION FORM
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
                    
                    Per alcune domande vorremmo che ci desse un punteggio, che va da 1 a 7: 7 significa che è molto soddisfatto e 1 che è molto insoddisfatto. Potete darci qualsiasi punteggio che ritenete corretto.  *[7=ottimo, 6=molto soddisfatto, 5=soddisfatto, 4=neutro 3=né soddisfatto né insoddisfatto, 2=insoddisfatto, 1=molto insoddisfatto]*.
                    
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
            
        # ###FORM 1
        if slider<4:
            col1,  col2 = st.columns([1, 0.60])
            with col1:
                new_title = '<b style="font-family:serif; color:#FF0000; font-size: 40px;">📋 MEDi Experience Form:</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.info("➡️ 1. Come ha preso l'appuntamento?")
                cols = st.columns((1, 1))
                #APPUNTAMENTO
                var_a1 = cols[0].selectbox("Ho preso un appuntamento:",  ["Personalmente",  "Telefono",  "Sito Web", "E-mail",  "Tramite medico",  "Altro"])
                var_a2= cols[1].slider("Quanto è soddisfatto della facilità di fissare un appuntamento?", 1, 7, 1)

                #ACCOGLIENZA
                st.info("➡️ 2. Sull'accoglienza del nostro dipartimento")
                cols2 = st.columns((2))
                var_c1 = cols2[0].slider("Quanto è soddisfatto dell'accoglienza del nostro reparto?", 1, 7, 1)
                var_c2 = cols2[1].slider("Quanto è soddisfatto del tempo che ha dovuto attendere per essere aiutato alla reception?", 1, 7, 1)
                
            #PROCEDURA
            st.info("➡️ 3. Sulla procedura che le è stata prescritta")
            cols3 = st.columns((1, 1, 1))
            var_d1 = cols3[0].selectbox("A quale procedura di imaging medico si è sottoposto?", ["RMN", "CT", "Ultrasuoni", "Raggi X", "Mammografia", "Artrografia/Mielografia", "Interventi/Biopsie", "Altro"])
            var_d2 = cols3[1].slider("Quanto è soddisfatto del tempo di attesa nel reparto prima dell'inizio della procedura?", 1, 7, 1)
            options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90]
            if var_d1=="RMN":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(30))
            elif var_d1=="CT" or var_d1=="Mammografia":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(5))
            elif var_d1=="Ultrasuoni" or var_d1=="Artrografia/Mielografia" or var_d1=="Interventi/Biopsie":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(20))
            elif var_d1=="Raggi X":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90], index=options.index(2))
            else:
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(1))
            
            #SPIEGAZIONE RISULTATI
            st.info("➡️ 4. Spiegazioni risultati del dipartimento")
            cols3 = st.columns((1, 1, 1))
            var_f1 = cols3[0].selectbox("Si è rivolto a un operatore sanitario dopo la visita in reparto?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f2 = cols3[1].selectbox("Ha consultato un professionista della salute per farsi spiegare i risultati?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f3 = cols3[2].slider("Quanto è soddisfatto della spiegazione fornita dal radiologo?", 1,  7,  1)
            
            #ESPERIENZA COME PAZIENTE
            st.info("➡️ 5. Com'è stata la sua esperienza nel reparto come paziente")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_h1 = cols3[0].slider("Quanto è soddisfatto della disponibilità di servizi igienici? ", 1,  7,  1)
            var_h2 = cols3[1].slider("Quanto è soddisfatto della pulizia del reparto? ", 1,  7,  1)
            var_h5 = cols3[2].slider("Quanto è soddisfatto della cordialità del personale ", 1,  7,  1)
            var_h7 = cols3[3].slider("Ha ritenuto che la sua privacy sia stata rispettata? ", 1,  7,  1)
            var_h9 = cols3[4].selectbox("Consiglierebbe il nostro reparto di radiologia ai suoi familiari e amici", ["SI", "NO"])
            
            #INFO PAZIENTE
            st.info("➡️ 6. La nostra analisi delle vostre risposte")
            cols3 = st.columns((1, 1))
            var_i1= cols3[0].select_slider('Potrebbe indicarci il suo gruppo di età (facoltativo)?',options=["< 18 anni",	"18-30anni", 	"30-65anni",  ">65 anni" ])
            var_i2= cols3[1].selectbox('Può indicarci il suo sesso (facoltativo)?',options=["Maschio", "Femmina", "Non Specificato" ])
            
            with col2:
                med_accoglienza=(var_c1+var_c2)/2
                med_experience=(var_h1+var_h2+var_h5+var_h7)/4
                DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                            {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                            {"taste": "PROCEDURE", "Peso Area": var_d2},
                            {"taste": "RISULTATI", "Peso Area": var_f3},
                            {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                graph_pes(DATA)
                media_tot=round(((med_accoglienza+med_experience+var_a2+var_d2+var_f3)/5), 1)
            
            # COMMENT 1
            cols_text = st.columns((0.25, 1))
            if media_tot ==1:
                pass
            elif media_tot<=4:
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza può essere migliorata, raccontaci cosa ne pensi e miglioreremo sicuramente")
                        
            elif media_tot>4 and media_tot<=5:
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza non è andata al massimo, se ti interessa raccontaci la tua esperienza e miglioreremo sicuramente i punti deboli della nostra struttura")
                        
            elif media_tot>5 and media_tot<=7:
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza sembra essere andata bene, se ti interessa raccontaci la tua esperienza continueremo a migliorare")
            else:
                feedback_gen=""
            
            # ADDITIONAL COMMENT
            if media_tot ==1:
                pass
            elif media_tot < 4.5:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("La tua ESPERIENZA COMPLESSIVA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(media_tot)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif var_a2 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("L'area APPUNTAMENTO è molto carente con un risultato di "+str(var_a2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif med_accoglienza < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("L'area ACCOGLIENZA PAZIENTE è molto carente con un risultato di "+str(med_accoglienza)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura. Essendo una delle aree più importanti per noi ci piacerebbe avere il tuo parere.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif var_d2 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("L'area PROCEDURE è molto carente con un risultato di "+str(var_d2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif var_f3 < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("L'area RISULTATI è molto carente con un risultato di "+str(var_f3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif med_experience < 4:
                colss = st.columns([0.23, 0.02, 1])
                colss[0].error("L'area dell'ESPERIENZA VISSUTA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(med_experience)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                colss[1].write("")
                add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            else:
                add_comm=""
                     
            @st.cache_resource()
            def classif_nlp(str):
                # str to classify
                emotion_classifier = EmotionClassifier()
                resp1=emotion_classifier.predict([str])
                sentiment_classifier = SentimentClassifier()
                resp2=sentiment_classifier.predict([str])
                return resp1, resp2
            
            cols_text=st.columns([0.5,1])
            cols_text[0].subheader("Test the sentiment of your comment")
            cols_text[0].write("")
            but= cols_text[0].button("Test Sentiment 🔝 😐 👎")
            if but:
                if feedback_gen=="":
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("Inserisci un commento")
                    emozione=""
                    sentiment=""
                else:
                    resp1, resp2 = classif_nlp(feedback_gen)
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    # force the classification to limit outlier
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    else:
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    
            submitted = st.button(label="Submit")  
            if submitted==True:
                if feedback_gen=="":
                    emozione=""
                    sentiment=""
                else:  
                    resp1, resp2 = classif_nlp(feedback_gen)
                    emozione=resp1[0]
                    sentiment=resp2[0]
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                    else:
                        pass
                st.success("Successfully")
                st.balloons()
                #Storing data
                datetime_object = datetime.datetime.now()
                add_row_to_gsheet(
                df, [[var_a1, var_a2, "",
                        "", "", "",
                        var_c1, var_c2, "",
                        var_d1, var_d2, var_d3, "","", "", "",
                        "", "", 
                        var_f1, var_f2, var_f3,
                        "","", "", "","",
                        var_h1, var_h2, "","", var_h5, "", var_h7,"", var_h9, 
                        var_i1, var_i2, 
                        feedback_gen, 
                        str(datetime_object),  "Form_breve", add_comm,  emozione,  sentiment]])
        
        # ###FORM 2
        if slider>3 and slider<8:
            col1,  col2 = st.columns([1, 0.60])
            with col1:
                new_title = '<b style="font-family:serif; color:#FF0000; font-size: 40px;">📋 MEDi Experience Form:</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.info("➡️ 1. Come ha preso l'appuntamento?")
                cols = st.columns((1, 1, 1.7))
                #APPUNTAMENTO
                var_a1 = cols[0].selectbox("Ho preso un appuntamento:",  ["Personalmente",  "Telefono",  "Sito Web", "E-mail",  "Tramite medico",  "Altro"])
                var_a2= cols[1].slider("Quanto è soddisfatto della facilità di fissare un appuntamento?", 1, 7, 1)
                var_a3= cols[2].select_slider('Quanto tempo è trascorso tra la segnalazione del medico e l\'appuntamento?',options=["< 1 settimana", "< 1 mese", "1-3 mesi", "3-6 mesi", "> 6 mesi"])
                
                #SITO WEB
                st.info("➡️ 2. Informazioni sul sito nostro sito web")
                cols2 = st.columns((3))
                var_b1 = cols2[0].selectbox("Avete visitato il nostro sito web", ["SI", "NO"])
                if var_b1=="SI":
                    var_b2 = cols2[1].slider("Se sì, quanto è soddisfatto delle informazioni che trova sul nostro sito web?", 1, 7, 1)
                    var_b3 = cols2[2].slider("Se sì, quanto è soddisfatto della facilità di utilizzo del nostro sito web?", 1, 7, 1)
                else:
                    var_add= cols2[1].selectbox("Non hai visitato il nostro sito web per quale motivo?", ["Ho avuto difficoltà a trovarlo", "Non mi interessa visitarlo", "Altro"])
                    if var_add=="Altro":
                        var_add2=cols2[2].text_input("Se vuoi inserisci la motivazione")

            #ACCOGLIENZA
            st.info("➡️ 3. Sull'accoglienza del nostro dipartimento")
            cols2 = st.columns((3))
            var_c1 = cols2[0].slider("Quanto è soddisfatto dell'accoglienza del nostro reparto?", 1, 7, 1)
            var_c2 = cols2[1].slider("Quanto è soddisfatto del tempo che ha dovuto attendere per essere aiutato alla reception?", 1, 7, 1)
            var_c3 = cols2[2].slider("Quanto è soddisfatto delle istruzioni ricevute per trovare l'area d'attesa corretta per la procedura?", 1, 7, 1)
                
            #PROCEDURA
            st.info("➡️ 4. Sulla procedura che le è stata prescritta")
            cols3 = st.columns((1.3,  1.7,  1,  1,  1,  1,  1.6))
            var_d1 = cols3[0].selectbox("A quale procedura di imaging medico si è sottoposto?", ["RMN", "CT", "Ultrasuoni", "Raggi X", "Mammografia", "Artrografia/Mielografia", "Interventi/Biopsie", "Altro"])
            var_d2 = cols3[1].slider("Quanto è soddisfatto del tempo di attesa nel reparto prima dell'inizio della procedura?", 1, 7, 1)
            options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90]
            if var_d1=="RMN":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(30))
            elif var_d1=="CT" or var_d1=="Mammografia":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(5))
            elif var_d1=="Ultrasuoni" or var_d1=="Artrografia/Mielografia" or var_d1=="Interventi/Biopsie":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(20))
            elif var_d1=="Raggi X":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90], index=options.index(2))
            else:
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(1))
            var_d4 = cols3[3].selectbox("Si è sentito sicuro durante la procedura?", ["SI", "NO", "Indifferente"])
            var_d5 = cols3[4].selectbox("Ha provato dolore a causa della procedura?", ["SI", "NO", "Indifferente"])
            var_d6 = cols3[5].selectbox("Ha provato ansia durante la procedura?", ["SI", "NO", "Indifferente"])
            var_d7 = cols3[6].slider("Quanto è soddisfatto della durata della procedura stessa?", 1, 7, 1)
            
            #SPIEGAZIONE RISULTATI
            st.info("➡️ 5. Spiegazioni risultati del dipartimento")
            cols3 = st.columns((1, 1, 1))
            var_f1 = cols3[0].selectbox("Si è rivolto a un operatore sanitario dopo la visita in reparto?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f2 = cols3[1].selectbox("Ha consultato un professionista della salute per farsi spiegare i risultati?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f3 = cols3[2].slider("Quanto è soddisfatto della spiegazione fornita dal radiologo?", 1,  7,  1)
            
            #ESPERIENZA COME PAZIENTE
            st.info("➡️ 6. Com'è stata la sua esperienza nel reparto come paziente")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_h1 = cols3[0].slider("Quanto è soddisfatto della disponibilità di servizi igienici? ", 1,  7,  1)
            var_h2 = cols3[1].slider("Quanto è soddisfatto della pulizia del reparto? ", 1,  7,  1)
            var_h5 = cols3[2].slider("Quanto è soddisfatto della cordialità del personale ", 1,  7,  1)
            var_h7 = cols3[3].slider("Ha ritenuto che la sua privacy sia stata rispettata? ", 1,  7,  1)
            var_h9 = cols3[4].selectbox("Consiglierebbe il nostro reparto di radiologia ai suoi familiari e amici", ["SI", "NO"])
            
            #INFO PAZIENTE
            st.info("➡️ 7. La nostra analisi delle vostre risposte")
            cols3 = st.columns((1, 1))
            var_i1= cols3[0].select_slider('Potrebbe indicarci il suo gruppo di età (facoltativo)?',options=["< 18 anni",	"18-30anni", 	"30-65anni",  ">65 anni" ])
            var_i2= cols3[1].selectbox('Può indicarci il suo sesso (facoltativo)?',options=["Maschio", "Femmina", "Non Specificato" ])

            with col2:
                if var_b1=="NO":
                    med_accoglienza=(var_c1+var_c2+var_c3)/2
                    med_experience=(var_h1+var_h2+var_h5+var_h7)/4
                    med_proc=(var_d2+var_d7)/2
                    DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                                {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                                {"taste": "PROCEDURE", "Peso Area": med_proc},
                                {"taste": "RISULTATI", "Peso Area": var_f3},
                                {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                    graph_pes(DATA)
                    media_tot=(med_accoglienza+med_experience+var_a2+var_d2+var_f3)/5
                elif var_b1=="SI":
                    med_accoglienza=(var_c1+var_c2)/2
                    med_sito=(var_b2+var_b3)/2
                    med_experience=(var_h1+var_h2+var_h5+var_h7)/4
                    med_proc=(var_d2+var_d7)/2
                    DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                                {"taste": "SITO WEB", "Peso Area": med_sito},
                                {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                                {"taste": "PROCEDURE", "Peso Area": med_proc},
                                {"taste": "RISULTATI", "Peso Area": var_f3},
                                {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                    graph_pes(DATA)
                    media_tot=round(((med_accoglienza+med_sito+med_experience+var_a2+var_d2+var_f3)/6), 1)
            
            # COMMENT 1
            if media_tot ==1:
                pass
            elif media_tot<=4:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza può essere migliorata, raccontaci cosa ne pensi e miglioreremo sicuramente")
                        
            elif media_tot>4 and media_tot<=5:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza non è andata al massimo, se ti interessa raccontaci la tua esperienza e miglioreremo sicuramente i punti deboli della nostra struttura")
                        
            elif media_tot>5 and media_tot<=7:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza sembra essere andata bene, se ti interessa raccontaci la tua esperienza continueremo a migliorare")
            else:
                feedback_gen=""
            
            # ADDITIONAL COMMENT 
            if var_b1=="NO":
                if media_tot ==1:
                    pass
                elif media_tot < 4.5:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("La tua ESPERIENZA COMPLESSIVA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(media_tot)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_a2 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area APPUNTAMENTO è molto carente con un risultato di "+str(var_a2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_accoglienza < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area ACCOGLIENZA PAZIENTE è molto carente con un risultato di "+str(med_accoglienza)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura. Essendo una delle aree più importanti per noi ci piacerebbe avere il tuo parere.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_proc < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area PROCEDURE è molto carente con un risultato di "+str(med_proc)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_f3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area RISULTATI è molto carente con un risultato di "+str(var_f3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_experience < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area dell'ESPERIENZA VISSUTA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(med_experience)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                else:
                    add_comm=""
            
            elif var_b1=="SI":
                if media_tot ==1:
                    pass
                elif media_tot < 4.5:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("La tua ESPERIENZA COMPLESSIVA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(media_tot)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_a2 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area APPUNTAMENTO è molto carente con un risultato di "+str(var_a2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    add_comm=colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_sito < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area SITO WEB è molto carente con un risultato di "+str(med_sito)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_accoglienza < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area ACCOGLIENZA PAZIENTE è molto carente con un risultato di "+str(med_accoglienza)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura. Essendo una delle aree più importanti per noi ci piacerebbe avere il tuo parere.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_proc < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area PROCEDURE è molto carente con un risultato di "+str(med_proc)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_f3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area RISULTATI è molto carente con un risultato di "+str(var_f3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_experience < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area dell'ESPERIENZA VISSUTA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(med_experience)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                else:
                    add_comm=""
            
            @st.cache_resource()
            def classif_nlp(str):
                # str to classify
                emotion_classifier = EmotionClassifier()
                resp1=emotion_classifier.predict([str])
                sentiment_classifier = SentimentClassifier()
                resp2=sentiment_classifier.predict([str])
                return resp1, resp2
                
            cols_text=st.columns([0.5,1])
            cols_text[0].subheader("Test the sentiment of your comment")
            cols_text[0].write("")
            but= cols_text[0].button("Test Sentiment 🔝 😐 👎")
            if but:
                if feedback_gen=="":
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("Inserisci un commento")
                    emozione=""
                    sentiment=""
                else:
                    resp1, resp2 = classif_nlp(feedback_gen)
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    # force the classification to limit outlier
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    else:
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
            
            submitted = st.button(label="Submit")
            if submitted==True:
                if feedback_gen=="":
                    emozione=""
                    sentiment=""
                else:  
                    resp1, resp2 = classif_nlp(feedback_gen)
                    emozione=resp1[0]
                    sentiment=resp2[0]
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                    else:
                        pass
                st.success("Successfully")
                st.balloons()
                if var_b1=="SI":
                    #Storing data
                    datetime_object = datetime.datetime.now()
                    add_row_to_gsheet(
                    df, [[var_a1, var_a2, var_a3,
                            var_b1, var_b2, var_b3,
                            var_c1, var_c2, var_c3,
                            var_d1, var_d2, var_d3, var_d4, var_d5, var_d6, var_d7,
                            "", "", 
                            var_f1, var_f2, var_f3,
                            "","", "", "","",
                            var_h1, var_h2, "","", var_h5, "", var_h7,"", var_h9, 
                            var_i1, var_i2, 
                            feedback_gen, 
                            str(datetime_object),  "Form_medio",  add_comm,  emozione,  sentiment]])
                else:
                    #Storing data
                    datetime_object = datetime.datetime.now()
                    add_row_to_gsheet(
                    df, [[var_a1, var_a2, var_a3,
                            var_b1, "", "",
                            var_c1, var_c2, var_c3,
                            var_d1, var_d2, var_d3, var_d4, var_d5, var_d6, var_d7,
                            "", "", 
                            var_f1, var_f2, var_f3,
                            "","", "", "","",
                            var_h1, var_h2, "","", var_h5, "", var_h7,"", var_h9, 
                            var_i1, var_i2, 
                            feedback_gen, 
                            str(datetime_object),  "Form_medio",  add_comm,  emozione,  sentiment]])
        
        # ###FORM 3
        if slider>7:
            col1,  col2 = st.columns([1, 0.60])
            with col1:
                new_title = '<b style="font-family:serif; color:#FF0000; font-size: 40px;">📋 MEDi Experience Form:</b>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.info("➡️ 1. Come ha preso l'appuntamento?")
                cols = st.columns((1, 1, 1.7))
                #APPUNTAMENTO
                var_a1 = cols[0].selectbox("Ho preso un appuntamento:",  ["Personalmente",  "Telefono",  "Sito Web", "E-mail",  "Tramite medico",  "Altro"])
                var_a2= cols[1].slider("Quanto è soddisfatto della facilità di fissare un appuntamento?", 1, 7, 1)
                var_a3= cols[2].select_slider('Quanto tempo è trascorso tra la segnalazione del medico e l\'appuntamento?',options=["< 1 settimana", "< 1 mese", "1-3 mesi", "3-6 mesi", "> 6 mesi"])
                
                #SITO WEB
                st.info("➡️ 2. Informazioni sul sito nostro sito web")
                cols2 = st.columns((3))
                var_b1 = cols2[0].selectbox("Avete visitato il nostro sito web", ["SI", "NO"])
                if var_b1=="SI":
                    var_b2 = cols2[1].slider("Se sì, quanto è soddisfatto delle informazioni che trova sul nostro sito web?", 1, 7, 1)
                    var_b3 = cols2[2].slider("Se sì, quanto è soddisfatto della facilità di utilizzo del nostro sito web?", 1, 7, 1)
                else:
                    var_add= cols2[1].selectbox("Non hai visitato il nostro sito web per quale motivo?", ["Ho avuto difficoltà a trovarlo", "Non mi interessa visitarlo", "Altro"])
                    if var_add=="Altro":
                        var_add2=cols2[2].text_input("Se vuoi inserisci la motivazione")

            #ACCOGLIENZA
            st.info("➡️ 3. Sull'accoglienza del nostro dipartimento")
            cols2 = st.columns((3))
            var_c1 = cols2[0].slider("Quanto è soddisfatto dell'accoglienza del nostro reparto?", 1, 7, 1)
            var_c2 = cols2[1].slider("Quanto è soddisfatto del tempo che ha dovuto attendere per essere aiutato alla reception?", 1, 7, 1)
            var_c3 = cols2[2].slider("Quanto è soddisfatto delle istruzioni ricevute per trovare l'area d'attesa corretta per la procedura?", 1, 7, 1)
                
            #PROCEDURA
            st.info("➡️ 4. Sulla procedura che le è stata prescritta")
            cols3 = st.columns((1.3,  1.7,  1,  1,  1,  1,  1.6))
            var_d1 = cols3[0].selectbox("A quale procedura di imaging medico si è sottoposto?", ["RMN", "CT", "Ultrasuoni", "Raggi X", "Mammografia", "Artrografia/Mielografia", "Interventi/Biopsie", "Altro"])
            var_d2 = cols3[1].slider("Quanto è soddisfatto del tempo di attesa nel reparto prima dell'inizio della procedura?", 1, 7, 1)
            options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90]
            if var_d1=="RMN":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(30))
            elif var_d1=="CT" or var_d1=="Mammografia":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(5))
            elif var_d1=="Ultrasuoni" or var_d1=="Artrografia/Mielografia" or var_d1=="Interventi/Biopsie":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(20))
            elif var_d1=="Raggi X":
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90], index=options.index(2))
            else:
                var_d3 = cols3[2].selectbox("Quanto tempo è durata la visita? (minuti)", options=[1, 2, 3, 4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,70,80,90],  index=options.index(1))
            var_d4 = cols3[3].selectbox("Si è sentito sicuro durante la procedura?", ["SI", "NO", "Indifferente"])
            var_d5 = cols3[4].selectbox("Ha provato dolore a causa della procedura?", ["SI", "NO", "Indifferente"])
            var_d6 = cols3[5].selectbox("Ha provato ansia durante la procedura?", ["SI", "NO", "Indifferente"])
            var_d7 = cols3[6].slider("Quanto è soddisfatto della durata della procedura stessa?", 1, 7, 1)
            
            #INFORMAZIONI PROCEDURA
            st.info("➡️ 5. Informazioni sulle procedure")
            cols3 = st.columns((1, 1))
            var_e1 = cols3[0].selectbox("Ha ricevuto informazioni scritte sulla procedura?", ["SI", "NO"])
            var_e2 = cols3[1].slider("Ha consultato un professionista della salute per farsi spiegare i risultati?", 1,  7,  1)
            
            #SPIEGAZIONE RISULTATI
            st.info("➡️ 6. Spiegazioni risultati del dipartimento")
            cols3 = st.columns((1, 1, 1))
            var_f1 = cols3[0].selectbox("Si è rivolto a un operatore sanitario dopo la visita in reparto?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f2 = cols3[1].selectbox("Ha consultato un professionista della salute per farsi spiegare i risultati?", ["NO", "Si, radiologo (medico)", "Si, tecnico radiologia", "Altro specialista"])
            var_f3 = cols3[2].slider("Quanto è soddisfatto della spiegazione fornita dal radiologo?", 1,  7,  1)
            
            #TEMPO ATTESA RISULTATI
            st.info("➡️ 7. Tempo di attesa risultati")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_g1 = cols3[0].selectbox("Quanto tempo dovrete aspettare per i risultati?", ["Li ho già", "< 1 settimana", "< 1 mese", "1-3 mesi", "3-6 mesi", "> 6 mesi"] )
            var_g2 = cols3[1].selectbox("L'attesa è quella che mi aspettavo e che mi era stata anticipata? ", ["SI", "NO"])
            var_g3 = cols3[2].slider("Quanto è soddisfatto del tempo di attesa dei risultati? ", 1,  7,  1)
            var_g4 = cols3[3].selectbox("Riceverà i risultati dal medico che l'ha inviata qui? ", ["SI", "NO"])
            var_g5 = cols3[4].selectbox("Il medico le spiegherà i risultati? ", ["SI", "NO"])
            
            #ESPERIENZA COME PAZIENTE
            st.info("➡️ 8. Com'è stata la sua esperienza nel reparto come paziente")
            cols3 = st.columns((1, 1, 1, 1, 1))
            var_h1 = cols3[0].slider("Quanto è soddisfatto della disponibilità di servizi igienici? ", 1,  7,  1)
            var_h2 = cols3[1].slider("Quanto è soddisfatto della pulizia del reparto? ", 1,  7,  1)
            var_h3 = cols3[2].slider("Quanto è soddisfatto della disponibilità di acqua potabile o di altre bevande? ", 1,  7,  1)
            var_h4 = cols3[3].slider("Quanto è soddisfatto del numero di posti a sedere nelle aree	di attesa?", 1,  7,  1)
            var_h5 = cols3[4].slider("Quanto è soddisfatto della cordialità del personale ", 1,  7,  1)
            
            cols3 = st.columns((1, 1, 1, 1))
            var_h6 = cols3[0].slider("Quanto è soddisfatto dell'ambiente (temperatura, rumore...) nel reparto? ", 1,  7,  1)
            var_h7 = cols3[1].slider("Ha ritenuto che la sua privacy sia stata rispettata? ", 1,  7,  1)
            var_h8 = cols3[2].selectbox("Tornerebbe nel nostro reparto di radiologia per un'altra procedura", ["SI", "NO"])
            var_h9 = cols3[3].selectbox("Consiglierebbe il nostro reparto di radiologia ai suoi familiari e amici", ["SI", "NO"])
            
            #INFO PAZIENTE
            st.info("➡️ 9. La nostra analisi delle vostre risposte")
            cols3 = st.columns((1, 1))
            var_i1= cols3[0].select_slider('Potrebbe indicarci il suo gruppo di età (facoltativo)?',options=["< 18 anni",	"18-30anni", 	"30-65anni",  ">65 anni" ])
            var_i2= cols3[1].selectbox('Può indicarci il suo sesso (facoltativo)?',options=["Maschio", "Femmina", "Non Specificato"  ])
            
            with col2:
                if var_b1=="NO":
                    med_accoglienza=(var_c1+var_c2+var_c3)/2
                    med_experience=(var_h1+var_h2+var_h3+var_h4+var_h5+var_h6+var_h7)/7
                    med_proc=(var_d2+var_d7)/2
                    DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                                {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                                {"taste": "PROCEDURE", "Peso Area": med_proc},
                                {"taste": "TEMPO ATTESA RISULTATI", "Peso Area": var_g3},
                                {"taste": "RISULTATI", "Peso Area": var_f3},
                                {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                    graph_pes(DATA)
                    media_tot=(med_accoglienza+var_g3+med_experience+var_a2+var_d2+var_f3)/6
                elif var_b1=="SI":
                    med_accoglienza=(var_c1+var_c2)/2
                    med_sito=(var_b2+var_b3)/2
                    med_experience=(var_h1+var_h2+var_h3+var_h4+var_h5+var_h6+var_h7)/7
                    med_proc=(var_d2+var_d7)/2
                    DATA = [{"taste": "APPUNTAMENTO", "Peso Area": var_a2},
                                {"taste": "SITO WEB", "Peso Area": med_sito},
                                {"taste": "ACCOGLIENZA", "Peso Area": med_accoglienza},
                                {"taste": "PROCEDURE", "Peso Area": med_proc},
                                {"taste": "TEMPO ATTESA RISULTATI", "Peso Area": var_g3},
                                {"taste": "RISULTATI", "Peso Area": var_f3},
                                {"taste": "ESPERIENZA", "Peso Area": med_experience}]
                    graph_pes(DATA)
                    media_tot=round(((med_accoglienza+med_sito+med_experience+var_a2+var_d2+var_f3+ var_g3)/7), 1)
            
            # COMMENT 1
            if media_tot ==1:
                pass
            elif media_tot<=4:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza può essere migliorata, raccontaci cosa ne pensi e miglioreremo sicuramente")
                        
            elif media_tot>4 and media_tot<=5:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza non è andata al massimo, se ti interessa raccontaci la tua esperienza e miglioreremo sicuramente i punti deboli della nostra struttura")
                        
            elif media_tot>5 and media_tot<=7:
                cols_text = st.columns((0.25, 1))
                cols_text[0].metric("Risultato della tua survey:", value=str(media_tot)+"/7")
                feedback_gen=cols_text[1].text_area("La tua esperienza sembra essere andata bene, se ti interessa raccontaci la tua esperienza continueremo a migliorare")
            else:
                feedback_gen=""
            
            # ADDITIONAL COMMENT 
            if var_b1=="NO":
                if media_tot ==1:
                    pass
                elif media_tot < 4.5:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("La tua ESPERIENZA COMPLESSIVA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(media_tot)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_a2 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area APPUNTAMENTO è molto carente con un risultato di "+str(var_a2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_accoglienza < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area ACCOGLIENZA PAZIENTE è molto carente con un risultato di "+str(med_accoglienza)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura. Essendo una delle aree più importanti per noi ci piacerebbe avere il tuo parere.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_proc < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area PROCEDURE è molto carente con un risultato di "+str(med_proc)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_g3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area TEMPO ATTESA RISULTATI è molto carente con un risultato di "+str(var_g3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_f3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area RISULTATI è molto carente con un risultato di "+str(var_f3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_experience < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area dell'ESPERIENZA VISSUTA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(med_experience)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
            elif var_b1=="SI":
                if media_tot ==1:
                    pass
                elif media_tot < 4.5:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("La tua ESPERIENZA COMPLESSIVA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(media_tot)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_a2 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area APPUNTAMENTO è molto carente con un risultato di "+str(var_a2)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_sito < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area SITO WEB è molto carente con un risultato di "+str(med_sito)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_accoglienza < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area ACCOGLIENZA PAZIENTE è molto carente con un risultato di "+str(med_accoglienza)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura. Essendo una delle aree più importanti per noi ci piacerebbe avere il tuo parere.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_proc < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area PROCEDURE è molto carente con un risultato di "+str(med_proc)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_g3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area TEMPO ATTESA RISULTATI è molto carente con un risultato di "+str(var_g3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif var_f3 < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area RISULTATI è molto carente con un risultato di "+str(var_f3)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                elif med_experience < 4:
                    colss = st.columns([0.23, 0.02, 1])
                    colss[0].error("L'area dell'ESPERIENZA VISSUTA NELLA NOSTRA STRUTTURA è molto carente con un risultato di "+str(med_experience)+"/7. Vorremmo chiedere quali sono state le problematiche riscontrate nella nostra struttura.", icon="🚨")
                    colss[1].write("")
                    add_comm=colss[2].text_area("Scrivici cosa non ha funzionato. Miglioreremo grazie ai tuoi feedback. Il tuo parere è fondamentale per noi.")
                else:
                    add_comm=""
            
            @st.cache_resource()
            def classif_nlp(str):
                # str to classify
                emotion_classifier = EmotionClassifier()
                resp1=emotion_classifier.predict([str])
                sentiment_classifier = SentimentClassifier()
                resp2=sentiment_classifier.predict([str])
                return resp1, resp2
            
            #emotion classification (joy, fear, anger, sadness)
            cols_text=st.columns([0.5,1])
            cols_text[0].subheader("Test the sentiment of your comment")
            cols_text[0].write("")
            but= cols_text[0].button("Test Sentiment 🔝 😐 👎")
            if but:
                if feedback_gen=="":
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("Inserisci un commento")
                    emozione=""
                    sentiment=""
                else:
                    resp1, resp2 = classif_nlp(feedback_gen)
                    cols_text[1].write("")
                    cols_text[1].write("")
                    cols_text[1].write("")
                    # force the classification to limit outlier
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
                    else:
                        emozione=cols_text[1].subheader("Emozione trasmessa: "+resp1[0])
                        sentiment=cols_text[1].subheader("Sentiment analysis: "+resp2[0])
            
            submitted = st.button(label="Submit")
            if submitted==True:
                if feedback_gen=="":
                    emozione=""
                    sentiment=""
                else:  
                    resp1, resp2 = classif_nlp(feedback_gen)
                    emozione=resp1[0]
                    sentiment=resp2[0]
                    if media_tot >=5.5:
                        resp1[0]="joy"
                        resp2[0]="positive"
                    elif media_tot <=3.5:
                        resp1[0]="sadness"
                        resp2[0]="negative"
                    else:
                        pass
                st.success("Successfully")
                st.balloons()
                if var_b1=="SI":
                    #Storing data
                    datetime_object = datetime.datetime.now()
                    add_row_to_gsheet(
                    df, [[var_a1, var_a2, var_a3,
                            var_b1, var_b2, var_b3,
                            var_c1, var_c2, var_c3,
                            var_d1, var_d2, var_d3, var_d4, var_d5, var_d6, var_d7,
                            var_e1,  var_e2,  
                            var_f1, var_f2, var_f3,
                            var_g1, var_g2, var_g3, var_g4,var_g5,
                            var_h1, var_h2, var_h3,var_h4, var_h5, var_h6, var_h7,var_h8, var_h9, 
                            var_i1, var_i2, 
                            feedback_gen, 
                            str(datetime_object),  "Form_lungo",  add_comm,  emozione,  sentiment]])
                else:
                    #Storing data
                    datetime_object = datetime.datetime.now()
                    add_row_to_gsheet(
                    df, [[var_a1, var_a2, var_a3,
                            var_b1, "", "",
                            var_c1, var_c2, var_c3,
                            var_d1, var_d2, var_d3, var_d4, var_d5, var_d6, var_d7,
                            var_e1,  var_e2,  
                            var_f1, var_f2, var_f3,
                            var_g1, var_g2, var_g3, var_g4,var_g5,
                            var_h1, var_h2, var_h3,var_h4, var_h5, var_h6, var_h7,var_h8, var_h9, 
                            var_i1, var_i2, 
                            feedback_gen, 
                            str(datetime_object),  "Form_lungo",  add_comm,  emozione,  sentiment]])
    
                
    page_names_to_funcs = {
            "Form Patient Satisfaction": form_pazienti,
            "Dashboard Patient Satisfaction": dashboard_patient_satisf, 
            "Info Framework":landing_page}
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys(), key ="value")
    page_names_to_funcs[selected_page]()
