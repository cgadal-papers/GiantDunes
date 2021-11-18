"""
=====================================================
Plot theoretical regime diagrams from the time series
=====================================================

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import matplotlib.colors as mpcolors
import os
import sys
sys.path.append('../../')
from python_codes.linear_theory import Cisaillement_basal
from python_codes.plot_functions import log_tick_formatter, plot_regime_diagram
import python_codes.theme as theme
theme.load_style()


# Paths
path_savefig = '../../static/output_data/figures/'
path_outputdata = '../../static/output_data/data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()

# ##### Loading time series of hydrodyamic coefficients
Data_coeff = np.load(os.path.join(path_outputdata, 'time_series_hydro_coeffs.npy'))

# ##### Loading pattern characteristics
Data_pattern = {}
for station in ['Deep_Sea_Station', 'South_Namib_Station']:
    Data_pattern[station] = np.load(os.path.join(path_outputdata, 'Analysis_DEM_' + station + '.npy'), allow_pickle=True).item()


Stations = ['South_Namib_Station', 'Deep_Sea_Station']
# Stations = ['South_Namib_Station']

# %%
# Plotting the regime diagrams for the modulus -- scatter plots
# -------------------------------------------------------------
numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}
modulus = np.linalg.norm(Data_coeff, axis=0)
# phase = np.arctan2(Data_coeff[1], Data_coeff[0])
#
ax_labels = {'Froude': r'$Fr_{\textup{surface}} =  U/\sqrt{(\Delta\rho/\rho) g H}$', 'kH': '$k H$', 'kLB': r'$Fr_{\textup{internal}} = k U/N$'}
lims = {'Froude': (5.8e-3, 450), 'kLB': (0.009, 7.5), 'kH': (2.2e-2, 10.8)}
couples = [('Froude', 'kH'), ('kLB', 'kH')]
mask = ~np.isnan(modulus)
plot_idx = np.random.permutation(np.arange(modulus[mask].size))  # to plot the points of the scatter plot in random order
#
fig = plt.figure(figsize=(theme.fig_width, 0.7*theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.04, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.09, top=0.91, hspace=0.05)
gs_plots = gs[1].subgridspec(1, 2, hspace=0.05, wspace=0.05)
#
for i, (var1, var2) in enumerate(couples):
    ax = plt.subplot(gs_plots[i])
    vars = [numbers[var1][plot_idx], numbers[var2][plot_idx]]
    cmap = 'viridis'
    lims_list = [lims[var1], lims[var2]]
    xlabel = ax_labels[var1]
    ylabel = ax_labels[var2] if i == 0 else None
    a = plot_regime_diagram(ax, modulus[plot_idx], vars, lims_list, xlabel, ylabel, vmin=0, vmax=20, cmap='plasma')
    # a = plot_regime_diagram(ax, phase[plot_idx], vars, lims_list, xlabel, ylabel, cmap='plasma')

# colorbar
cb = fig.colorbar(a, cax=plt.subplot(gs[0]), orientation='horizontal')
cb.set_label(r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
plt.savefig(os.path.join(path_savefig, 'regime_diagrams_modulus.pdf'))
plt.show()


# %%
# Plotting the regime diagrams for the modulus -- binned plots
# -------------------------------------------------------------

log_counts_max = np.log10(2230)

fig = plt.figure(figsize=(theme.fig_width, 0.7*theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.04, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.09, top=0.91, hspace=0.05)
gs_plots = gs[1].subgridspec(1, 2, hspace=0.05, wspace=0.05)
#
for i, (var1, var2) in enumerate(couples):
    ax = plt.subplot(gs_plots[i])
    vars = [numbers[var1][mask], numbers[var2][mask]]
    cmap = 'viridis'
    lims_list = [lims[var1], lims[var2]]
    xlabel = ax_labels[var1]
    ylabel = ax_labels[var2] if i == 0 else None
    #
    bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
    bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
    bins = [bin1, bin2]
    a = plot_regime_diagram(ax, modulus[mask], vars, lims_list, xlabel, ylabel, bins=bins, vmin=0, vmax=20, cmap='plasma', type='binned')

# #### colorbar
cb = fig.colorbar(a, cax=plt.subplot(gs[0]), orientation='horizontal')
cb.set_label(r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')

plt.savefig(os.path.join(path_savefig, 'regime_diagrams_binned_modulus.pdf'))
plt.show()


# %%
# Plotting the 3D scatter plot
# ------------------------

fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
ax = fig.add_subplot(projection='3d')
ax.scatter(np.log10(numbers['Froude'][plot_idx]), np.log10(numbers['kH'][plot_idx]), np.log10(numbers['kLB'][plot_idx]), s=5, c=modulus[plot_idx], lw=0, rasterized=True, vmin=0, vmax=20, cmap='plasma')
ax.set_xlabel(ax_labels['Froude'])
ax.set_ylabel(ax_labels['kH'])
ax.set_zlabel(ax_labels['kLB'])
#
ax.xaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.zaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
ax.zaxis.set_major_locator(mticker.MaxNLocator(integer=True))
#
ax.view_init(elev=22, azim=-111)
plt.subplots_adjust(left=0.05, right=1, bottom=0.05, top=1)
plt.savefig(os.path.join(path_savefig, 'regime_diagram_3d_modulus.pdf'))
plt.show()

# %%
# Regime diagrams for the orientation/velocity -- scatter plots
# -------------------------------------------------------------

# #### Calculation of the predicted redirections and attenuation
x = 0
# time series of input variables
Orientation_era = np.concatenate([Data[station]['Orientation_era'] for station in Stations])
k = np.concatenate([np.zeros(Data[station]['Froude'].shape) + 2*np.pi/(Data_pattern[station]['wavelength']*1e3) for station in Stations])  # vector of wavelength [m]
xi = np.concatenate([np.zeros(Data[station]['Froude'].shape) + Data_pattern[station]['amplitude'] for station in Stations])  # vector of wavelength [m]
alphas_dune = np.concatenate([np.zeros(Data[station]['Froude'].shape) + Data_pattern[station]['orientation'] for station in Stations]) - 90  # vector of wavelength [m]
alphas_th = ((alphas_dune - Orientation_era + 90) % 180) - 90
A0, B0 = Data_coeff[0, :], Data_coeff[1, :]
y = np.pi/np.sin(alphas_th*180/np.pi)  # to always be in between two dunes
# Calculating maximum redirection
TAU = Cisaillement_basal(x, y, alphas_dune, A0, B0, k*xi)
#
delta_angle = np.abs(np.arctan2(TAU[1], TAU[0]))*180/np.pi
# Calculating maximum relative difference
delta_u = 1 - np.linalg.norm(np.array(TAU), axis=0)

# #### Plotting quantities
quantities = [delta_angle, delta_u]
cmaps = [theme.cmap_delta_theta, theme.cmap_delta_u]
cbar_labels = [r'$\delta_{\theta}$ [deg.]', r'$\delta_{u}$']
norms = [mpcolors.Normalize(vmin=0, vmax=7), mpcolors.TwoSlopeNorm(vmin=-2, vcenter=0, vmax=0.2)]
#
fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.08, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.07, top=0.94, hspace=0.17)
gs_plots = gs[1].subgridspec(2, 2, hspace=0.05, wspace=0.05)
#
for i, (quantity, cmap, norm) in enumerate(zip(quantities, cmaps, norms)):
    for j, (var1, var2) in enumerate(couples):
        ax = plt.subplot(gs_plots[i, j])
        vars = [numbers[var1][plot_idx], numbers[var2][plot_idx]]
        lims_list = [lims[var1], lims[var2]]
        xlabel = ax_labels[var1] if i > 0 else None
        ylabel = ax_labels[var2] if j == 0 else None
        a = plot_regime_diagram(ax, quantity[plot_idx], vars, lims_list, xlabel, ylabel, norm=norm, cmap=cmap)

# #### colorbars
gs_colorbars = gs[0].subgridspec(2, 1, hspace=0.3)
for i, (norm, label, cmap) in enumerate(zip(norms, cbar_labels, cmaps)):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, cax=plt.subplot(gs_colorbars[i]), orientation='horizontal')
    cb.set_label(label)
    if i == 0:
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.xaxis.set_label_position('top')

plt.savefig(os.path.join(path_savefig, 'regime_diagrams_predicted_scatter.pdf'))
plt.show()

# %%
# Regime diagrams for the orientation/velocity -- binned plots
# -------------------------------------------------------------
fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.08, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.07, top=0.94, hspace=0.17)
gs_plots = gs[1].subgridspec(2, 2, hspace=0.05, wspace=0.05)
#
for i, (quantity, cmap, norm) in enumerate(zip(quantities, cmaps, norms)):
    for j, (var1, var2) in enumerate(couples):
        ax = plt.subplot(gs_plots[i, j])
        vars = [numbers[var1][mask], numbers[var2][mask]]
        lims_list = [lims[var1], lims[var2]]
        xlabel = ax_labels[var1] if i > 0 else None
        ylabel = ax_labels[var2] if j == 0 else None
        #
        bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
        bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
        bins = [bin1, bin2]
        a = plot_regime_diagram(ax, quantity[mask], vars, lims_list, xlabel, ylabel, bins=bins, norm=norm, cmap=cmap, type='binned')

# #### colorbars
gs_colorbars = gs[0].subgridspec(2, 1, hspace=0.3)
for i, (norm, label, cmap) in enumerate(zip(norms, cbar_labels, cmaps)):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, cax=plt.subplot(gs_colorbars[i]), orientation='horizontal')
    cb.set_label(label)
    if i == 0:
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.xaxis.set_label_position('top')

plt.savefig(os.path.join(path_savefig, 'regime_diagrams_predicted_binned.pdf'))
plt.show()
