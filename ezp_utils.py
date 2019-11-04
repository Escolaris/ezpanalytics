# 
import pandas as pd
import pygeoip
from geolite2 import geolite2

geo = geolite2.reader()

#country en funcion ip
def get_country(ip):
    try:
        x = geo.get(ip)
    except ValueError:
        return pd.np.nan
    try:
        return x['country']['names']['en'] if x else pd.np.nan
    except KeyError:
        return pd.np.nan

#latitude  try en funcion ip
def get_latitud(ip):
    try:
        x = geo.get(ip)
    except ValueError:
        return pd.np.nan
    try:
        return x['location']['latitude'] if x else pd.np.nan
    except KeyError:
        return pd.np.nan

#longitud try en funcion ip
def get_longitude(ip):
    try:
        x = geo.get(ip)
    except ValueError:
        return pd.np.nan
    try:
        return x['location']['longitude'] if x else pd.np.nan
    except KeyError:
        return pd.np.nan

#city try en funcion ip
def get_city(ip):
    try:
        x = geo.get(ip)
    except ValueError:
        return pd.np.nan
    try:
        return x['city']['names']['en'] if x else pd.np.nan
    except KeyError:
        return pd.np.nan        