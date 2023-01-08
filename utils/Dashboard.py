import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import altair as alt
#from Patient_Form import df, get_data

def dashboard_patient_satisf():
    st.title("Sezione Personale Sanitario")
    st.markdown("Sezione dedicata agli specialisti di medicina generale per visionare andamento Poliambulatorio")
    #st.dataframe(get_data(df))

    #df1=pd.DataFrame(df)

    #c = alt.Chart(df1).mark_circle().encode(
    #        x='Sesso', y='Sicurezza',)
    #st.altair_chart(c, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Patient satisfaction")
        st.image("https://www.datapine.com/images/patient-satisfaction-dashboard.png")

    with col2:
        st.header("Health data")
        st.image("https://www.datapine.com/images/hospital-kpi-dashboard.png")
