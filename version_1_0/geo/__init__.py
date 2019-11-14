"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

import numpy as np
from numba import njit

@njit
def haversine(lon1, lat1, lon2, lat2):
    """
    Haversine funciton gets distance between two points on a globe
    :param lon1: float, longitude of the first stop
    :param lat1: float, latitude of the first stop
    :param lon2: float, longitude of the second stop
    :param lat2: float, latitude of the second stop
    :return:
    """
    R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km
    lon1, lat1, lon2, lat2 = np.radians(lon1), np.radians(lat2) , np.radians(lon2), np.radians(lat2)
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = np.sin(dLat /2)** 2 + np.cos(lat1 ) *np.cos(lat2 ) *np.sin(dLon /2 )**2
    c = 2* np.arcsin(np.sqrt(a))
    return R * c * 5280