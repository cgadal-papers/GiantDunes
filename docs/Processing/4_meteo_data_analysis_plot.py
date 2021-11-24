"""
==================================
Processing the meteorological data
==================================


"""

import numpy as np
import os
import sys
sys.path.append('../')
import python_codes.theme as theme
from python_codes.meteo_analysis import mu
theme.load_style()

# Paths
path_savefig = '../static/output_data/figures/'
path_outputdata = '../static/output_data/data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

# ##### Loading pattern characteristics
Data_pattern = np.load(os.path.join(path_outputdata, 'Data_DEM.npy'), allow_pickle=True).item()


# %%
# Calculating the relevant meteorological quantities
# ------------------------
#
# We calculate the relevant meteorological quantities from the Era5 pressure levels data.

# Parameters
g = 9.81  # gravitational acceleration [m2/s]
Rt = 6356766  # Average Earth radius [m]
Kelvin = 273.15  # Kelvin shift
P0 = 1000        # Standard pressure [hPa]
Md = 0.029       # Molecular mass of dry air [kg/mol]
Mw = 0.018       # Molecular mass of water [kg/mol]
R_M = Md/Mw
R = 8.314  # Gaz constant
Pc = 0.2854      # Poisson coefficient for dry air R/Cp
z0_era = 1e-3  # hydrodynamic roughness chosen for the Era5Land dataset [m]

# #### Calculating relevant meteorological quantities
for station in Stations:
    Data[station]['height'] = Data[station]['Geopotential']*Rt/(g*Rt - Data[station]['Geopotential'])
    Data[station]['Potential_temperature'] = Data[station]['Temperature']*(P0/Data[station]['Pressure levels'][:, None])**(Pc*(1 - 0.24*Data[station]['Specific humidity']))
    Data[station]['Virtual_potential_temperature'] = (1 + (R_M - 1)*Data[station]['Specific humidity'])*Data[station]['Potential_temperature']
    Data[station]['Density'] = (P0*Md/(R*Data[station]['Virtual_potential_temperature']))*(P0/Data[station]['Pressure levels'][:, None])**(Pc-1)


# %%
# Analyzing the vertical profiles of virtual potential temperature
# ------------------------

Hmax_fit = 10000  # maximum height for fitting gradient in free atmosphere [m]
for station in Stations:
    # ordering by pressure levels
    height_sort = Data[station]['height'][Data[station]['Pressure levels'].argsort()[::-1]].data
    Potential_temperature_sort = Data[station]['Potential_temperature'][Data[station]['Pressure levels'].argsort()[::-1]].data
    Virtual_potential_temperature_sort = Data[station]['Virtual_potential_temperature'][Data[station]['Pressure levels'].argsort()[::-1]].data
    Temperature_sort = Data[station]['Temperature'][Data[station]['Pressure levels'].argsort()[::-1]].data
    Density_sort = Data[station]['Density'][Data[station]['Pressure levels'].argsort()[::-1]].data
    #
    BLH = Data[station]['Boundary layer height'].data
    theta_ground = np.zeros((BLH.size,))
    theta_free_atm = np.zeros((BLH.size,))
    gradient_free_atm = np.zeros((BLH.size,))
    #
    for t, time in enumerate(Data[station]['time']):
        mask_H = (height_sort[:, t] >= BLH[t]) & (height_sort[:, t] <= Hmax_fit)
        gradient_free_atm[t], theta_free_atm[t] = np.polyfit(height_sort[:, t][mask_H], Virtual_potential_temperature_sort[:, t][mask_H], 1)  # fitting linear trend in the free atmosphere
        # Computing temperature in the convective boundary layer
        if BLH[t] >= height_sort[:, t].min():
            theta_ground[t] = Virtual_potential_temperature_sort[:, t][(height_sort[:, t] <= BLH[t])].mean()
        else:
            theta_ground[t] = Virtual_potential_temperature_sort[0, t]
    #
    # ### temperature jump
    delta_theta = np.array([np.poly1d([grad, theta])(blh) for (grad, theta, blh) in zip(gradient_free_atm, theta_free_atm, BLH)]) - theta_ground
    delta_theta[delta_theta < 0] = np.nan
    #
    N = np.sqrt(g*gradient_free_atm/theta_ground)   # Brunt vaisala frequency
    LB = Data[station]['U_star_era']*mu(BLH, z0_era)/N  # corresponding length scale
    k = 2*np.pi/(Data_pattern[station]['wavelength']*1e3)
    #
    # Calculating relevant non-dimensional numbers
    Data[station]['Froude'] = Data[station]['U_star_era']*mu(BLH, z0_era)/np.sqrt((delta_theta/theta_ground)*g*BLH)
    Data[station]['kH'] = k*BLH
    Data[station]['kLB'] = k*LB
    #
    # Storing other relevant quantities
    Data[station]['delta_theta'] = delta_theta
    Data[station]['theta_ground'] = theta_ground
    Data[station]['theta_free_atm'] = theta_free_atm
    Data[station]['gradient_free_atm'] = gradient_free_atm

# Saving
np.save(os.path.join(path_outputdata, 'Data_final.npy'), Data)
