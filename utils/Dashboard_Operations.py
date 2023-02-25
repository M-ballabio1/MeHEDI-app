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
from datetime import timedelta
 

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
   Categ_Visita_Fil=st.sidebar.multiselect("Categoria Visita", df["Categoria_Visita"].unique(), default=["CARDIOLOGIA","RADIOLOGIA","IMMUNOLOGIA"])
   Sesso_Fil=st.sidebar.multiselect("Sesso Pazienti", df["Sesso"].unique())
   Proveni_Fil=st.sidebar.multiselect("Provenienza", df["RegioneResidenza"].unique())
   
   dfs = {Categ_Visita_Fi: df[df["Categoria_Visita"] == Categ_Visita_Fi] for Categ_Visita_Fi in Categ_Visita_Fil}
   #df_selection = df.query(
   #     "Categoria_Visita == @Categ_Visita_Fil & Sesso == @Sesso_Fil & RegioneResidenza == @Proveni_Fil"
   # )
   
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
   # Yesterday date
   yesterday = today - timedelta(days = 1)
   date_oggi = today.strftime("%m/%d/%Y")
   date_yesterday = yesterday.strftime("%m/%d/%Y")
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
       delta_ricav_now_sett_scorsa=str(delta_ricav_now_sett_scorsa)+"€"
   
   #media mobile e target
   df1["MA_sicurezza_prezzo"]=df1["Prezzo pieno trattamento Paziente"].rolling(2).mean()
   df1["target_sicurezza_prezzo"]=1500
   
   #numero accesso giornaliero oggi e ieri
   df2= df["Data Visita"].value_counts()
   dt_oggi=df2.loc[date_oggi][0]
   dt_ieri=df2.loc[date_yesterday][0]
   if dt_oggi < dt_ieri:
       dt_ieri="-"+str(dt_ieri)
   else:
       dt_ieri="+"+str(dt_ieri)
       
   g1, g2, g3 = st.columns(3)
   with g1:
       st.metric(label = dicit , value = str(int(ricavo_settimanale))+" €", delta=delta_ricav_now_sett_scorsa)
   with g2:
       st.metric(label = "Accesso giornaliero ambulatorio", value = dt_oggi, delta = dt_ieri)
   with g3:
       st.metric(label = "Accessi giornalieri",value = ("221"), delta = ("12"))

   a, b = st.columns(2)
   with a:
     # Ricavi dai trattamenti ambulatoriali nel tempo
     st.header("Revenue dai trattamenti ambulatorio")
     fig = px.bar(df1, x ="Data Visita", y='Prezzo pieno trattamento Paziente', color='Prezzo pieno trattamento Paziente',template = 'ggplot2',width=800, height=400)
     fig.add_trace(go.Scatter(x=df1['Data Visita'], y=df1["MA_sicurezza_prezzo"],mode='lines', line=dict(color="orange"), name='Media Mobile a 2 week'))
     fig.add_trace(go.Scatter(x=df1['Data Visita'], y=df1["target_sicurezza_prezzo"],mode='lines', line=dict(color="blue"), name='Safety Target'))
     fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
     #fig.update_layout(title_text="Ricavi Settimanali derivanti dalle visite ambulatoriali")
     a.plotly_chart(fig, use_container_width=True)

   with b:
       # Count frequency visite ambulatorio filtered by TYPE
       st.header("Visite ambulatorio per tipologia")
       fig = go.Figure()
       fig.add_trace(go.Bar(x=Categ_Visita_Fil, y=df["Categoria_Visita"].value_counts()))
       b.plotly_chart(fig, use_container_width=True)

   st.write(df)
   st.write(df1)
   st.write(df2)
