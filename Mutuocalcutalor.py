import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# liste e/o costanti


#####################
# MENU IMPOSTAZIONI #
#####################

with st.sidebar:
    st.header("Impostazioni")
    prestito = st.number_input("Prestito [€]", value = 100000, step = 10000, help = f"Inserisci l'importo desiderto del prestito")
    anni     = st.number_input("Anni [-]", value = 20, step = 5, help = f"Inserisci il numero di anni dell'ammortamento del mutuo")
    int_anno = st.number_input("Tasso d'interesse annuo [%]", value = 3.0, step = 0.1, help = f"Inserisci il valore del tasso fisso annuo")
    st.markdown("---")
    st.caption("Mutuocalculator ver. 1.0")
    st.markdown('<p style="font-size: 8px; color: gray;">Sviluppato da Stefano Antonini',unsafe_allow_html=True)


############
# CALCOLI #
############

i        = int_anno/100/12
n        = anni*12
rata     = prestito*(i*(1+i)**n)/((1+i)**n-1)
totale   = rata*n
int_tot  = totale - prestito
int_perc = (int_tot / prestito)*100
    
cap_res = prestito
int_res = int_tot
tot_cap = 0
tot_int = 0
anno = 1
mese = 1
data = []

for a in range(0,anni):
    for m in range (1,13):
        k = a*12+m
        int = i*cap_res
        cap = rata-int
        cap_res = cap_res - cap
        int_res = int_res - int
        tot_cap = tot_cap + cap
        tot_int = tot_int + int
        tot     = tot_cap + tot_int
        data.append({
    "Anno": a+1,
    "Mese": m,
    "Rata": rata,
    "Quota Capitale Rata": cap,
    "Quota Interesse Rata": int,
    "Capitale Residuo": cap_res,
    "Interesse Residuo": int_res,
    "Totale Capitale Versato": tot_cap,
    "Totale Interesse Versato": tot_int,
    "Totale Versato": tot,
    })

df = pd.DataFrame(data) 

df_anno = df.drop(columns=['Mese','Totale Capitale Versato','Totale Interesse Versato']).groupby('Anno').agg({
    'Rata': 'sum',
    'Quota Capitale Rata': 'sum',
    'Quota Interesse Rata': 'sum',
    'Capitale Residuo': 'last',
    'Interesse Residuo': 'last',
    'Totale Versato': 'last'}).reset_index()
df_anno['Detrazioni'] = np.where(
    df_anno['Quota Interesse Rata'] < 4000,          # Condizione
    df_anno['Quota Interesse Rata'] * 0.19,          # Valore se Vero
    760                              # Valore se Falso (4000 * 0.19 = 760)
)

tot_detr = df_anno['Detrazioni'].sum()




#####################
# PAGINA PRINCIPALE #
#####################

st.subheader("Calcolo Ammortamento Mutuo")
st.divider()

st.write(f"Rata Mutuo: {rata:,.2f} €")
st.write(f"Totale Mutuo: {totale:,.2f} €")
st.write(f"Interesse totale: {int_tot:,.2f} €")
st.write(f"Interesse percentuale: {int_perc:.2f} %")
st.divider()
st.write(f"Totale detrazioni: {tot_detr:,.2f} €")
st.write(f"Totale Mutuo con detrazioni: {(totale-tot_detr):,.2f} €")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Dettaglio Mensile Rate",  "📊 Dettaglio Annuale Rate", "📈 Grafico Rate"])

###########
# TABELLA #
###########

with tab1:
    st.write(f"Dettagli Mutuo")
    df_tab = df.copy()
    colonne_euro = df_tab.columns[2:]
    for col in colonne_euro:
        df_tab[col] = df_tab[col].map('€ {:,.2f}'.format)
    st.dataframe(df_tab, width='stretch', hide_index=True)

with tab2:
    st.write(f"Dettagli Mutuo")
    df_anno_tab = df_anno.copy()
    colonne_anno_euro = df_anno_tab.columns[1:]
    for col in colonne_anno_euro:
        df_anno_tab[col] = df_anno_tab[col].map('€ {:,.2f}'.format)
    st.dataframe(df_anno_tab, width='stretch', hide_index=True)

###########
# GRAFICO #
###########

with tab3:
    df = df.apply(pd.to_numeric)
    df['Data'] = (df['Anno']-1) * 12 + df['Mese']
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
    x=df['Data'],
    y=df['Quota Capitale Rata'],
    name='Quota Capitale Rata',
    marker_color='royalblue'
    ))

    fig.add_trace(go.Bar(
    x=df['Data'],
    y=df['Quota Interesse Rata'],
    name='Quota Interesse Rata',
    marker_color='firebrick'
    ))

    fig.update_layout(
    title='Quota Rata: Capitale vs Interessi',
    xaxis_title='Mese',
    yaxis_title='€',
    barmode='stack',
    template='plotly_white',
    hovermode='x unified',
    )

    st.plotly_chart(fig,use_container_width=True)