"""
====================
Analysis of the DEMs
====================

Here, we extract from each DEMs the average orientation, wavelength and amplitude of the dune pattern:

    - we remove the general trend by fitting a second order polynomial surface.
    - we use autocorrelation of the residual topography to extract the three relevant quantities (see :func:`periodicity_2d <python_codes.DEM_analysis.periodicity_2d>` for details).
"""


import numpy as np
import os
from geopy import distance
import sys
sys.path.append('../')
from python_codes.DEM_analysis import polyfit2d, periodicity_2d
import python_codes.theme as theme

theme.load_style()


def DEM_analysis(file):
    data = np.load(file, allow_pickle=True).item()
    # Removing large scale topo
    kx, ky = 2, 2
    LON, LAT = np.meshgrid(data['lon'], data['lat'])
    soln, residuals, rank, s = polyfit2d(LON, LAT, data['DEM'], kx=kx, ky=ky, order_max=2)
    fitted_surf = np.polynomial.polynomial.polyval2d(LON, LAT, soln.reshape((kx + 1, ky + 1)).T)
    # Calculating average conversion deg -> km
    x_km = np.array([distance.distance((data['lat'][0], i), (data['lat'][0], data['lon'][0]), ellipsoid='WGS-84').km for i in data['lon']])
    y_km = np.array([distance.distance((i, data['lon'][0]), (data['lat'][0], data['lon'][0]), ellipsoid='WGS-84').km for i in data['lat']])
    km_step = np.mean([np.diff(x_km).mean(), np.diff(y_km).mean()])
    return *periodicity_2d(data['DEM'] - fitted_surf, 40), data['DEM'] - fitted_surf, data['lon'], data['lat'], km_step


Stations = ['Deep_Sea_Station', 'South_Namib_Station']
Data_DEM = {}
#
# Paths
path_outputdata = '../static/processed_data/'
path_inputdata = '../static/raw_data/'
#
for i, station in enumerate(Stations):
    file = os.path.join(path_inputdata, 'DEM/DEM_' + station + '.npy')
    orientation, wavelength_indx, amplitude, p0, p1, transect, C, topo, lon, lat, km_step = DEM_analysis(file)
    #
    Data_DEM[station] = {'orientation': orientation, 'wavelength': wavelength_indx*km_step,
                         'wavelength_indx': wavelength_indx,
                         'amplitude': amplitude, 'p0': p0, 'p1': p1,
                         'transect': transect, 'C': C, 'topo': topo, 'lat': lat,
                         'lon': lon, 'km_step': km_step}

np.save(os.path.join(path_outputdata, 'Data_DEM.npy'), Data_DEM)
