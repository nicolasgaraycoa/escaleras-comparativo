import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import statistics



st.set_page_config(page_title="Analisis competitivo", layout="wide")

st.subheader('Analisis competitivo')

precios = pd.read_excel('precios.xlsx')

with st.sidebar:
    pais = st.multiselect('Pais: ', list(precios.pais.unique()))
    sku_ref = st.selectbox("SKU referencial: ", 
                           list(precios['sku'].unique()))
    marca = st.multiselect('Marcas: ', list(precios.marca.unique()))
    

precios = precios[precios['pais'].str.contains('|'.join(map(str, pais)))]

comp = precios[['marca','sku', 'precio', 'ml']]
comp['precio'] = (statistics.mode(comp['ml'])/comp['ml'])*comp['precio']
comp.drop(columns=['ml'], inplace=True)
psku_ref = precios['precio'][precios['sku']==sku_ref].mean()
comp['pref'] = (comp['precio']/psku_ref)*100

comp.drop(columns=['precio'], inplace=True)
comp = comp.groupby(by=['marca','sku'], as_index=False).agg({'pref':['mean','std']})
comp.columns = ['marca','sku', 'pref_mean', 'pref_std']
comp['pref_mean'] = round(comp['pref_mean'],0)
comp['pref_std'] = round(comp['pref_std'],0)
comp = comp.fillna(value=1)

comp = comp[comp['marca'].str.contains('|'.join(map(str, marca)))]
tier = min(5, comp.shape[0])
comp['ptier'] = pd.qcut(comp['pref_mean'], q=tier, 
                                labels=["A","B","C","D","E"][:tier])

fig = px.scatter(comp, x="ptier", y="pref_mean", color="sku", opacity=0.6,
                 title="Escaleras de precios x marca x sku")
fig.update_traces(marker=dict(size=22))
fig.add_hline(y=100, line_dash="dash", opacity=0.3)
fig.update_xaxes(categoryorder='array', categoryarray=["A","B","C","D","E"][:tier])
fig.update_layout(yaxis_title="(%) de SKU referencial")

st.plotly_chart(fig, theme="streamlit", use_container_width=True)
