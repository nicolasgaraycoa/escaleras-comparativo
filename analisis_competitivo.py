import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px



st.set_page_config(page_title="Analisis competitivo", layout="wide")

st.title('Analisis competitivo')

precios = pd.read_excel('precios.xlsx')

with st.sidebar:
    pais = st.multiselect('Pais: ', list(precios.pais.unique()))
    tipo = st.multiselect('Tipo de alcohol: ', list(precios.tipo.unique()))
    tier = st.slider('Price tiers (n): ', min_value =2, max_value=5,
                     value = 3, step=1)
    

precios = precios[precios['pais'].str.contains('|'.join(map(str, pais)))]
precios = precios[precios['tipo'].str.contains('|'.join(map(str, tipo)))]
bin_labels = ["A","B","C","D","E"][1:(tier-1)]
precios['ptier'] = pd.qcut(precios['precio'], q=tier, 
                                labels=["A","B","C","D","E"][:tier])


fig = px.box(precios, y="precio", x="ptier", color="marca", hover_data=precios.columns)

fig.update_xaxes(categoryorder='total ascending')


st.plotly_chart(fig, theme="streamlit", use_container_width=True)
