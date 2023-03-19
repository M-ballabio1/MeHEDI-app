import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
#import altair as alt
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from datetime import date
from datetime import timedelta

#from streamlit_elements import elements, mui, html, sync, lazy
#from streamlit_elements import nivo

from wordcloud import WordCloud,  STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image


def dashboard_patient_satisf():
    img = Image.open('images/dashboard1_logo.png')
    st.image(img) 
    image3 = Image.open('images/Mehedi_logo2.png')
    
    color1 = "#1919e6"
    color2 = "#89CFF0"
    
    #serve per allargare margini da block-container
    st.markdown("""
    <style>
           .css-k1ih3n {
                padding-top: 2rem;
                padding-bottom: 4rem;
                padding-left: 4em;
                padding-right: 4rem;
            }
    </style>
    """, unsafe_allow_html=True)
    
    hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)
   
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
    
    expander = st.expander("In questa sezione puoi verificare come sono state calcolate le differenti metriche")
    with expander:
        st.write("In questa sezione dovrà esserci la dashbaord con i KPI riferiti all'ambito Patient Satisfaction-Healthcare")
    
    df_selection = df.query(
        "Tipo_procedura == @Proced_Fil & Sesso == @Sesso_Fil & Range_Età == @Eta_Fil")
    
    #lettura dataset column and groupby weekly
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%Y-%m-%d")
    df1= df.groupby(pd.Grouper(key='Timestamp', axis=0,freq='1W')).count()
    df1.reset_index(inplace=True)

    #filter dataset only to date < to today (dd/mm/YY)
    today = date.today()
    # Yesterday date
    last_week = today - timedelta(days = 6)
    date_oggi = today.strftime("%Y-%m-%d")
    date_last_week = last_week.strftime("%Y-%m-%d")
    #df1 = df1.loc[(df1['Timestamp'] <= date_oggi)]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        len_report_sett_now=df1['Sesso'].iloc[-1]
        len_report_sett_last_week=df1['Sesso'].iloc[-2]
        delta_report=int(len_report_sett_now) - int(len_report_sett_last_week)
        st.metric("Numero Report Inviati questa settimana",  value= str(int(len_report_sett_now))+" rep", delta=str(delta_report),  help="Numero totale di report inviati questa settimana rispetto a settimana scorsa")
    with col2:
        #Settimana attuale psi
        df2_att_scorsa_settimana=df.loc[(df['Timestamp'] >= date_last_week)]
        df2_medie_valori_week=df2_att_scorsa_settimana.mean()
        psi_this_week=round(df2_medie_valori_week[0].mean(), 2)
        psi_perc=round((psi_this_week/7)*100,2)
        #Settimana precedente alla sett scorsa psi
        df2_prima_scorsa_settimana=df.loc[(df['Timestamp'] <= date_last_week)]
        df2_medie_valori_prec_week=df2_prima_scorsa_settimana.mean()
        psi_prima_last_week=round(df2_medie_valori_prec_week[0].mean(), 2)
        #differenza tra i PSI
        delta_psi=round(((float(psi_this_week)-float(psi_prima_last_week))/7)*100, 2)
        st.metric("PSI Index",  value=str(psi_perc)+" %", delta=str(delta_psi)+" %", help="Patient Satisfaction Index (misura complessiva di grado di soddisfazione dei pazienti)")
    with col3:
        #Settimana attuale tws MEAN
        df2_medie_valori_tws_week=df2_att_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].mean()
        tws_this_week=round(df2_medie_valori_tws_week[0].mean(), 2)
        #Settimana attuale tws STD
        df2_dev_stand_valori_tws_week=df2_att_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].std()
        tws_this_week_std=round(df2_dev_stand_valori_tws_week[0].mean(), 2)
        #Settimana precedente alla sett scorsa tws
        df2_medie_valori_prec_tws_week=df2_prima_scorsa_settimana[["Sodd_tempo_attesa_rec","Sodd-tempo_attes_reparto_pre", "Soddisf_Tempo_Attesa_Risult"]].mean()
        tws_prima_last_week=round(df2_medie_valori_prec_tws_week[0].mean(), 2)
        #differenza tra i TWS
        delta_tws=round(float(tws_this_week)-float(tws_prima_last_week), 2)
        st.metric("TWS Index",  value=(str(tws_this_week)+"/7"+" ±"+str(tws_this_week_std)), delta=delta_tws,  help="Time Waiting Satisfaction Index (misura che elabora una media del grado di soddifazione del paziente legate al tempo d'attesa)")
    with col4:
        #Settimana attuale stru
        df2_medie_valori_stru_week=df2_att_scorsa_settimana[["Soddisf_Servizi_Igenici","Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere"]].mean()
        stru_this_week=round(df2_medie_valori_stru_week[0].mean(), 2)
        #Settimana precedente alla sett scorsa stru
        df2_medie_valori_prec_stru_week=df2_prima_scorsa_settimana[["Soddisf_Servizi_Igenici","Soddisf_Pulizia_Reparto", "Soddisf_Cibo_Bevande", "Soddisf_Posti_Sedere"]].mean()
        stru_prima_last_week=round(df2_medie_valori_prec_stru_week[0].mean(), 2)
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
        df2_medie_valori_dig_week=df2_att_scorsa_settimana[["Info_sito","Facili_sito"]].mean()
        dig_this_week=round(df2_medie_valori_dig_week[0].mean(), 2)
        dig_score_att=(dig_this_week+sit_ema_score)/2
        #Settimana precedente alla sett scorsa dig
        df2_medie_valori_prec_dig_week=df2_prima_scorsa_settimana[["Info_sito","Facili_sito"]].mean()
        dig_prima_last_week=round(df2_medie_valori_prec_dig_week[0].mean(), 2)
        dig_score_last=(dig_prima_last_week+sit_ema_score)/2
        #differenza tra i STRU
        delta_dig=round(float(sit_ema_score)-float(dig_score_last), 2)
        st.metric("DIG Index",  value=str(dig_score_att)+"/7", delta=str(delta_dig),  help="Digitalization Index (permette di calcolare una media ponderata di grado di digitalizzazione della struttura rispetto ad una baseline)")
    
    a, b = st.columns(2)
    with a:
        st.header("Revenue dai trattamenti ambulatorio")
    with b:
       # Count frequency visite ambulatorio filtered by TYPE
       st.header("Visite ambulatorio per tipologia")
       #fig = go.Figure()
       #fig.add_trace(go.Bar(x=Categ_Visita_Fil, y=df["Categoria_Visita"].value_counts()))
       #b.plotly_chart(fig, use_container_width=True)
    
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Word Cloud Patient Form")
        text = """Healthcare, hospital, sanità, monitoraggio, empatia, relazioni, sanità, pulizia,
                goals, health, sanità pubblica, esperienza, bene, healthcare, sanità, ambiente,
                pulito, sicuro, ospedale, ambulatorio, ambulatorio, healthcare, healthcare, sanità,
                dottori, professionisti, settore in crescita, medicina generale, cardiologia,
                radiologia, sanità, sanitario, health, health"""
        commenttext_merged= df['Comment_Text'].str.cat(sep=',')

        # Create and generate a word cloud image:
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(stopwords=stopwords, background_color="#E4E3E3", width=400, height=400, colormap="Blues").generate(commenttext_merged)

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
    
    st.write(df_selection)
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
