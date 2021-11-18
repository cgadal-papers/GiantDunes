r"""
============================================
Time series of the hydrodyanmic coefficients
============================================

Here, we calculate the time series of the hydrodynamic coefficients from the time series of the non dimensional parameters extracted from the meteorological and elevation data.
"""

import numpy as np
import os
import sys
sys.path.append('../../')
from python_codes.linear_theory import calculate_solution

# Paths
path_outputdata = '../../static/output_data/data/'

# Importing non-dimensional numbers calculated
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

# ##### Loading pattern characteristics
Data_pattern = {}
for station in ['Deep_Sea_Station', 'South_Namib_Station']:
    Data_pattern[station] = np.load(os.path.join(path_outputdata, 'Analysis_DEM_' + station + '.npy'), allow_pickle=True).item()

# Parameters
Kappa = 0.4  # Von Kàrmàn constant
k = np.concatenate([np.zeros(Data[station]['Froude'].shape) + 2*np.pi/(Data_pattern[station]['wavelength']*1e3) for station in Stations])  # vector of wavelength [m]
z0 = 1e-3  # hydrodynamic roughness, [m]
eta_0_vals = k*1e-3
eta = 0  # non dimensional position where to calculate the solution (bottom)

hydro_Coeffs = {}
for station in Stations:
    hydro_Coeffs[station] = np.zeros((2, Data[station]['kH'].size))
    k = 2*np.pi/(Data_pattern[station]['wavelength']*1e3)
    #
    for i, (eta_0, eta_H, Froude, eta_B) in enumerate(zip(eta_0_vals, Data[station]['kH'], Data[station]['Froude'], Data[station]['kLB'])):
        max_z = 0.9999*eta_H
        if not np.isnan([eta_H, Froude, eta_B]).any():
            Sol = calculate_solution(eta, eta_H, eta_0, eta_B, Froude, max_z, Kappa=0.4)
            #
            Ax, Bx = np.real(Sol[2]), np.imag(Sol[2])
        else:
            Ax, Bx = np.nan, np.nan
        hydro_Coeffs[station][:, i] = [Ax, Bx]
#
np.save(os.path.join(path_outputdata, 'time_series_hydro_coeffs.npy'), hydro_Coeffs)
