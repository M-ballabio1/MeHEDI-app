import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import altair as alt
from Patient_Form import df, get_data

st.title("Sezione Personale Sanitario")

# --- USER AUTHENTICATION ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("Click enter to log")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("Click enter to log")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct
        return True

if check_password(): 
    st.markdown("Sezione dedicata agli specialisti di medicina generale per visionare andamento Poliambulatorio")
    st.dataframe(get_data(df))
   
    c = alt.Chart(df).mark_circle().encode(
            x='Sesso', y='Sicurezza',)
    st.altair_chart(c, use_container_width=True)
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
         
    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")
