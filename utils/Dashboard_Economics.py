import google_auth_httplib2
import httplib2
import pandas as pd
import datetime
import streamlit as st

#from Patient_Form import form_pazienti

def dashboard_economics():
    
    st.title("Dashboard MedTech Economics")
    st.markdown("""**Questa sezione mostra i risultati dell'analisi utilizzando i dati delle operations di MeHedi""")
        
    g1, g2, g3 = st.columns(2)
    g1.metric(label = "Fatturato mensile", value = ("505.000€"), delta = ("20.000€"))
    g2.st_radial('Metric 1', value=88)
    g3.metric(label = "Costi menisili",
    value = ("202.300 €"),
    delta = ("10.000€"))

    col1, col2 = st.columns(2)

    with col1:
        st.header("Economics")
        st.image("https://www.slideteam.net/media/catalog/product/cache/1280x720/d/a/dashboard_depicting_hospital_kpi_with_treatment_costs_slide01.jpg")

    with col2:
        st.header("Health data")
        st.image("https://www.datapine.com/images/hospital-kpi-dashboard.png")
