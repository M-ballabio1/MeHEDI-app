import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import altair as alt
#from Patient_Form import df, get_data


def dashboard_patient_satisf():
    st.title("Dashboard Patient Satisfaction")
    st.markdown("Sezione dedicata agli specialisti di medicina generale per visionare andamento Poliambulatorio")
    #st.dataframe(get_data(df))

    #df1=pd.DataFrame(df)

    #c = alt.Chart(df1).mark_circle().encode(
    #        x='Sesso', y='Sicurezza',)
    #st.altair_chart(c, use_container_width=True)
    
    #with open('ui/style.css')as f:
    #   st.markdown("<style>{f.read()}</style>", unsafe_allow_html = True)
    
    g1, g2, g3 = st.columns(3)
    g1.metric(label = "Patient Experience", value = ("91 %"),)
    g2.metric(label = "Safety Medical Center",
    value = ("88%"),
    delta = ("+6%"))
    g3.metric(label = "Empatia personale",
    value = ("76%"),
    delta = ("-5%"))

    col1, col2 = st.columns(2)

    with col1:
        st.header("Patient satisfaction")
        st.image("https://www.healthcareitnews.com/sites/hitn/files/Stanford%20dashboard-HITN.png")

    with col2:
        st.header("Health data")
        st.image("https://www.slideteam.net/media/catalog/product/cache/1280x720/p/a/patient_satisfaction_measurement_dashboard_service_ppt_show_vector_slide01.jpg")
