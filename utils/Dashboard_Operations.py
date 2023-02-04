import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

def dashboard_operations():
    
   color1 = "#89CFF0"
   color2 = "#89CFF0"
   
    
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
   data="DatasetOperations_Economics.xlsx"
   df=pd.read_excel(data)
   
   st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
   new_title = '<p style="font-size: 22px;">🔁 Filtra ciò che ti interessa</p>'
   st.sidebar.markdown(new_title, unsafe_allow_html=True)
   st.sidebar.markdown("")
   st.sidebar.multiselect("Categoria Visita", df["Categoria Visita"].unique())
   st.sidebar.multiselect("Sesso Pazienti", df["Sesso"].unique())
   st.sidebar.multiselect("Provenienza", df["Regione Nascita"].unique())
   
   
   st.title("Dashboard MedTech Operations")   
   expander = st.expander("See all records")
   with expander:
     st.write("In questa sezione dovrà esserci la dashbaord con i KPI riferiti all'ambito Operations-Healthcare")

   st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
   
   #lettura dataset column and groupby weekly
   df['Data Visita'] = pd.to_datetime(df['Data Visita'], format="%d/%m/%Y")
   df1= df.groupby(pd.Grouper(key='Data Visita', axis=0,freq='1W')).sum()
   df1.reset_index(inplace=True)

   #filter dataset only to date < to today (dd/mm/YY)
   today = date.today()
   date_oggi = today.strftime("%m/%d/%Y")
   df1 = df1.loc[(df1['Data Visita'] <= date_oggi)]
   
   #ricavo settimana corrente
   ricavo_settimanale = (df1["Prezzo pieno trattamento Paziente"].values[-1:])
   ricavo_settimanale_prec = (df1["Prezzo pieno trattamento Paziente"].values[-2:])
   dicit="Ricavo trattamenti aggiornato al "+date_oggi
   delta_ricav_now_sett_scorsa= ricavo_settimanale - ricavo_settimanale_prec
   delta_ricav_now_sett_scorsa=delta_ricav_now_sett_scorsa[0]
   if delta_ricav_now_sett_scorsa>0:
       delta_ricav_now_sett_scorsa="+"+str(delta_ricav_now_sett_scorsa)+"€"
   else:
       delta_ricav_now_sett_scorsa="-"+str(delta_ricav_now_sett_scorsa)+"€"
   
   df1["linea_sicurezza_prezzo"]=0.65*df1["Prezzo pieno trattamento Paziente"]
   #linea_sicurezza = (df1["linea_sicurezza_prezzo"])
   
   g1, g2, g3 = st.columns(3)
   with g1:
       st.metric(label = dicit , value = str(int(ricavo_settimanale))+" €", delta=delta_ricav_now_sett_scorsa)
   with g2:
       st.metric(label = "Drugs treatment cost", value = ("500.230 €"), delta = ("210€"))
   with g3:
       st.metric(label = "Accessi giornalieri",value = ("221"), delta = ("12"))

   a, b = st.columns(2)
   with a:
     st.header("Outcome/Cost")
     fig = px.bar(df1, x ="Data Visita", y='Prezzo pieno trattamento Paziente', color='Prezzo pieno trattamento Paziente',template = 'ggplot2',width=800, height=400)
     #fig.add_scatter(x ="Data Visita", y=df1["linea_sicurezza_prezzo"], mode='lines', line=dict(color="black"), name='Target')
     fig.update_layout(title_text="Ricavi Settimanali derivanti dalle visite ambulatoriali")
     a.plotly_chart(fig, use_container_width=True)

   with b:
     display_dial("Numero nuovi ingressi", "114", color2)
    
   st.write(df)
   st.write(df1)

