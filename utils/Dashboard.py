import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import numpy as np
import streamlit as st  # pip install streamlit
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from datetime import date
from datetime import timedelta
from wordcloud import WordCloud,  STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

#import altair as alt
from sklearn import datasets, ensemble
from sklearn.inspection import permutation_importance
import time
import statsmodels.api as sm
from streamlit_elements import elements, mui
from streamlit_elements import nivo
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from utils.addition.graphs import graph_pes

def dashboard_patient_satisf():
    img = Image.open('images/dashboard1_logo.png')
    st.image(img) 
    image3 = Image.open('images/Mehedi_logo2.png')
    
    #good, neutral, bad
    img_bad = Image.open('images/px_bad.png')
    img_neu = Image.open('images/px_neutral.png')
    img_good = Image.open('images/px_good.png')
    
    color1 = "#6082B6"
    color2 = "#89CFF0"
    
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
    
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:1rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)
    
    hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)
   
    def display_dial(title, value,  color):
     st.markdown(
         div(
             style=styles(
                 text_align="center",
                 color=color,
                 padding=(rem(0.8), 0, rem(3), 0),
             )
         )(
             h2(style=styles(font_size=rem(1.0), font_weight=600, padding=0))(title),
             big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(value),
         ),
         unsafe_allow_html=True,
    )
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
        #reading gsheet to dataframe
        sheet_url = "https://docs.google.com/spreadsheets/d/1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8/edit#gid=0"
        url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
        df=pd.read_csv(url_1)
        
        #SIDEBAR FILTRI
        st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
        new_title = '<p style="font-size: 22px;">🔁 Filtra ciò che ti interessa</p>'
        st.sidebar.markdown(new_title, unsafe_allow_html=True)
        st.sidebar.markdown("")
        a, b, c = st.sidebar.columns([0.05,1,0.05])
        with a:
            st.write("")
        with b:
            Proced_Fil=st.multiselect("Tipo Procedura", df["Tipo_procedura"].unique(),  default=["RMN", "Raggi X", "CT"])
            Sesso_Fil=st.multiselect("Sesso", df["Sesso"].unique(),  default=["Maschio", "Femmina", "Non Specificato"])
            Eta_Fil=st.multiselect("Fasce di età", df["Range_Età"].unique(),  default=["18-30anni"])
            st.image(image3, width=170)
            st.markdown("""
            <div align=center><small>
            Page views interaction: <img src="https://www.cutercounter.com/hits.php?id=hxndpfn&nd=6&style=52" border="0" alt="hit counter"><br>
            GitHub <a href="https://github.com/M-ballabio1/MeHEDI-app"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/M-ballabio1/MeHEDI-app?style=social"></a>
            </small></div>
            """, unsafe_allow_html=True)
        with c:
            st.write("")
        
        css='''
        [data-testid="metric-container"] {
            width: fit-content;
            margin: auto;
        }

        [data-testid="metric-container"] > div {
            width: fit-content;
            margin: auto;
        }

        [data-testid="metric-container"] label {
            width: fit-content;
            margin: auto;
        }
        '''
        st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
        
        
        #expander = st.expander("In questa sezione puoi verificare come sono state calcolate le differenti metriche")
        #with expander:
        #    st.write("In questa sezione dovrà esserci la dashbaord con i KPI riferiti all'ambito Patient Satisfaction-Healthcare")
        
        df_selection = df.query(
            "Tipo_procedura == @Proced_Fil & Sesso == @Sesso_Fil & Range_Età == @Eta_Fil")
        
        #lettura dataset column and groupby weekly
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d', exact=False).fillna(3)
        df1= df.groupby(pd.Grouper(key='Timestamp', axis=0,freq='1W')).count().fillna(3)
        df1.reset_index(inplace=True)

        #filter dataset only to date < to today (dd/mm/YY)
        today = date.today()
        # Yesterday date
        last_week = today - timedelta(days = 6)
        last_month = today - timedelta(days = 45)
        date_oggi = today.strftime('%Y-%m-%d')
        date_last_week = last_week.strftime('%Y-%m-%d')
        date_last_month = last_month.strftime('%Y-%m-%d')
        
        st.subheader("KPI per la settimana corrente delle principali macro-aree")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            len_report_sett_now=df1['Sesso'].iloc[-1]
            len_report_sett_last_week=df1['Sesso'].iloc[-2]
            delta_report=int(len_report_sett_now) - int(len_report_sett_last_week)
            st.metric("Report Inviati In Settimana",  value= str(int(len_report_sett_now))+" rep", delta=str(delta_report),  help="Numero totale di report inviati questa settimana rispetto a settimana scorsa")
        with col2:
            #Settimana attuale psi
            df2_att_scorsa_settimana=df.loc[(df['Timestamp'] >= str(date_last_week))]
            df2_medie_valori_week=df2_att_scorsa_settimana.mean().reset_index()
            df2_medie_valori_week.columns = ['variables', 'count']
            psi_this_week=round(df2_medie_valori_week["count"].mean(), 4)
            psi_perc=round((psi_this_week/7)*100,2)
            #Settimana precedente alla sett scorsa psi
            df2_prima_scorsa_settimana=df.loc[(df['Timestamp'] < str(date_last_week))]
            df2_medie_valori_prec_week=df2_prima_scorsa_settimana.mean().reset_index()
            df2_medie_valori_prec_week.columns = ['variables', 'count']
            psi_prima_last_week=round(df2_medie_valori_prec_week['count'].mean(), 4)
            #differenza tra i PSI
            delta_psi=round(((float(psi_this_week)-float(psi_prima_last_week))/7)*100, 2)
            st.metric("PSI Index",  value=str(psi_perc)+" %", delta=str(delta_psi)+" %", help="Patient Satisfaction Index (misura complessiva di grado di soddisfazione dei pazienti)")
        with col3:
            #Settimana attuale tws MEAN
            df2_medie_valori_tws_week=df2_att_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].mean().reset_index()
            df2_medie_valori_tws_week.columns = ['variables', 'count']
            tws_this_week=round(df2_medie_valori_tws_week["count"].mean(), 2)
            #Settimana attuale tws STD
            df2_dev_stand_valori_tws_week=df2_att_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].std().reset_index()
            df2_dev_stand_valori_tws_week.columns = ['variables', 'std']
            tws_this_week_std=round(df2_dev_stand_valori_tws_week["std"].mean(), 2)
            #Settimana precedente alla sett scorsa tws
            df2_medie_valori_prec_tws_week=df2_prima_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].mean().reset_index()
            df2_medie_valori_prec_tws_week.columns = ['variables', 'count']
            tws_prima_last_week=round(df2_medie_valori_prec_tws_week['count'].mean(), 2)
            #differenza tra i TWS
            delta_tws=round(float(tws_this_week)-float(tws_prima_last_week), 2)
            st.metric("TWS Index",  value=(str(tws_this_week)+"/7"+" ±"+str(tws_this_week_std)), delta=delta_tws,  help="Time Waiting Satisfaction Index (misura che elabora una media del grado di soddifazione del paziente legate al tempo d'attesa)")
        with col4:
            #Settimana attuale stru
            df2_medie_valori_stru_week=df2_att_scorsa_settimana[["Soddisf_Servizi_Igenici","Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere"]].mean().reset_index()
            df2_medie_valori_stru_week.columns = ['variables', 'count']
            stru_this_week=round(df2_medie_valori_stru_week["count"].mean(), 2)
            #Settimana precedente alla sett scorsa stru
            df2_medie_valori_prec_stru_week=df2_prima_scorsa_settimana[["Soddisf_Servizi_Igenici","Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere"]].mean().reset_index()
            df2_medie_valori_prec_stru_week.columns = ['variables', 'count']
            stru_prima_last_week=round(df2_medie_valori_prec_stru_week["count"].mean(), 2)
            #differenza tra i STRU
            delta_stru=round(float(stru_this_week)-float(stru_prima_last_week), 2)
            st.metric("Structural Index",  value=str(stru_this_week)+"/7", delta=delta_stru,  help="Structural Index (permette di calcolare una media della soddisfazione dei pazienti riguardo l'ambiente della struttura (servizi, posti a sedere ecc...)")
        with col5:
            #calcolo di un nuovo coefficiente di Digitalization
            sito_pren=df['Tipo_appun'].value_counts()["Sito Web"]
            email_pren=df['Tipo_appun'].value_counts()["E-mail"]
            # ho portato da percentuale centesimi a settesimi
            sit_ema_score=round(((sito_pren+email_pren)*7)/len(df), 2)
            
            #Settimana attuale dig
            df2_medie_valori_dig_week=df2_att_scorsa_settimana[["Info_sito","Facili_sito"]].mean().reset_index()
            df2_medie_valori_dig_week.columns = ['variables', 'count']
            dig_this_week=round(df2_medie_valori_dig_week["count"].mean(), 2)
            dig_score_att=round((dig_this_week+sit_ema_score)/2, 2)
            #Settimana precedente alla sett scorsa dig
            df2_medie_valori_prec_dig_week=df2_prima_scorsa_settimana[["Info_sito","Facili_sito"]].mean().reset_index()
            df2_medie_valori_prec_dig_week.columns = ['variables', 'count']
            dig_prima_last_week=round(df2_medie_valori_prec_dig_week["count"].mean(), 2)
            dig_score_last=(dig_prima_last_week+sit_ema_score)/2
            #differenza tra i DIG
            delta_dig=round(float(sit_ema_score)-float(dig_score_last), 2)
            st.metric("DIG Index",  value=str(dig_score_att)+"/7", delta=str(delta_dig),  help="Digitalization Index (permette di calcolare una media ponderata di grado di digitalizzazione della struttura rispetto ad una baseline)")
        
        #First row
        st.title("Area indicatori principali Health Patient Experience - filtrabile 🎯")
        if len(df_selection)==0:
            st.header("Business Rule Exception")
            st.warning("Non posso fare nessuna query se non è presente almeno un campo per ciascun selectbox")
        else: 
            a, b, c, d, e = st.columns([0.42, 0.01, 0.14, 0.01, 0.42])
            with a:
                #appuntamento
                appunt_media=round(df_selection["Sodd_fac_appun"].mean(), 2)
                #sito
                df['Visitato_Sito'] = np.where(df['Visita_sito'] == "SI", -0.5, 0.5)
                visita_sito_right=df['Visitato_Sito'].sum()
                visita_sito_right=visita_sito_right/len(df['Visitato_Sito'])
                sito_web_media=round(df_selection[['Info_sito', "Facili_sito"]].mean(), 2)
                sito_web_media=((sito_web_media[0]+sito_web_media[1])/2)+visita_sito_right
                #accoglienza
                accog_media=round(df_selection[["Sodd_acc_rep", "Sodd_tempo_attesa_rec", "Sodd_indica_area_visi"]].mean(), 2)
                accog_media=(accog_media[0]+accog_media[1]+accog_media[2])/len(accog_media)
                #procedure
                proc_media=round(df_selection[["Sodd-tempo_attes_reparto_pre", "Soddisf_procedura"]].mean(), 2)
                proc_media=(proc_media[0]+proc_media[1])/len(proc_media)
                #attesa risultati
                att_ris_media=round(df_selection["Soddisf_Tempo_Attesa_Risult"].mean(), 2)
                #risultati
                ris_media=round(df_selection["Soddisf_Spiegaz_Radiologo"].mean(), 2)
                st.header("Radar Chart Macro-Aree")
                #esperienza
                esp_media=round(df_selection[["Soddisf_Servizi_Igenici", "Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere", "Soddisf_Cordialità_staff", "Soddisf_Ambiente", "Soddisf_Privacy"]].mean(), 2)
                esp_media=(esp_media[0]+esp_media[1]+esp_media[2]+esp_media[3]+esp_media[4]+esp_media[5])/len(esp_media)
                st.subheader("")
                DATA = [{"taste": "APPUNTAMENTO", "Peso Area": appunt_media},
                            {"taste": "SITO WEB", "Peso Area": sito_web_media},
                            {"taste": "ACCOGLIENZA", "Peso Area": accog_media},
                            {"taste": "PROCEDURE", "Peso Area": proc_media},
                            {"taste": "TEMPO ATTESA RISULTATI", "Peso Area": att_ris_media},
                            {"taste": "RISULTATI", "Peso Area": ris_media},
                            {"taste": "ESPERIENZA", "Peso Area": esp_media}]
                graph_pes(DATA)
                st.write("")
                st.write("")
                st.write("")
                st.text("")
                with st.expander("ℹ️ Informazioni grafico", expanded=False):
                        st.markdown(
                            """
                            #### Explaination Plot
                            A radar chart is an informative visual tool in which multiple variables (three or more) and compared on a two-dimensional plane.

                            #### Radar chart
                            This plot is used by the healthcare facility to understand the result of the various macro-areas.
                            With the filters in the right area, you can understand how age, gender and types of procedure influence the survey result.""")

            with b:
                st.text("")
            with c:
                st.subheader("")
                st.subheader("")
                st.metric("Spiegazione KPIs",  value="", help="PEI=Indicatore per misurare il grado di soddisfazione medio delle procedure || CKI=Indicatore per misurare il grado di cordialità dello staff Medi || PSafy=Indicatore per misurare il grado di soddisfazione della privacy e sicurezza percepita")
                st.write("")
                perc_proc_media=round((proc_media/7)*100, 2)
                display_dial("Procedure Evaluation Index",  str(perc_proc_media)+"%",   color1)
                #st.metric("PEI ",  value="45%",  delta="-5%",  help="Procedure Evaluation Index Var_d2, var_d7")
                st.write("")
                st.write("")
                cki_1=round(df_selection[["Sodd_acc_rep", "Sodd_tempo_attesa_rec", "Soddisf_Cordialità_staff"]].mean(), 2)
                cki_media=round((cki_1[0]+cki_1[1]+cki_1[2])/3, 2)
                cki_1_media_per=round((cki_media/7)*100, 2)
                #st.metric("CKI ",  value="75%",  delta="+5%",  help="Cordiality & Kindness Index c1, c2, h5, ")
                display_dial("Cordiality & Kindness Index",  str(cki_1_media_per)+"%",  color1)
                st.write("")
                st.write("")
                #st.metric("PSafI ",  value="85%",  delta="+5%",  help="Privacy and Safety Index d4, d6, h7")
                psafi_1=round(df_selection["Soddisf_Privacy"].mean(), 2)
                psafi_1_media_per=round((psafi_1/7)*100, 2)
                #calcolo safety
                safy_si_pren=df['Sicur_visita'].value_counts()["SI"]

                # ho portato da percentuale centesimi a settesimi
                sit_safy_score=round(((safy_si_pren))/len(df['Sicur_visita']), 2)
                display_dial("Privacy and Safety Index",  str(psafi_1_media_per)+"%",  color1)
            with d:
                st.text("")
            with e:
                df_cat=df_selection[['Sodd_fac_appun',"Tipo_appun", "Tipo_procedura", "Tempo_segn_medic_app",  "Dolore_visita", "Sesso", "Range_Età"]]
                df_fin=df_cat.rename(columns={'Sodd_fac_appun':"Soddisfazione fac appuntamento","Tipo_appun": "Tipologia Appuntamento", "Tipo_procedura": "Tipologia Procedure", "Tempo_segn_medic_app": "Tempo tra segnalazione medico e visita", "Dolore_visita": "Dolore nelle procedure", "Sesso": "Sesso pazienti", "Range_Età": "Range Età pazienti"}, errors="raise")
                pie_filter=st.selectbox("", ["Tipologia Appuntamento", "Tipologia Procedure", "Tempo tra segnalazione medico e visita", "Sesso pazienti", "Range Età pazienti"])
                if pie_filter=="Tipologia Appuntamento":
                    st.header("Metodologia Appuntamento")
                    fig = px.pie(df_fin, values='Soddisfazione fac appuntamento', names='Tipologia Appuntamento', color_discrete_sequence=px.colors.sequential.RdBu)
                elif pie_filter=="Tipologia Procedure":
                    st.header("Tipologie visite effettuate")
                    val_0=df_fin['Tipologia Procedure'].value_counts()
                    fig = px.pie(df_fin, values=val_0.values, names=val_0.index,  color_discrete_sequence=px.colors.sequential.RdBu)
                elif pie_filter=="Tempo tra segnalazione medico e visita":
                    st.header("Tempistiche Segnalazione medico-visita")
                    val_1=df_fin['Tempo tra segnalazione medico e visita'].value_counts()
                    fig = px.pie(df_fin, values=val_1.values, names=val_1.index,  color_discrete_sequence=px.colors.sequential.RdBu)
                elif pie_filter=="Dolore nelle procedure":
                    st.header("Dolore nelle procedure")
                    val_2=df_fin['Dolore nelle procedure'].value_counts()
                    fig = px.pie(df_fin, values=val_2.values, names=val_2.index,  color_discrete_sequence=px.colors.sequential.RdBu)
                elif pie_filter=="Sesso pazienti":
                    st.header("Sesso pazienti")
                    val_3=df_fin['Sesso pazienti'].value_counts()
                    fig = px.pie(df_fin, values=val_3.values, names=val_3.index, color_discrete_sequence=px.colors.sequential.RdBu)
                else:
                    st.header("Range Età pazienti")
                    val_4=df_fin['Range Età pazienti'].value_counts()
                    fig = px.pie(df_fin, values=val_4.values, names=val_4.index, color_discrete_sequence=px.colors.sequential.RdBu)
                fig.show()
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("ℹ️ Informazioni grafico", expanded=False):
                        st.markdown(
                            """
                            #### Pie chart
                            This graph is used to understand which is the most used method of booking visits.
                            In particular, the DIG index makes it possible to discriminate between patients who are more inclined to 
                            technology as they book via website or e-mail. This aspect could be highlighted perhaps during the application of the filters on the left.""")

            df3=df.copy()
            #st.write(df3)
            df3["FCorto"]=df3["Type_Form"]=="Form_corto"
            df3["FMedio"]=df3["Type_Form"]=="Form_medio"
            df3["FLungo"]=df3["Type_Form"]=="Form_lungo"
        
        #first-sec row
        df4= df.groupby(pd.Grouper(key='Timestamp', axis=0,freq='1W')).mean().reset_index()
        df4["PX"]=round(df4[["Soddisf_Servizi_Igenici", "Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere", "Soddisf_Cordialità_staff", "Soddisf_Privacy"]].mean(axis=1), 2)
        df4["target"]=10
        df4["MA_PX"]=df4["PX"].rolling(2).mean()
        
        ml_df=df4
        X = ml_df.drop(columns=['PX',  "Timestamp"]).fillna(df4.mean())
        y = ml_df["PX"]
        
        col0, col1, col2 = st.columns([0.02, 1, 0.02])
        with col0:
            st.write("")
        with col1:
            # first bar plot
            df42= df.groupby(pd.Grouper(key='Timestamp', axis=0,freq='1W')).count().reset_index()
            df42.rename(columns={'Sesso':'Form_Inviati'}, inplace=True)
            df42["target"]=10
            df42["MA_REPORT"]=df42["Form_Inviati"].rolling(2).mean()
            st.header("Bar Chart Numero report inviati per settimana")
            fig=px.bar(df42, x ="Timestamp", y='Form_Inviati', color='Form_Inviati',template = 'ggplot2',width=800, height=400)
            fig.add_trace(go.Scatter(x=df42['Timestamp'], y=df42["target"],mode='lines', line=dict(color="blue"), name='Safety Target'))
            fig.add_trace(go.Scatter(x=df42['Timestamp'], y=df42["MA_REPORT"],mode='lines', line=dict(color="orange"), name='Media mobile'))
            fig.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("")
        
        st.write("")
        st.progress(100, text="")
        st.write("")
        
        #TIME MANAGEMENT AREA
        st.title("Time Management Area ⌛")
        co1, s,  co2=st.columns([1, 0.05,  1])
        with co1:
            # second stacked bar chart
            # group the data by week and Tempo_segn_medic_app, count the occurrences of each category, and reset the index
            st.header("Tempo trascorso tra la segnalazione del medico e appuntamento")
            df_grouped = df.groupby([pd.Grouper(key='Timestamp', freq='1W'), 'Tempo_segn_medic_app'])['Tempo_segn_medic_app'].count().reset_index(name='count')

            # create a stacked bar chart using Plotly
            fig = px.bar(df_grouped, x='Timestamp', y='count', color='Tempo_segn_medic_app', barmode='stack')
            fig.show()
            st.plotly_chart(fig)
        with s:
            st.write("")
        with co2:
            # third stacked bar chart
            # group the data by week and Tempo_segn_medic_app, count the occurrences of each category, and reset the index
            st.header("Tempo di attesa per ricevere risultati rispetto alla compilazione form")
            df_grouped = df.groupby([pd.Grouper(key='Timestamp', freq='1W'), 'Tempo_attesa_per_risultati'])['Tempo_attesa_per_risultati'].count().reset_index(name='count')

            # create a stacked bar chart using Plotly
            fig = px.bar(df_grouped, x='Timestamp', y='count', color='Tempo_attesa_per_risultati', barmode='stack')
            fig.show()
            st.plotly_chart(fig)
        
        
        #Before the second row
        st.header("Tempo teorico vs Tempo stimato")
        st.write("Tempo stimato e il delta rappresenta differenza tra Tempo teorico medio - Tempo effettivo medio (stimato pazienti)")
        
        def calculate_mean_std(df):
            grouped_df = df.groupby("Tipo_procedura")["Tempo_stim_visita"]
            mean = grouped_df.mean()
            std = grouped_df.std()
            return mean, std
        
        mean_time,  std_time = calculate_mean_std(df)
        
        # Theoretical exam time
        rmn_theorical_time = 30
        ct_theorical_time = 5
        raggi_theorical_time = 2
        mammografia_theorical_time = 5
        ultrasuoni_theorical_time = 20
        biopsie_theorical_time = 20
        artografia_theorical_time = 20

        # Define the procedure types
        procedure_types = ["RMN", "CT", "Raggi X", "Mammografia", "Ultrasuoni",  "Interventi/Biopsie", "Artrografia/Mielografia"]

        # Calculate the mean and standard deviation for each procedure type
        mean_time, std_time = calculate_mean_std(df)

        # Get the difference between theoretical and mean exam time
        diff_time = [rmn_theorical_time - mean_time.loc["RMN"],
                     ct_theorical_time - mean_time.loc["CT"],
                     raggi_theorical_time - mean_time.loc["Raggi X"],
                     mammografia_theorical_time - mean_time.loc["Mammografia"],
                     ultrasuoni_theorical_time - mean_time.loc["Ultrasuoni"],
                     biopsie_theorical_time - mean_time.loc["Interventi/Biopsie"],
                     artografia_theorical_time - mean_time.loc["Artrografia/Mielografia"]]

        # Divide the screen into 7 columns
        columns = st.columns(7)
        
        # Create a metric element for each procedure type and place it in a separate column
        for i, procedure in enumerate(procedure_types):
            columns[i].metric(label=procedure, value=f"{round(mean_time.loc[procedure], 2)} min", delta=round(diff_time[i], 2)) 
        
        
        st.write("")
        st.progress(100, text="")
        st.write("")

        # Second row
        #calcolo Patient Experience ogni 1 week
        st.title("Predictive Modeling e Data Analysis per Forecasting PX 📈")
        
        col0, col1, col2 = st.columns([1.1, 0.01, 1])
        with col0:
            st.subheader("Feature Importance to predict PSI")
            ##features importance
            X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.05, random_state=13)

            params = {
            "n_estimators": 500,
            "max_depth": 4,
            "min_samples_split": 5,
            "learning_rate": 0.01,
            "loss": "squared_error"}
            
            reg = ensemble.GradientBoostingRegressor(**params)
            reg.fit(X_train, y_train)
            
            feature_importance = reg.feature_importances_
            sorted_idx = np.argsort(feature_importance)
            pos = np.arange(sorted_idx.shape[0]) + 0.5
            fig, ax = plt.subplots(facecolor="#E4E3E3")
            plt.barh(pos, feature_importance[sorted_idx], align="center")
            plt.yticks(pos, np.array(ml_df.columns.values)[sorted_idx])
            st.pyplot(fig)
            plt.show()
            
            label_best_features=(np.array(ml_df.columns.values)[sorted_idx][-1]) #aggiorna la feature più predittiva
        with col1:
            st.write("")
        with col2:
            st.subheader("Correlation Matrix")
            # Correlation Matrix in Content
            st.write("")
            df_corr = df.corr()
            fig_corr = go.Figure([go.Heatmap(z=df_corr.values,
                                             x=df_corr.index.values,
                                             y=df_corr.columns.values)])
            fig_corr.update_layout(height=580,
                                   width=1000,
                                   margin={'l': 20, 'r': 20, 't': 0, 'b': 0})
            st.plotly_chart(fig_corr, use_container_width=True)
        
        #algorithms
        def training_ml(x,  y):
            X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.05, random_state=13)

            params = {
            "n_estimators": 500,
            "max_depth": 4,
            "min_samples_split": 5,
            "learning_rate": 0.01,
            "loss": "squared_error"}
            
            reg = ensemble.GradientBoostingRegressor(**params)
            reg.fit(X_train, y_train)

            pred=reg.predict(X_test)
            
            mse = mean_squared_error(y_test, pred)
            print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
            #take the first prediction
            return pred[-1]
        
        #check preds (1 e 7)
        pred = training_ml(X,  y)
        if pred>7:
            pred=7
        elif pred<1:
            pred=1
        else:
            if df4["PX"].iat[-2] and df4["PX"].iat[-1] > pred:
                pred=pred+1
            elif df4["PX"].iat[-2] and df4["PX"].iat[-1] < pred:
                pred=pred-1
            elif df4["PX"].iat[-1] > pred:
                pred=pred+0.5
            elif df4["PX"].iat[-1] < pred:
                pred=pred-0.5
            else:
                pass
            
        
        #media mobile e target
        df4["MA_PX"]=df4["PX"].rolling(2).mean()
        df4["target_sicurezza_PX"]=4
        
        col0, col01,  col1,col2, col3 = st.columns([0.2,0.05,  1, 0.05, 0.25])
        with col0:
            st.write("")
            st.write("")
            if df4["PX"].iat[-1] >5.5:
                st.write("")
                st.subheader("✅ Continua così")
                st.success("Come puoi vedere il livello di Patient Satisfaction della nostra struttura è abbastanza alto. Tieni alta l'attenzione e cerca di concentrarti sulle aree più carenti!")
            elif df4["PX"].iat[-1]< 5.5 and df4["PX"].iat[-1] > 4:
                st.write("")
                st.subheader("🤖 Si potrebbe migliorare")
                st.warning("Sicuramente si potrebbero rivedere alcuni aspetti perchè il livello di Patient Satisfaction è ancora accettbile, ma dobbiamo fare di più. Come noti hai un Patient Satisfaction index di "+str(psi_perc)+"%. Non è sufficiente bisogna fare di più.")
            else:
                st.write("")
                st.subheader("⚠ Attenzione bisogna intervenire!")
                st.error("Bisogna intervenire immediatamente per invertire questo trend negativo di Patient Satisfaction. Non è più ancora accettbile.")
        with col01:
            st.write("")
        with col1:
            st.header("Line Chart Patient Experience per settimana")
            fig = go.Figure([go.Scatter(x=df4['Timestamp'], y=df4['PX'], name='Patient Satisfaction')])
            fig.update_layout(yaxis_range=[1, 7])
            fig.add_trace(go.Scatter(x=df4['Timestamp'], y=df4["MA_PX"],mode='lines', line=dict(color="orange"), name='Media Mobile a 2 week'))
            fig.add_trace(go.Scatter(x=df4['Timestamp'], y=df4["target_sicurezza_PX"],mode='lines', line=dict(color="blue"), name='Safety Target'))
            fig.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("")
        with col3:
            st.write("")
            delta_psiprev=pred-df4["PX"].iat[-1]
            delta_psiprev=round(float(delta_psiprev), 2)
            preds=round(float(pred), 3)
            st.metric("Prevedo che settimna prossima PSI", str(preds),  str(delta_psiprev)+"/7", help="Patient Satisfaction Index stimata sulla base di algoritmo di ML (Gradient Boosting) che considera tutte le varibaili del dataset")
            st.write("")
            if df4["PX"].iat[-1] >5.5:
                st.image(img_good, width=300) 
            elif df4["PX"].iat[-1] < 5.5 and df4["PX"].iat[-1] > 4:
                st.image(img_neu, width=300)
            else:
                st.image(img_bad, width=300)
        
        # Third row

        #df_new = px.data.tips()
        #calcolo Patient Experience ogni 1 day
        df5= df.groupby(pd.Grouper(key='Timestamp', axis=0,freq='D')).mean().reset_index()
        df5["PX"]=round(df5[["Soddisf_Servizi_Igenici", "Soddisf_Tempo_Attesa_Risult",  "Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere", "Soddisf_Cordialità_staff", "Soddisf_Privacy"]].mean(axis=1), 2)
        #mean_px_daily=round(df5[["Soddisf_Servizi_Igenici", "Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere", "Soddisf_Cordialità_staff", "Soddisf_Privacy"]].mean(), 2)
        
        df5["PX"].fillna(value=3.5, inplace=True)
        df5["Soddisf_Tempo_Attesa_Risult"].fillna(value=3.5, inplace=True)
        
        X = df5.Soddisf_Tempo_Attesa_Risult.values.reshape(-1, 1)
        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        
        st.header("OLS Regression")
        a,b,c=st.columns([1,1,1])
        with a:
            st.subheader("PSI e Soddisfazione Tempo d'attesa Risultati")
            fig = px.scatter(df5, x='Soddisf_Tempo_Attesa_Risult', y='PX', opacity=0.65, trendline="ols", trendline_color_override="red")
            st.plotly_chart(fig, use_container_width=True)
        with b:
            st.subheader("PSI e Soddisfazione Pulizia")
            fig = px.scatter(df5, x='Soddisf_Pulizia_Reparto', y='PX', opacity=0.65, trendline="ols", trendline_color_override="red")
            st.plotly_chart(fig, use_container_width=True)
        with c:
            st.subheader("PSI e Soddisfazione Privacy")
            fig = px.scatter(df5, x='Soddisf_Privacy', y='PX', opacity=0.65, trendline="ols", trendline_color_override="red")
            st.plotly_chart(fig, use_container_width=True)

        st.write("")
        st.progress(100, text="")
        st.write("")
        
        
        # Fourth Row
        st.title("Natural Language Processing Analysis based on comments 🗣️")
        st.subheader("")
        col1,col2, col3 = st.columns([1, 1, 1])
        with col1:
            coment=len(df)
            comment_full=df['Comment_Text'].isna().sum()
            form_with_comment=round(((coment-comment_full)/coment)*100, 2)
            st.metric("% Form con commenti",  value=str(form_with_comment)+"%",  help="% Persone che hanno fatto un commento ")
        with col2:
            parole_positive = ["professionalità", "competenza", "efficacia", "precisione", "attenzione", "impegno", "competenza", "efficacia","precisione", 
                                        "attenzione", "impegno", "cura", "comprensione", "empatia", "discrezione", 
                                        "riservatezza", "rispetto", "gentilezza", "cordialità", "cortesia", "umanità", "dolcezza", "disponibilità", "agio", "dedizione", "positiva", "ritornerò", "pulito", "eccellente", "fiducia"]
            parole_negative = [ "bruttissime", "bruttissimo", "antipatia", "dispetto", "mancanza", "abbandonato", "scarso", "mancanza", "abbandonato", "scarso", "scandalosi", "scandaloso", "incapaci", "furto", "ignorato", "delusa", "delusione", "sgarbato", 
                                    "scorbutico", "negativa", "lentezza", "disagio", "ritardo", "incompetenza", "discutibile", "imbarazzante", "arrabbiato", "sporco", "indecente", "trasandato", "pessimo"]
            
            commenttext_merged_withcomma= df['Comment_Text'].str.cat(sep=' ')
            text_lowercase=commenttext_merged_withcomma.lower()
            
            risultato_pos = 0
            # Counter parole negative
            for elemento in parole_positive:
                if elemento in text_lowercase:
                    risultato_pos += 1
                
            risultato_neg = 0
            # Counter parole negative
            for elemento in parole_negative:
                if elemento in text_lowercase:
                    risultato_neg += 1
                    
            perc_ris_neg=round((risultato_neg/(len(text_lowercase)))*100, 2)
            st.metric("% Risultati Negativi",  value=str(perc_ris_neg)+"%",  help="Percentuale Key-Words Negative sul totale parole inserite nei form e filtrate")
        with col3:
            ris_neg=round(((risultato_pos/risultato_neg)), 2)
            delta_ris_neg=round((ris_neg-1), 2)
            st.metric("Sentiment Analysis Score", value=ris_neg, delta=str(delta_ris_neg) ,  help="Rapporto Positivi-Negativi. Calcola qual è il rapporto tra Key-words positive e negative se > 0 allora sono più quelle positive.")
        
        col1,col2, col3,  col4,  col5= st.columns([2,0.05, 0.8, 0.02, 1.1 ])
        with col1:
            st.header("Word Cloud Patient Form")
            commenttext_merged= df['Comment_Text'].str.cat(sep=' , ')
            text_propercase=commenttext_merged.title()
            text_propercase.replace("Non", "")
            # Create and generate a word cloud image:
            stop_words =STOPWORDS.update(["La ", "Non ", "Mi ", "E ", "Il ", "Dei ", "Di ", "Degli ", "Lo ",  "Della ", "C'Era ", ", ",  "Del ",  "Per ", "Sotto ", "Alcuni", "Alcune ", "Ok "
                                    , "Rispetto!","Degli ",  "Ho ", "E' ",  "Da ",  "Un ",  "In ",  "Una ", "Dalla ", "Stata ", "Mia ", "Che ",  "Ma ",  "Tutto ",  "Sono "])
            wordcloud = WordCloud(stopwords = stop_words,background_color="#E4E3E3", width=800, height=500, colormap="Blues").generate(text_propercase)

            # Display the generated image:
            fig, ax = plt.subplots(facecolor="#E4E3E3")
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.subplots_adjust(left=-5, right=-2, top=-2, bottom=-5)
            plt.show()
            st.pyplot(fig)
        with col2:
            st.text("")
        with col3:
            st.header("Dataframe Key-Words")
            
            def word_count(str):
                counts = dict()
                words = str.split()

                for word in words:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1

                return counts
            
            commenttext_merged_withoutcomma= df['Comment_Text'].str.cat(sep=' , ')
            text_propercase=commenttext_merged_withoutcomma.title()
            
            #remove articles and preposition
            char_remov = ["La ", "Non ", "Mi ", "E ", "Il ", "Dei ", "Di ", "Degli ", "Lo ",  "Della ", "C'Era ", ", ",  "Del ",  "Per ", "Sotto ", "Alcuni", "Alcune ", "Ok "
                                    , "Rispetto!","Degli ",  "Ho ", "E' ",  "Da ",  "Un ",  "In ",  "Una ", "Dalla ", "Stata ", "Mia ", "Che ",  "Ma ",  "Tutto ",  "Sono "]
            for char in char_remov:
                # replace() "returns" an altered string
                text_propercase = text_propercase.replace(char, " ")
            
            counter_words=word_count(text_propercase)
            df_word_mode=pd.DataFrame.from_dict(counter_words, orient='index').reset_index()
            df_word_mode.columns = ["Key-Words", "Frequency"]
            df_word_mode.sort_values(by="Frequency", inplace=True, ascending=False)
            st.write(df_word_mode)
            
        with col4:
            st.text("")
        with col5:
            st.subheader("Top 5 Key-Words")
            fig = px.pie(df_word_mode.head(5), values='Frequency', names='Key-Words', color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        
        cols1,  cols2,  cols3=st.columns([1, 0.02, 0.35])
        with cols1:
            st.subheader("Word Cloud Negative Feedback")
            df_negative=df[df['Sentiment'] =="negative"]
            commenttext_merged_neg= df_negative['Comment_Text'].str.cat(sep=',')
            text_propercase_neg=commenttext_merged_neg.title()
            text_propercase_neg.replace("Non", "")
            text_propercase_neg.replace("Di", "")
            text_propercase_neg.replace("Sono", "")
            # Create and generate a word cloud image:
            stop_words =STOPWORDS.update(["La ", "Non ", "Mi ", "E ", "Il ", "Dei ", "Di ", "Degli ", "Lo ",  "Della ", "C'Era ", ", ",  "Del ",  "Per ", "Sotto ", "Alcuni", "Alcune ", "Ok "
                                    , "Rispetto!","Degli ",  "Ho ", "E' ",  "Da ",  "Un ",  "In ",  "Una ", "Dalla ", "Stata ", "Mia ", "Che ",  "Ma ",  "Tutto ",  "Sono "])
            wordcloud = WordCloud(stopwords = stop_words,background_color="#E4E3E3", width=800, height=175, colormap="Reds").generate(text_propercase_neg)
            fig, ax = plt.subplots(facecolor="#E4E3E3")
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.subplots_adjust(left=-5, right=-2, top=-2, bottom=-5)
            plt.show()
            st.pyplot(fig)
            
            st.subheader("Word Cloud Positive Feedback")
            df_positive=df[df['Sentiment'] =="positive"]
            commenttext_merged_pos= df_positive['Comment_Text'].str.cat(sep=',')
            text_propercase_pos=commenttext_merged_pos.title()
            text_propercase_pos.replace("Non", "")
            text_propercase_pos.replace("Di", "")
            text_propercase_pos.replace("Sono", "")
            # Create and generate a word cloud image:
            stop_words =STOPWORDS.update(["La ", "Non ", "Mi ", "E ", "Il ", "Dei ", "Di ", "Degli ", "Lo ",  "Della ", "C'Era ", ", ",  "Del ",  "Per ", "Sotto ", "Alcuni", "Alcune ", "Ok "
                                    , "Rispetto!","Degli ",  "Ho ", "E' ",  "Da ",  "Un ",  "In ",  "Una ", "Dalla ", "Stata ", "Mia ", "Che ",  "Ma ",  "Tutto ",  "Sono "])
            wordcloud = WordCloud(stopwords = stop_words,background_color="#E4E3E3", width=800, height=175, colormap="Greens").generate(text_propercase_pos)
            fig, ax = plt.subplots(facecolor="#E4E3E3")
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.subplots_adjust(left=-5, right=-2, top=-2, bottom=-5)
            plt.show()
            st.pyplot(fig)
        with cols2:
            st.write("")
        with cols3:
            df_tot_comment=df[~df.Sentiment.isnull()]
            neg_comm=round(len(df_negative)/len(df_tot_comment)*100, 2)
            pos_comm=round(len(df_positive)/len(df_tot_comment)*100, 2)
            st.header("")
            st.header("")
            st.metric("", "",  help="% Form negativi rispetto al totale form con commenti")
            display_dial("% Form con Commenti Negativi",  str(neg_comm)+"%",   "#a30000")
            st.write("")
            st.write("")
            st.header("")
            st.header("")
            st.header("")
            st.header("")
            st.metric("", "",  help="% Form positivi rispetto al totale form con commenti")
            display_dial("% Form con Commenti Positivi",  str(pos_comm)+" %",   "#065535")
        
        # Custom styling function
        def style_dataframe(row):
            if row['Sentiment'] == 'positive':
                return ['background-color: #b6e8b0'] * len(row)
            elif row['Sentiment'] == 'negative':
                return ['background-color: #f2867e'] * len(row)
            elif row['Sentiment'] == '':
                return ['background-color: #f5f7b5'] * len(row)
            else:
                return [''] * len(row)


        # Style pandas table
        th_props = [
            ('font-size', '14px'),
            ('text-align', 'center'),
            ('font-weight', 'bold'),
            ('color', '#hex color'),
            ('background-color', '#8fc0eb')
        ]

        td_props = [
            ('font-size', '12px')
        ]

        styles_df_css = [
            dict(selector="th", props=th_props),
            dict(selector="td", props=td_props)
        ]

        # Apply custom styling - df filtrabile
        styled_df = df_selection.style.apply(style_dataframe, axis=1)
        # Set additional styling options
        styled_df.set_table_styles(styles_df_css)
        # Display the styled DataFrame in Streamlit
        st.subheader("Dataframe Filtrato tramite query")
        st.dataframe(styled_df)
        
        # Apply custom styling - df filtrabile
        df = df.style.apply(style_dataframe, axis=1)
        # Set additional styling options
        df.set_table_styles(styles_df_css)
        # display complete df
        st.subheader("Dataframe completo")
        st.write(df)
        
        """
        #processi - strutture
        quality_str_m=df["Qualità struttura"].mean()
        quality_pro_m=df["Qualità processi"].mean()
        kpi_qua_str=round((quality_str_m+quality_pro_m)/2, 1)
        #kpi_qua_str=str(kpi_qua_str)*"%"
        df["KPI Percezione Strutturale"]=kpi_qua_str
        
        #sicurezza - qualità
        sicurezza=df["Sicurezza"].mean()
        quality_per=df["Qualità personale"].mean()
        pulizia=df["Pulizia"].mean()
        kpi_saf_str=round((sicurezza+quality_per+pulizia)/3, 1)
        #kpi_saf_str=str(kpi_saf_str)+"%"
        df["KPI Percezione Ambienti"]=kpi_saf_str
        
        #relational
        empatia=df["Empatia"].mean()
        chiare=df["Chiarezza"].mean()
        kpi_relazi=round((empatia+chiare)/2, 1)
        #kpi_relazi=str(kpi_relazi)+"%"
        df["KPI Percezione Relazionale"]=kpi_relazi
        
        #PSI
        kpi_psi=round((kpi_qua_str+kpi_saf_str+kpi_relazi)/3,1)
        
        #conditionally color kpi (rosso under 60)
        #l=[kpi_qua_str,kpi_saf_str,kpi_relazi,kpi_psi]
        #for i in l:
        
        g1, g2, g3, g4, g5 = st.columns(5)
        with g1:
            if kpi_qua_str < 65:
                color1="#EE4B2B"
            elif kpi_qua_str > 80:
                color1="#32CD32"
            else:
                color1 = "#1919e6"
            display_dial("KPI Percezione strutturale", str(kpi_qua_str)+"%", color1)
        with g2:
            if kpi_saf_str < 65:
                color1="#EE4B2B"
            elif kpi_saf_str > 80:
                color1="#32CD32"
            else:
                color1 = "#1919e6"
            display_dial("KPI Percezione ambienti", str(kpi_saf_str)+"%", color1)
        with g3:
            if kpi_relazi < 65:
                color1="#EE4B2B"
            elif kpi_relazi > 80:
                color1="#32CD32"
            else:
                color1 = "#1919e6"
            display_dial("KPI Percezione relazione", str(kpi_relazi)+"%", color1)
        with g4:
            if kpi_psi < 65:
                color1="#EE4B2B"
            elif kpi_psi > 80:
                color1="#32CD32"
            else:
                color1 = "#1919e6"
            display_dial("PSI (Patient Satisfaction Index)", str(kpi_psi)+"%", color1)
        with g5:
            display_dial("Numero Report inviati", str(len(df))+" rep", color1)
        
        
        css='''
        [data-testid="metric-container"] {
            width: fit-content;
            margin: auto;
        }
        
        [data-testid="metric-container"] > div {
            width: fit-content;
            margin: auto;
        }
        
        [data-testid="metric-container"] label {
            width: fit-content;
            margin: auto;
        }
        '''
        # I usually dump any scripts at the bottom of the page to avoid adding unwanted blank lines
        st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
            
         
        import matplotlib.pyplot as plt

        # data
        label = ["A", "B", "C"]
        val = [1,2,3]
        
        # append data and assign color
        label.append("")
        val.append(sum(val))  # 50% blank
        colors = ['red', 'blue', 'green', 'white']
        
        # plot
        fig = plt.figure(figsize=(8,6),dpi=100)
        ax = fig.add_subplot(1,1,1)
        ax.pie(val, labels=label, colors=colors)
        ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
        fig.show()
        
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Word Cloud Patient Form")
            text = Healthcare, hospital, sanità, monitoraggio, empatia, relazioni, sanità, pulizia,
                    goals, health, sanità pubblica, esperienza, bene, healthcare, sanità, ambiente,
                    pulito, sicuro, ospedale, ambulatorio, ambulatorio, healthcare, healthcare, sanità,
                    dottori, professionisti, settore in crescita, medicina generale, cardiologia,
                    radiologia, sanità, sanitario, health, health

            # Create and generate a word cloud image:
            wordcloud = WordCloud(
                background_color="#E4E3E3", width=450, height=500, colormap="Blues").generate(text)

            # Display the generated image:
            fig, ax = plt.subplots(facecolor="#E4E3E3")
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.subplots_adjust(left=-5, right=-2, top=-2, bottom=-5)
            plt.show()
            st.pyplot(fig)
       
        with col2:
            st.header("Health data")
            st.image("https://www.slideteam.net/media/catalog/product/cache/1280x720/p/a/patient_satisfaction_measurement_dashboard_service_ppt_show_vector_slide01.jpg")
         """
