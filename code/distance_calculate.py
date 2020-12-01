#use lat and lon to calculate the distance between two points
#https://stackoverflow.com/a/21623206
import pandas as pd
import numpy as np
import math
def distance_formula(lat1, lon1, lat2, lon2):
    p = np.pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 12742 * np.arcsin(np.sqrt(a)) * 1000.0  #2*R*asin...

def distance_formula_row(row):
    lat1 = row['user_lat']
    lon1 = row['user_lon']
    lat2 = row['loc'][0]
    lon2 = row['loc'][1]
    p = np.pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 12742 * np.arcsin(np.sqrt(a)) * 1000.0  #2*R*asin...


