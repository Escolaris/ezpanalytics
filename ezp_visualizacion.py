# -*- coding: utf-8 -*-
# Copyright 2019 CSI_SAS.

"""Analisis AzProxy"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import datetime

DATE_TIME = "03_fec_inicio"
#DATA_URL = '..\ezp_analytics\data\export_dataframe.csv'
DATA_URL = 'export_dataframe.csv'

st.title("EZproxy: origenes de accesos y autenticaciones")

@st.cache(persist=True)
def load_data(nrows):

    data = pd.read_csv(DATA_URL,sep=",", header=0, engine='python', nrows=nrows) 
    #data = pd.read_csv(DATA_URL,sep="\ ", header=0, engine='python', nrows=nrows) 

    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    
    #01/Jan/2019:07:23:04
    #data[DATE_TIME] =  pd.to_datetime(data[DATE_TIME], format="%d/%b/%Y:%H:%M:%S")

    #2019-01-01 00:01:41
    data[DATE_TIME] =  pd.to_datetime(data[DATE_TIME], format="%Y-%m-%d %H:%M:%S")
    return data

data = load_data(60000)

#####################################################

# dibujar línea del tiempo
hour = st.slider("Horario disponibilidad del servicio", 0, 23)
data = data[data[DATE_TIME].dt.hour == hour]

# DataFrame
if st.checkbox("Show raw data", False):
    st.subheader("Datos entre %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)


#mapa
st.subheader("Geo data ente %i:00 y %i:00" % (hour, (hour + 1) % 24))

# mapa
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.deck_gl_chart(
    viewport={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        {
            "type": "HexagonLayer",
            "data": data,
            "radius": 100,
            "elevationScale": 4,
            "elevationRange": [0, 1000],
            "pickable": True,
            "extruded": True,
        }
    ],
)

# histograma
st.subheader("Desglose por minuto entre %i:00 y %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minuto": range(60), "accesos": hist})

st.write(alt.Chart(chart_data, height=150)    .mark_area(
        interpolate='step-after',
        line=True
    ).encode(
        x=alt.X("minuto:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("accesos:Q"),
        tooltip=['minuto', 'accesos']
    ))

