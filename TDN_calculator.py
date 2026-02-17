import streamlit as st
import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# liste e/o costanti

lista_fluidi = ["Water","Ammonia","CarbonDioxide","Methane","Nitrogen","Oxygen"]
lista_calcoli = ["Saturazione (p)","Saturazione (T)",
                 "Bifase (p,Xv)",
                 "Vapore SH o Liquido SC (p,T)","Vapore SH o Liquido SC (p,h)"]

#####################
# MENU IMPOSTAZIONI #
#####################

with st.sidebar:
    st.header("Impostazioni")
    fluido = st.sidebar.selectbox("Seleziona il Fluido", lista_fluidi)
    T_min  = CP.PropsSI('Tmin',fluido)-273.15 #[°C]
    T_cr   = CP.PropsSI('Tcrit',fluido)-273.15 #[°C]
    P_min  = CP.PropsSI('P', 'T', T_min+273.15, 'Q', 0, fluido)*10**-5 #[bara]
    P_cr   = CP.PropsSI('P', 'T', T_cr+273.15, 'Q', 0, fluido)*10**-5 #[bara]
    st.divider()
    calcolo = st.sidebar.selectbox("Modalità di calcolo", lista_calcoli)
    st.divider()


    if calcolo == "Saturazione (p)":
        P  = st.number_input("P sat [bara]", value = float(round(P_min+1.0)),step=1.0,help=f"Inserisci un valore tra {P_min:.2f}bara e {P_cr:.2f}bara") #[bara]
        T  = CP.PropsSI('T', 'P', P*10**5, 'Q', 0, fluido)-273.15 #[°C]
        DL = CP.PropsSI("D","P",P*10**5,"Q",0,fluido)
        DV = CP.PropsSI("D","P",P*10**5,"Q",1,fluido)
        VL = 1/DL
        VV = 1/DV
        HL = CP.PropsSI("H","P",P*10**5,"Q",0,fluido)/1000
        HV = CP.PropsSI("H","P",P*10**5,"Q",1,fluido)/1000
        DH = HV-HL
        SL = CP.PropsSI("S","P",P*10**5,"Q",0,fluido)/1000
        SV = CP.PropsSI("S","P",P*10**5,"Q",1,fluido)/1000
        DS = SV-SL
        output = {
        "Parametro": ["Pressione saturazione", "Temperatura saturazione", "Densità liquido saturo", "Densità vapore saturo","Volume sp. liquido saturo","Volume sp. vapore saturo","Entalpia liquido saturo","Entalpia vapore saturo","Delta Entalpia VS-LS","Entropia liquido saturo","Entropia vapore saturo","Delta entropia VS-LS"],
        "Valore": [P,T,DL,DV,VL,VV,HL,HV,DH,SL,SV,DS],
        "Unità di misura": ["bara","°C","kg/m³","kg/m³", "m³/kg","m³/kg", "kJ/kg","kJ/kg","kJ/kg","kJ/kg·K","kJ/kg·K","kJ/kg·K"],
        }
        df = pd.DataFrame(output)


    elif calcolo == "Saturazione (T)":
        T = st.number_input("T sat [°C]", value = float(round(T_min+30.0)),step=1.0,help=f"Inserisci un valore tra {T_min:.2f}°C e {T_cr:.2f}°C") #[°C]
        P = CP.PropsSI('P', 'T', T+273.15, 'Q', 0, fluido)*10**-5 #[bara]
        DL = CP.PropsSI("D","P",P*10**5,"Q",0,fluido)
        DV = CP.PropsSI("D","P",P*10**5,"Q",1,fluido)
        VL = 1/DL
        VV = 1/DV
        HL = CP.PropsSI("H","P",P*10**5,"Q",0,fluido)/1000
        HV = CP.PropsSI("H","P",P*10**5,"Q",1,fluido)/1000
        DH = HV-HL
        SL = CP.PropsSI("S","P",P*10**5,"Q",0,fluido)/1000
        SV = CP.PropsSI("S","P",P*10**5,"Q",1,fluido)/1000
        DS = SV-SL
        output = {
        "Parametro": ["Pressione saturazione", "Temperatura saturazione", "Densità liquido saturo", "Densità vapore saturo","Volume sp. liquido saturo","Volume sp. vapore saturo","Entalpia liquido saturo","Entalpia vapore saturo","Delta Entalpia VS-LS","Entropia liquido saturo","Entropia vapore saturo","Delta entropia VS-LS"],
        "Valore": [P,T,DL,DV,VL,VV,HL,HV,DH,SL,SV,DS],
        "Unità di misura": ["bara","°C","kg/m³","kg/m³", "m³/kg","m³/kg", "kJ/kg","kJ/kg","kJ/kg","kJ/kg·K","kJ/kg·K","kJ/kg·K"],
        }
        df = pd.DataFrame(output)


    elif calcolo == "Bifase (p,Xv)":
        P  = st.number_input("P sat [bara]", value = float(round(P_min+1.0)),step=1.0,help=f"Inserisci un valore tra {P_min:.2f}bara e {P_cr:.2f}bara") #[bara]
        XV = st.number_input("Titolo vapore [-]", value = 0.5,step=0.1,help=f"Inserisci un valore tra 0 e 1 ")
        T  = CP.PropsSI('T', 'P', P*10**5, 'Q', 0, fluido)-273.15 #[°C]
        DL = CP.PropsSI("D","P",P*10**5,"Q",0,fluido)
        DV = CP.PropsSI("D","P",P*10**5,"Q",1,fluido)
        D  = CP.PropsSI("D","P",P*10**5,"Q",XV,fluido)
        VL = 1/DL
        VV = 1/DV
        V  = 1/D
        HL = CP.PropsSI("H","P",P*10**5,"Q",0,fluido)/1000
        HV = CP.PropsSI("H","P",P*10**5,"Q",1,fluido)/1000
        H  = CP.PropsSI("H","P",P*10**5,"Q",XV,fluido)/1000
        DH = HV-HL
        SL = CP.PropsSI("S","P",P*10**5,"Q",0,fluido)/1000
        SV = CP.PropsSI("S","P",P*10**5,"Q",1,fluido)/1000
        S  = CP.PropsSI("S","P",P*10**5,"Q",XV,fluido)/1000
        DS = SV-SL
        output = {
        "Parametro": ["Pressione saturazione", "Temperatura saturazione", "Densità liquido saturo", "Densità vapore saturo", "Densità miscela bifase","Volume sp. liquido saturo","Volume sp. vapore saturo","Volume sp. miscela bifase","Entalpia liquido saturo","Entalpia vapore saturo","Entalpia miscela bifase","Delta Entalpia VS-LS","Entropia liquido saturo","Entropia vapore saturo","Entropia miscela bifase","Delta entropia VS-LS"],
        "Valore": [P,T,DL,DV,D,VL,VV,V,HL,HV,H,DH,SL,SV,S,DS],
        "Unità di misura": ["bara","°C","kg/m³","kg/m³","kg/m³", "m³/kg","m³/kg","m³/kg","kJ/kg","kJ/kg","kJ/kg","kJ/kg","kJ/kg·K","kJ/kg·K","kJ/kg·K","kJ/kg·K"],
        }
        df = pd.DataFrame(output)


    elif calcolo == "Vapore SH o Liquido SC (p,T)":
        P  = st.number_input("P [bara]", value = P_min, step=1.0) #[bara]
        T  = st.number_input("T [°C]", value = T_cr, step=1.0) #[°C]
        D  = CP.PropsSI("D","P",P*10**5,"T",T+273.15,fluido)
        V  = 1/D
        H  = CP.PropsSI("H","P",P*10**5,"T",T+273.15,fluido)/1000
        S  = CP.PropsSI("S","P",P*10**5,"T",T+273.15,fluido)/1000
        output = {
        "Parametro": ["Pressione", "Temperatura", "Densità","Volume specifico","Entalpia","Entropia"],
        "Valore": [P,T,D,V,H,S],
        "Unità di misura": ["bara","°C","kg/m³","m³/kg","kJ/kg","kJ/kg·K"],
        }
        df = pd.DataFrame(output)  


    elif calcolo == "Vapore SH o Liquido SC (p,h)":
        P  = st.number_input("P [bara]", value = P_min, step=1.0) #[bara]
        H_default = CP.PropsSI("H","P",P*10**5,"T",T_cr+273.15,fluido)/1000
        H  = st.number_input("H [kJ/kg]", value = H_default, step=1.0) #[kJ/kg]
        T  = CP.PropsSI("T","P",P*10**5,"H",H*1000,fluido)-273.15
        D  = CP.PropsSI("D","P",P*10**5,"T",T+273.15,fluido)
        V  = 1/D
        S  = CP.PropsSI("S","P",P*10**5,"T",T+273.15,fluido)/1000
        output = {
        "Parametro": ["Pressione", "Temperatura", "Densità","Volume specifico","Entalpia","Entropia"],
        "Valore": [P,T,D,V,H,S],
        "Unità di misura": ["bara","°C","kg/m³","m³/kg","kJ/kg","kJ/kg·K"],
        }
        df = pd.DataFrame(output) 


    st.markdown("---")
    st.caption("TDN calculator ver. 1.0")
    st.markdown('<p style="font-size: 8px; color: gray;">Basato sulla libreria di <a href="http://www.coolprop.org" style="color: lightgray;">CoolProp</a> </p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: gray;">Sviluppato da Stefano Antonini',unsafe_allow_html=True)

#####################
# PAGINA PRINCIPALE #
#####################

st.subheader("🔥 Calcolo delle Proprietà Termodinamiche 🔥")
st.divider()

st.write(f"Fluido selezionato: {fluido}")
st.write(f"Calcolo selezionato: {calcolo}")
st.divider()

tab1, tab2 = st.tabs(["📊 Dati", "📈 Diagramma T-s"])

###########
# TABELLA #
###########

with tab1:
    st.write(f"Dettagli calcolo {calcolo}")

    if calcolo == "Saturazione (p)":
        st.dataframe(df, width='stretch', hide_index=True)

    elif calcolo == "Saturazione (T)":
        st.dataframe(df, width='stretch', hide_index=True)

    elif calcolo == "Bifase (p,Xv)":
        st.dataframe(df, width='stretch', hide_index=True)

    elif calcolo == "Vapore SH o Liquido SC (p,T)":
        st.dataframe(df, width='stretch', hide_index=True)

    elif calcolo == "Vapore SH o Liquido SC (p,h)":
        st.dataframe(df, width='stretch', hide_index=True)

###########
# GRAFICO #
###########

with tab2:
    T_min  = CP.PropsSI('Tmin',fluido)-273.15 #[°C]
    T_cr   = CP.PropsSI('Tcrit',fluido)-273.15 #[°C]
    T_sat  = np.linspace(T_min,T_cr,100)
    SL_sat = CP.PropsSI("S","T",T_sat+273.15,"Q",0,fluido)/1000
    SV_sat = CP.PropsSI("S","T",T_sat+273.15,"Q",1,fluido)/1000

    fig = make_subplots(rows = 1,cols = 1)
    fig.add_trace(go.Scatter(x= SL_sat, y = T_sat, mode = 'lines', line_color = 'black', hoverinfo  = 'x+y'), row = 1, col = 1)
    fig.add_trace(go.Scatter(x= SV_sat, y = T_sat, mode = 'lines', line_color = 'black', hoverinfo  = 'x+y'), row = 1, col = 1)

    if calcolo == "Saturazione (p)" or calcolo == "Saturazione (T)":
        fig.add_trace(go.Scatter(x= [SL,SV], y = [T,T], mode = 'lines', line_color = 'tomato', hoverinfo  = 'x+y'), row = 1, col = 1)

    if calcolo == "Bifase (p,Xv)":
        fig.add_trace(go.Scatter(x= [SL,SV], y = [T,T], mode = 'lines', line_color = 'tomato', hoverinfo  = 'x+y'), row = 1, col = 1)
        fig.add_trace(go.Scatter(x= [S], y = [T], mode = 'markers',marker_color = 'tomato',marker_size=10, hoverinfo  = 'x+y'), row = 1, col = 1)

    if calcolo == "Vapore SH o Liquido SC (p,T)" or calcolo == "Vapore SH o Liquido SC (p,h)":
        fig.add_trace(go.Scatter(x= [S], y = [T], mode = 'markers',marker_color = 'tomato',marker_size=10, hoverinfo  = 'x+y'), row = 1, col = 1)

    fig.update_layout(
        xaxis_title = "Entropia specifica [kJ/kgK]",
        yaxis_title = "Temperatura [°C]",
        showlegend = False,
        template="simple_white")

    st.plotly_chart(fig,use_container_width=True)
