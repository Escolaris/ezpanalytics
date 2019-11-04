# -*- coding: utf-8 -*-
# toma el archivo log de ezproxy y lo conviete en un DataFrame

import pandas as pd
import numpy as np
import altair as alt

import datetime

# ips
import ezp_utils as utilidades

# constantes
IPUSUARIO   = '00_ip_cliente'
DATE_TIME   = "03_fec_inicio"
HUSO_TIME   = '04_uso_horario'

#DATA_LOG    = "..\ezp_analytics\data\ezp201901.log"
#DATA_FRAME  = '..\ezp_analytics\data\export_dataframe.csv'

DATA_LOG    = "ezp201901.log"
DATA_FRAME  = 'export_dataframe.csv'

NRO_FILAS   = 60000

#@st.cache(persist=True)
def load_data(nrows):

    #data = pd.read_csv('ezp201901_3.tsv',sep="\ ", header=0, engine='python', nrows=nrows) 
    #data = pd.read_csv('ezp201901.log',sep="\ ", header=0, engine='python', nrows=nrows) 
    
    data = pd.read_csv(DATA_LOG,sep="\ ", header=0, engine='python', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    
    #01/Jan/2019:07:23:04
    data[DATE_TIME] =  pd.to_datetime(data[DATE_TIME], format="%d/%b/%Y:%H:%M:%S")

    return data

data = load_data(NRO_FILAS)

#  descifrar IP

# get unique IPs
unique_ips = data[IPUSUARIO].unique()

# make series out of it
unique_ips = pd.Series(unique_ips, index = unique_ips)

# map IP --> country, city, lat, long
data['country'] = data[IPUSUARIO].map(unique_ips.apply(utilidades.get_country))
data['city'] = data[IPUSUARIO].map(unique_ips.apply(utilidades.get_city))
data['lat'] = data[IPUSUARIO].map(unique_ips.apply(utilidades.get_latitud))
data['lon'] = data[IPUSUARIO].map(unique_ips.apply(utilidades.get_longitude))               

# Exportar DF
data.to_csv(DATA_FRAME, index = False, header=True)  