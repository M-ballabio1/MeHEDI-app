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
                padding-right: 10rem;
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

    new_title = '<b style="font-family:serif; color:#6082B6; font-size: 26px;">Il tool MEDi è un framework di Patient Satisfaction guidato per la compilazione di survey in ambito soddisfazione in ambito Healthcare.</b>'
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
            new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Summary Proof of Concept MEHEDI:</b>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write(
                """
                
                The last decade has seen an exponential growth of data in every sector due to improved sensing technologies.
                Among these sectors we consider for this **POC the Healthcare sector**. Despite the strong growth from the technical point
                of view of storing these data, there has not always been optimal interpretation and management of the available data.
                
                **What is the status of the digital transformation of Italian healthcare?**
                
                Saleforce Italia conducted a survey of a sample of 84 healthcare organizations including AOs, IRCSSs, Nursing Homes and Diagnostic Centers.
                For 56% of the Italian healthcare organizations surveyed, there is still no formal strategic planning for digital innovation. For **37%, on the other hand, digitization
                strategy is limited to individual processes**, while **7% consider digital strategy as an integral part of business strategy** to innovate patient care models.
                
                If you want to read the full document (POC) you can click on this [**link**](https://docs.google.com/document/d/1qZtcUX0fqJVSSDIQqjuxeVHOiQLSsaUabji72NJYdMM/edit#), otherwise if you prefer to see to our 
                solution click the Go Next button.
                Instead, if you want to see the raw dataset, you can click here [**link dataset**](https://docs.google.com/spreadsheets/d/1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8/edit#gid=0).
                """
            )
            st.markdown("""
            <div align=right><small>
            Page views interaction: <img src="https://www.cutercounter.com/hits.php?id=hxndpfn&nd=6&style=52" border="0" alt="hit counter"><br>
            GitHub <a href="https://github.com/M-ballabio1/MeHEDI-app"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/M-ballabio1/MeHEDI-app?style=social"></a>
            </small></div>
            """, unsafe_allow_html=True)
        with b:
            st.image(img2,width=300)
        st.button("Go Next ⬇️", key='first', on_click=increment)
        
    if st.session_state.count==1:
        a, b = st.columns([7, 1.5])
        with a:
            new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Summary Proof of Concept MEHEDI:</b>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write(
                """
                
                The last decade has seen an exponential growth of data in every sector due to improved sensing technologies.
                Among these sectors we consider for this **POC the Healthcare sector**. Despite the strong growth from the technical point
                of view of storing these data, there has not always been optimal interpretation and management of the available data.
                
                **What is the status of the digital transformation of Italian healthcare?**
                
                Saleforce Italia conducted a survey of a sample of 84 healthcare organizations including AOs, IRCSSs, Nursing Homes and Diagnostic Centers.
                For 56% of the Italian healthcare organizations surveyed, there is still no formal strategic planning for digital innovation. For **37%, on the other hand, digitization
                strategy is limited to individual processes**, while **7% consider digital strategy as an integral part of business strategy** to innovate patient care models.
                
                If you want to read the full document (POC) you can click on this [**link**](https://docs.google.com/document/d/1qZtcUX0fqJVSSDIQqjuxeVHOiQLSsaUabji72NJYdMM/edit#), otherwise if you prefer to see to our 
                solution click the Go Next button.
                Instead, if you want to see the raw dataset, you can click here [**link dataset**](https://docs.google.com/spreadsheets/d/1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8/edit#gid=0).
                """
            )
            st.markdown("""
            <div align=right><small>
            Page views interaction: <img src="https://www.cutercounter.com/hits.php?id=hxndpfn&nd=6&style=52" border="0" alt="hit counter"><br>
            GitHub <a href="https://github.com/M-ballabio1/MeHEDI-app"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/M-ballabio1/MeHEDI-app?style=social"></a>
            </small></div>
            """, unsafe_allow_html=True)
        with b:
            st.image(img2,width=300)
        new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Our MEHEDI\'s Solution:</b>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(
            """Hospital management and practitioners need to be able to evaluate real-time the evolution of metrics related to different business areas.
                This aspect of Digital Transformation as far as especially small centers are concerned is underestimated, done crudely through monthly reports (single photographs), or even not even considered.
            """
        )
        st.markdown("- **1: Creating a structured (data-driven) dialogue relationship with patients/customers (Patient satisfaction)**")
        st.markdown("- **2: Processing insights on such data in a real-time manner (Integration and Continuous monitoring)**")
        st.markdown("- **3: Providing strategic directions to the facility (Monitoring and Innovation), enables immediate assessment of business problems and opportunities for growth**")
        
        new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Project Goal:</b>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(
            """The goal of the project is to create a web-application for the integration of data derived from Patients through ad-hoc developed questionnaires (PREM)
                with the facility's operational and economic management metrics to set up a 360-degree data-driven improvement strategy. The goal of the project is the creation of web-application 
                for management and monitoring uses from a business management perspective concerning 3 spheres:
            """)
        
        st.markdown("- **Patient Satisfaction** --> Finish ✅")
        st.markdown("- **Operations** --> Progress 🔄")
        st.markdown("- **Economics** (economics-billing) --> Progress 🔄")
        
        st.write(
            """The application allows through the use of an access managed by authentication to collect feedback from the patient regarding patient satisfaction
                and on the other hand, the possibility to evaluate and analyze the results derived from different strategic business areas.""")
    
        st.button("Go Next ⬇️", key='second', on_click=increment)
    if st.session_state.count==2:
        a, b = st.columns([7, 1.5])
        with a:
            new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Summary Proof of Concept MEHEDI:</b>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write(
                """
                
                The last decade has seen an exponential growth of data in every sector due to improved sensing technologies.
                Among these sectors we consider for this **POC the Healthcare sector**. Despite the strong growth from the technical point
                of view of storing these data, there has not always been optimal interpretation and management of the available data.
                
                **What is the status of the digital transformation of Italian healthcare?**
                
                Saleforce Italia conducted a survey of a sample of 84 healthcare organizations including AOs, IRCSSs, Nursing Homes and Diagnostic Centers.
                For 56% of the Italian healthcare organizations surveyed, there is still no formal strategic planning for digital innovation. For **37%, on the other hand, digitization
                strategy is limited to individual processes**, while **7% consider digital strategy as an integral part of business strategy** to innovate patient care models.
                
                If you want to read the full document (POC) you can click on this [**link**](https://docs.google.com/document/d/1qZtcUX0fqJVSSDIQqjuxeVHOiQLSsaUabji72NJYdMM/edit#), otherwise if you prefer to see to our 
                solution click the Go Next button.
                Instead, if you want to see the raw dataset, you can click here [**link dataset**](https://docs.google.com/spreadsheets/d/1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8/edit#gid=0).
                """
            )
            st.markdown("""
            <div align=right><small>
            Page views interaction: <img src="https://www.cutercounter.com/hits.php?id=hxndpfn&nd=6&style=52" border="0" alt="hit counter"><br>
            GitHub <a href="https://github.com/M-ballabio1/MeHEDI-app"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/M-ballabio1/MeHEDI-app?style=social"></a>
            </small></div>
            """, unsafe_allow_html=True)
        with b:
            st.image(img2,width=300)
        new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Our MEHEDI\'s Solution:</b>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(
            """Hospital management and practitioners need to be able to evaluate real-time the evolution of metrics related to different business areas.
                This aspect of Digital Transformation as far as especially small centers are concerned is underestimated, done crudely through monthly reports (single photographs), or even not even considered.
            """
        )
        st.markdown("- **1: Creating a structured (data-driven) dialogue relationship with patients/customers (Patient satisfaction)**")
        st.markdown("- **2: Processing insights on such data in a real-time manner (Integration and Continuous monitoring)**")
        st.markdown("- **3: Providing strategic directions to the facility (Monitoring and Innovation), enables immediate assessment of business problems and opportunities for growth**")
        
        new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Project Goal:</b>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.write(
            """The goal of the project is to create a web-application for the integration of data derived from Patients through ad-hoc developed questionnaires (PREM)
                with the facility's operational and economic management metrics to set up a 360-degree data-driven improvement strategy. The goal of the project is the creation of web-application 
                for management and monitoring uses from a business management perspective concerning 3 spheres:
            """)
        
        st.markdown("- **Patient Satisfaction** --> Finish ✅")
        st.markdown("- **Operations** --> Progress 🔄")
        st.markdown("- **Economics** (economics-billing) --> Progress 🔄")
        
        st.write(
            """The application allows through the use of an access managed by authentication to collect feedback from the patient regarding patient satisfaction
                and on the other hand, the possibility to evaluate and analyze the results derived from different strategic business areas.""")
        
        new_title = '<b style="font-family:serif; color:#000000; font-size: 22px;">Team of project:</b>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown("- Matteo Ballabio, Biomedical and Management Engineer, PwC consultant ")
        st.markdown("- Luca Alessandro Cappellini, Medical Doctor, Radiology Resident, MBA fellow ")
        st.markdown("- Federico Facoetti, Engineering and management for health ")
            
