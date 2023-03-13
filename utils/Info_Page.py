#import libraries

import streamlit as st
from PIL import Image

img = Image.open('images/landing_logo1.png')
img2 = Image.open('images/med_bot.png')
image3 = Image.open('images/Mehedi_logo2.png')

def landing_page():
    st.image(img)
    
    if 'count' not in st.session_state:
        st.session_state.count = 0
    
    def increment():
        st.session_state.count += 1
    
    #serve per allargare margini da block-container
    st.markdown("""
    <style>
           .css-k1ih3n {
                padding-top: 0rem;
                padding-bottom: 4rem;
                padding-left: 6em;
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

    new_title = '<b style="font-family:serif; color:#6082B6; font-size: 22px;">Il tool MEDi è un framework di Patient Satisfaction guidato per la compilazione di survey in ambito soddisfazione in ambito Healthcare.</b>'
    st.markdown(new_title, unsafe_allow_html=True)
    
    #SIDEBAR
    st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
    st.sidebar.info(
    """
    Questa è una webapp creata da che consente di valutare la Patient Satisfaction
    
    Web App URL: <https://xxx.streamlitapp.com>
    """
    )

    st.sidebar.title("Support")
    st.sidebar.info(
        """
        Per eventuali problemi nell'utilizzo app rivolgersi a: matteoballabio99@gmail.com
        """
    )
    a, b, c = st.sidebar.columns([0.2,1,0.2])
    with a:
        st.write("")
    with b:
        st.image(image3, width=170)
    with c:
        st.write("")
    
    if st.session_state.count==0:
        a, b = st.columns([7, 1.5])
        with a:
            st.write(
                """
                **Goal Framework:**
                
                The framework ROXi is a web-app for associated Goals and KPI.. There are different steps to
                complete this [**framework**](https://mail.google.com/chat/u/0/):
                """
            )
            st.markdown("- Definizione degli obiettivi progettuali")
            st.markdown("- Associazione tra obiettivi e KPI")
            st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")

            st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:40px;
            }
            </style>
            ''', unsafe_allow_html=True)
        with b:
            st.image(img2,width=250)
        st.button("Go Next ⬇️", key='first', on_click=increment)
        
    if st.session_state.count==1:
        a, b = st.columns([7, 1.5])
        with a:
            st.write(
                """
                **Goal Framework:**
                
                The framework ROXi is a web-app for associated Goals and KPI.. There are different steps to
                complete this [**framework**](https://mail.google.com/chat/u/0/):
                """
            )
            st.markdown("- Definizione degli obiettivi progettuali")
            st.markdown("- Associazione tra obiettivi e KPI")
            st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")

            st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:40px;
            }
            </style>
            ''', unsafe_allow_html=True)
        with b:
            st.image(img2,width=250)
        st.write(
            """**Type of Patient Satisfaction Form:**
            
            The framework ROXi is a web-app for associated Goals and KPI to Pwc's client. There are different steps to
            complete this [**framework**](https://mail.google.com/chat/u/0/):
            """
        )
        st.markdown("- Definizione degli obiettivi progettuali")
        st.markdown("- Associazione tra obiettivi e KPI")
        st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")
        st.button("Go Next ⬇️", key='second', on_click=increment)
    if st.session_state.count==2:
        a, b = st.columns([7, 1.5])
        with a:
            st.write(
                """
                **Goal Framework:**
                
                The framework ROXi is a web-app for associated Goals and KPI.. There are different steps to
                complete this [**framework**](https://mail.google.com/chat/u/0/):
                """
            )
            st.markdown("- Definizione degli obiettivi progettuali")
            st.markdown("- Associazione tra obiettivi e KPI")
            st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")

            st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:40px;
            }
            </style>
            ''', unsafe_allow_html=True)
        with b:
            st.image(img2,width=250)
        st.write(
            """**Type of Patient Satisfaction Form:**
            
            The framework ROXi is a web-app for associated Goals and KPI to Pwc's client. There are different steps to
            complete this [**framework**](https://mail.google.com/chat/u/0/):
            """
        )
        st.markdown("- Definizione degli obiettivi progettuali")
        st.markdown("- Associazione tra obiettivi e KPI")
        st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.write(
            """
            **Metrics of Patient Satisfaction Dashboard:**
            
            The framework ROXi is a web-app for associated Goals and KPI. There are different steps to
            complete this [**framework**](https://mail.google.com/chat/u/0/):
            """
        )
        st.markdown("- Definizione degli obiettivi progettuali")
        st.markdown("- Associazione tra obiettivi e KPI")
        st.markdown("- Clusterizzazione degli obiettivi inseriti in macro-aree e Review finale")
            
