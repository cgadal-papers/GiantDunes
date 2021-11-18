"""
==================================
Processing the meteorological data
==================================


"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.meteo_analysis import mu
theme.load_style()

# Paths
path_savefig = '../../static/output_data/figures/'
path_outputdata = '../../static/output_data/data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

# ##### Loading pattern characteristics
Data_pattern = {}
for station in ['Deep_Sea_Station', 'South_Namib_Station']:
    Data_pattern[station] = np.load(os.path.join(path_outputdata, 'Analysis_DEM_' + station + '.npy'), allow_pickle=True).item()


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


# %%
# Plotting a few vertical profiles for the Deep Sea station
# ------------------------

def plot_fitprofile(height, Virtual_potential_temperature, grad_free_atm, theta_free_atm, blh, theta_ground, Hmax_fit):
    mask_H = (height >= blh) & (height <= Hmax_fit)
    #
    plt.plot(Virtual_potential_temperature, height/1e3, '+', label='data', zorder=-1)
    plt.vlines(theta_ground, 0, blh/1e3, linewidth=2, label='boundary layer', zorder=0, color='tab:orange')
    plt.plot(np.poly1d([grad_free_atm, theta_free_atm])(height[mask_H]), height[mask_H]/1e3, linewidth=2, label='free atm.', color='tab:green')
    plt.xlabel('Virtual potential temp. [K]')
    plt.ylabel('Height [km]')
    plt.gca().set_ylim(0, top=0.7*Hmax_fit/1e3)
    plt.gca().set_xlim(280, 350)
    plt.legend()


times = [2012, 30254, 2024, 30266]
plt.figure(figsize=(theme.fig_width, 0.9*theme.fig_width), constrained_layout=True)
for i, t in enumerate(times):
    ax = plt.subplot(2, 2, i+1)
    plot_fitprofile(height_sort[:, t], Virtual_potential_temperature_sort[:, t], gradient_free_atm[t],
                    theta_free_atm[t], BLH[t], theta_ground[t], Hmax_fit)
    ax.set_title(Data[station]['time'][t])
plt.savefig(os.path.join(path_savefig, 'fit_virtual_potential_temperature.pdf'))
plt.show()


# %%
# Plotting the distributions of the non dimensional parameters for both stations
# ------------------------

def make_nice_histogram(data, nbins, ax, vmin=None, vmax=None, scale_bins='log', density=True, **kwargs):
    min = data.min() if vmin is None else vmin
    max = data.max() if vmax is None else vmax
    if scale_bins == 'log':
        bins = np.logspace(np.log10(min), np.log10(max), nbins)
    else:
        bins = np.linspace(min, max, nbins)
    a = ax.hist(data, bins=bins, histtype='stepfilled', density=density, **kwargs)
    ax.hist(data, bins=bins, histtype='step', color=a[-1][0].get_fc(), lw=2, density=density)


fig, axs = plt.subplots(3, 1, figsize=(theme.fig_width, 0.9*theme.fig_width), constrained_layout=True)
for station in Stations:
    make_nice_histogram(Data[station]['Froude'], 150, axs[0], alpha=0.5, vmin=0.06, vmax=50, label=' '.join(station.split('_')[:-1]))
    make_nice_histogram(Data[station]['kH'], 150, axs[1], alpha=0.5, vmin=0.07, label=' '.join(station.split('_')[:-1]))
    make_nice_histogram(Data[station]['kLB'], 150, axs[2], alpha=0.5, vmin=0.06, label=' '.join(station.split('_')[:-1]))
#
for ax in axs:
    ax.set_xscale('log')
    ax.set_ylabel('PDF')
    plt.sca(ax)
    plt.legend()
#
axs[0].set_xlabel(r'Froude number, $Fr$')
axs[1].set_xlabel(r'$k H$')
axs[2].set_xlabel(r'$k L_{\textup{B}}$')
plt.savefig(os.path.join(path_savefig, 'distributions_non_dimensional_parameters.pdf'))
plt.show()


# %%
# Temporal distributions of ill-processed vertical profiles
# ---------------------------------------------------------
fig, axs = plt.subplots(1, 1, figsize=(theme.fig_width, 0.6*theme.fig_width), constrained_layout=True)
for station in Stations:
    hr = np.array([i.hour for i in Data[station]['time']])
    make_nice_histogram(hr[np.isnan(Data[station]['Froude'])], 24, axs, alpha=0.5, vmin=0, vmax=23, label=' '.join(station.split('_')[:-1]), scale_bins='lin', density=False)
axs.set_xlabel('Hours of the day')
axs.set_ylabel(r'$N_{\textup{points}}$')
plt.sca(axs)
plt.xlim(0, 23)
plt.legend()
plt.savefig(os.path.join(path_savefig, 'distributions_failed_meteo_analysis.pdf'))
plt.show()
