import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
import gspread as gs

def dashboard_operations():
   SCOPE = "https://www.googleapis.com/auth/spreadsheets"
   SPREADSHEET_ID = "1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8"
   SHEET_NAME = "Database_Operations"
   GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
   
   sh = gs.open_by_url(GSHEET_URL)
   ws = sh.worksheet('Database_Operations')
   
   df = pd.DataFrame(ws.get_all_records())
   df.head()
   st.dataframe(df)
   
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
   df_new=connect_to_gsheet
   
   df_new=pd.DataFrame(df_new)
   
   prova=len(df_new)

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
   value = prova,
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
