import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from openpyxl import Workbook
from io import BytesIO
 


def dashboard_operations(): 
   
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
    
    st.title("Dashboard MedTech Operations")
    
    df_data = pd.read_excel("DatasetOperations_Economics.xlsx")
    
    df_data.groupby(['Data Visita']).size()
    st.write(df_data[0])
    
    expander = st.expander("See all records")
    with expander:
        st.write("In questa sezione dovrà esserci la dashbaord con i KPI riferiti all'ambito Operations-Healthcare")
    
    st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
    
    g1, g2, g3 = st.columns(3)
    g1.metric(label = "Safety", value = ("96 %"),)
    g2.metric(label = "Drugs treatment cost",
    value = ("500.230 €"),
    delta = ("210€"))
    g3.metric(label = "Accessi giornalieri",
    value = ("150"),
    delta = ("12"))
    
    color1 = "#89CFF0"
    color2 = "#89CFF0"

    a, b = st.columns(2)
    with a:
        display_dial("Tempo d'attesa", "26 min", color1)
    with b:
        display_dial("Numero nuovi ingressi", "114", color2)
    
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Operations")
        st.image("https://www.solverglobal.com/wp-content/uploads/2020/09/PowerBI_Dashboard_04-1.jpg")
    with col2:
        st.header("Outcome/Cost")
        st.image("https://cdn.sisense.com/wp-content/uploads/Hospital-performance.png")
