r"""
=============================================================
Parameter space exploration for the hydrodyanmic coefficients
=============================================================

In this script, we derive the basal shear stress coefficients across the entire 3D space of non-dimensional parameters :math:`(k H, Fr, k U/N)`.

.. note::

    The parameter space exploration takes a certain amount of times to run, and as such is separated from the plotting of the results.

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
numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}

# ##### Loading pattern characteristics
Data_pattern = {}
for station in ['Deep_Sea_Station', 'South_Namib_Station']:
    Data_pattern[station] = np.load(os.path.join(path_outputdata, 'Analysis_DEM_' + station + '.npy'), allow_pickle=True).item()

# Parameters
Kappa = 0.4  # Von Kàrmàn constant
k = 2*np.pi/np.mean([Data_pattern[station]['wavelength']*1e3 for station in Stations])  # mean wavelength [m]
z0 = 1e-3  # hydrodynamic roughness, [m]
eta_0 = k*1e-3
eta = 0  # non dimensional position where to calculate the solution (bottom)

# Parameter space
Npoints = 50
Dic = {}
Dic['kH_vals'] = np.logspace(-2, 1.1, Npoints)
Dic['Froude_vals'] = np.logspace(-2.3, 2.5, Npoints)
Dic['kLB_vals'] = np.logspace(-2.1, 1, Npoints)
#
Dic[('Froude', 'kH', 'kLB')] = {}
Dic[('Froude', 'kH', 'kLB')]['hydro_coeffs'] = np.zeros((2, Npoints, Npoints, Npoints))
#
for i, Fr in enumerate(Dic['Froude_vals']):
    print(i)
    for j, eta_H in enumerate(Dic['kH_vals']):
        for k, eta_B in enumerate(Dic['kLB_vals']):
            max_z = 0.9999*eta_H
            Sol = calculate_solution(eta, eta_H, eta_0, eta_B, Fr, max_z, Kappa=Kappa)
            #
            Ax, Bx = np.real(Sol[2]), np.imag(Sol[2])
            Dic[('Froude', 'kH', 'kLB')]['hydro_coeffs'][:, i, j, k] = [Ax, Bx]
#
np.save(os.path.join(path_outputdata, 'parameter_exploration_hydro_coeff_3D.npy'), Dic)
