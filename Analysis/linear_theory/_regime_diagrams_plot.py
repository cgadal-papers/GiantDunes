r"""
======================================================================
Plot the parameter space exploration of the hydrodyanamic coefficients
======================================================================

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from scipy.ndimage import gaussian_filter
import os
import sys
sys.path.append('../../')
import python_codes.theme as theme
theme.load_style()

# Paths
path_outputdata = '../../static/output_data/data/'

# Loading parameter space exploration
Dic = np.load(os.path.join(path_outputdata, 'parameter_exploration_hydro_coeff.npy'), allow_pickle=True).item()

# %%
# Plane (Froude - kH)
# ------------------------
hydro_coeffs = Dic[('Froude', 'kH')]['hydro_coeffs']

# #### figure
quantities = [hydro_coeffs[0, :, :], hydro_coeffs[1, :, :],
              np.linalg.norm(hydro_coeffs, axis=0), np.arctan2(hydro_coeffs[1, :, :], hydro_coeffs[0, :, :])]
labels = [r'$\mathcal{A}_{0}$', r'$\mathcal{B}_{0}$', r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$',
          r'$\textup{arctan}\left(\mathcal{B}_{0}/\mathcal{A}_{0}\right)$']
#
fig, axs = plt.subplots(2, 2, figsize=(theme.fig_width, 0.8*theme.fig_width), constrained_layout=True)
for i, (ax, label, quantity) in enumerate(zip(axs.flatten(), labels, quantities)):
    smoothed = gaussian_filter(quantity, 5)
    if i in [0, 2]:
        cmap = 'viridis'
        norm = None
    else:
        cmap = 'seismic'
        norm = TwoSlopeNorm(vcenter=0, vmin=smoothed.min(), vmax=smoothed.max())
    cnt = ax.contourf(Dic['Froude_vals'], Dic['kH_vals'], smoothed, levels=100, norm=norm, cmap=cmap)
    for c in cnt.collections:
        c.set_edgecolor("face")
    fig.colorbar(cnt, ax=ax, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    if i in [0, 2]:
        ax.set_ylabel(r'$k H$')
    else:
        ax.set_yticklabels([])
    if i in [2, 3]:
        ax.set_xlabel(r'Froude number, $\rho U/\sqrt{\Delta\rho g H}$')
    else:
        ax.set_xticklabels([])
plt.show()

# %%
# Plane (kLB - kH)
# ------------------------
hydro_coeffs = Dic[('kLB', 'kH')]['hydro_coeffs']

# #### figure
quantities = [hydro_coeffs[0, :, :], hydro_coeffs[1, :, :],
              np.linalg.norm(hydro_coeffs, axis=0), np.arctan2(hydro_coeffs[1, :, :], hydro_coeffs[0, :, :])]
labels = [r'$\mathcal{A}_{0}$', r'$\mathcal{B}_{0}$', r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$',
          r'$\textup{arctan}\left(\mathcal{B}_{0}/\mathcal{A}_{0}\right)$']
#
fig, axs = plt.subplots(2, 2, figsize=(theme.fig_width, 0.8*theme.fig_width), constrained_layout=True)
for i, (ax, label, quantity) in enumerate(zip(axs.flatten(), labels, quantities)):
    smoothed = gaussian_filter(quantity, 5)
    if i in [0, 2]:
        cmap = 'viridis'
        norm = None
    else:
        cmap = 'seismic'
        norm = TwoSlopeNorm(vcenter=0, vmin=smoothed.min(), vmax=smoothed.max())
    cnt = ax.contourf(Dic['kLB_vals'], Dic['kH_vals'], smoothed, levels=100, norm=norm, cmap=cmap)
    for c in cnt.collections:
        c.set_edgecolor("face")
    fig.colorbar(cnt, ax=ax, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    if i in [0, 2]:
        ax.set_ylabel(r'$k H$')
    else:
        ax.set_yticklabels([])
    if i in [2, 3]:
        ax.set_xlabel(r'$k L_{\textup{B}}$')
    else:
        ax.set_xticklabels([])
plt.show()

# %%
# Plane (Froude - kLB)
# ------------------------
hydro_coeffs = Dic[('Froude', 'kLB')]['hydro_coeffs']

# #### figure
quantities = [hydro_coeffs[0, :, :], hydro_coeffs[1, :, :],
              np.linalg.norm(hydro_coeffs, axis=0), np.arctan2(hydro_coeffs[1, :, :], hydro_coeffs[0, :, :])]
labels = [r'$\mathcal{A}_{0}$', r'$\mathcal{B}_{0}$', r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$',
          r'$\textup{arctan}\left(\mathcal{B}_{0}/\mathcal{A}_{0}\right)$']
#
fig, axs = plt.subplots(2, 2, figsize=(theme.fig_width, 0.8*theme.fig_width), constrained_layout=True)
for i, (ax, label, quantity) in enumerate(zip(axs.flatten(), labels, quantities)):
    smoothed = gaussian_filter(quantity, 5)
    if i in [0, 2]:
        cmap = 'viridis'
        norm = None
    else:
        cmap = 'seismic'
        norm = TwoSlopeNorm(vcenter=0, vmin=smoothed.min(), vmax=smoothed.max())
    cnt = ax.contourf(Dic['Froude_vals'], Dic['kLB_vals'], smoothed, levels=100, norm=norm, cmap=cmap)
    for c in cnt.collections:
        c.set_edgecolor("face")
    fig.colorbar(cnt, ax=ax, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    if i in [0, 2]:
        ax.set_ylabel(r'$k L_{\textup{B}}$')
    else:
        ax.set_yticklabels([])
    if i in [2, 3]:
        ax.set_xlabel(r'Froude number, $\rho U/\sqrt{\Delta\rho g H}$')
    else:
        ax.set_xticklabels([])
plt.show()
