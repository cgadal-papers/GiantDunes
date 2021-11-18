r"""
=================================================================
Plot theoretical regime diagrams from parameter space exploration
=================================================================

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, Normalize
import matplotlib.gridspec as gridspec
from scipy.ndimage import gaussian_filter
import os
import sys
sys.path.append('../../')
from python_codes.linear_theory import Cisaillement_basal
import python_codes.theme as theme
theme.load_style()

# Paths
path_outputdata = '../../static/output_data/data/'
path_savefig = '../../static/output_data/figures/'

# Loading parameter space exploration
Dic = np.load(os.path.join(path_outputdata, 'parameter_exploration_hydro_coeff_3D.npy'), allow_pickle=True).item()
#
axes_av = [3, 2]  # axes over which selecting/averaging is perform for plane representation
index = [64, 45]  # when selection, selecting these indexes in the relevant `axes_av`
#
hydro_coeffs_3D = Dic[('Froude', 'kH', 'kLB')]['hydro_coeffs'].swapaxes(1, 2)
# axes are now (A/B, kH, Froude, kLB)

# %%
# Plane (Froude - kH)
# ------------------------
hydro_coeffs = hydro_coeffs_3D.take(index[0], axis=axes_av[0])

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
    cbar = fig.colorbar(cnt, ax=ax, label=label)
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
hydro_coeffs = hydro_coeffs_3D.take(index[1], axis=axes_av[1])

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
        norm = TwoSlopeNorm(vcenter=0, vmin=min(-0.00001, smoothed.min()), vmax=smoothed.max())
    cnt = ax.contourf(Dic['kLB_vals'], Dic['kH_vals'], smoothed, levels=100, norm=norm, cmap=cmap)
    for c in cnt.collections:
        c.set_edgecolor("face")
    cbar = fig.colorbar(cnt, ax=ax, label=label)
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
# Computing theoretical regime diagrams
# -------------------------------------
# fixing dune properties
alpha = 45
# aspect_ratio = 1/np.linalg.norm(hydro_coeffs_3D, axis=0).max()
aspect_ratio = 0.05
# #### Plot properties
cmaps = [theme.cmap_delta_theta, theme.cmap_delta_u]
norms = [Normalize(vmin=0, vmax=95), TwoSlopeNorm(vmin=-3.5, vcenter=0, vmax=1)]
# norms = [None, TwoSlopeNorm(vcenter=0)]
cbar_labels = [r'$\delta_{\theta}$ [deg.]', r'$\delta_{u}$']
x_labels = [r'Froude number, $ U/\sqrt{(\Delta\rho/\rho) g H}$', r'$k U/N$']
#
fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.08, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.07, top=0.94, hspace=0.17)
gs_plots = gs[1].subgridspec(2, 2, hspace=0.05, wspace=0.05)
#
for i, (axis, label) in enumerate(zip(axes_av, x_labels)):
    A0 = hydro_coeffs_3D.take(index[i], axis=axis)[0, :, :]
    B0 = hydro_coeffs_3D.take(index[i], axis=axis)[1, :, :]
    #
    x = 0
    y = np.pi/np.sin(alpha*180/np.pi)
    # y = np.pi/np.sin(alpha*180/np.pi) - np.arctan2(B0, A0)
    # Calculating basal shear stress
    TAU = Cisaillement_basal(x, y, alpha,
                             A0, B0, aspect_ratio)
    #
    # Calculating maximum redirection
    delta_angle = np.abs(np.arctan2(TAU[1], TAU[0]))*180/np.pi
    #
    # Calculating maximum relative difference
    delta_u = 1 - np.linalg.norm(np.array(TAU), axis=0)
    #
    quantities = [delta_angle, delta_u]
    for j, (quantity, cmap, norm) in enumerate(zip(quantities, cmaps, norms)):
        ax = plt.subplot(gs_plots[j, i])
        ax.set_xscale('log')
        ax.set_yscale('log')
        x_vals = Dic['Froude_vals'] if i == 0 else Dic['kLB_vals']
        a = plt.pcolormesh(x_vals, Dic['kH_vals'], quantity, norm=norm, snap=True, cmap=cmap)
        a.set_edgecolor('face')
        #
        if j > 0:
            plt.xlabel(label)
        else:
            ax.set_xticklabels([])
        #
        if i == 0:
            plt.ylabel(r'$k H$')
        else:
            ax.set_yticklabels([])

# #### colorbars
gs_colorbars = gs[0].subgridspec(2, 1, hspace=0.3)
for i, (norm, label, cmap) in enumerate(zip(norms, cbar_labels, cmaps)):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, cax=plt.subplot(gs_colorbars[i]), orientation='horizontal')
    cb.set_label(label)
    if i == 0:
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.xaxis.set_label_position('top')

plt.savefig(os.path.join(path_savefig, 'regime_diagrams_theoretical_' + '{:.4f}'.format(aspect_ratio) + '.pdf'))
plt.show()
