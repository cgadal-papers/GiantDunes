"""
==================================================================================
Plotting the regime diagrams from the sime series of the hydrodynamic coefficients
==================================================================================

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import matplotlib.colors as mpcolors
from scipy.stats import binned_statistic_2d
import os
import sys
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.plot_functions import log_tick_formatter, rgba_to_rgb
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
k = np.concatenate([np.zeros(Data[station]['Froude'].shape) + 2*np.pi/(Data_pattern[station]['wavelength']*1e3) for station in Stations])  # vector of wavelength [m]
xi = np.concatenate([np.zeros(Data[station]['Froude'].shape) + Data_pattern[station]['amplitude'] for station in Stations])  # vector of wavelength [m]

# %%
# Plotting the 3 possible regime diagrams -- scatter plots
# ------------------------
numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}
modulus = np.linalg.norm(Data_coeff, axis=0)
#
ax_labels = {'Froude': r'Froude number, $\rho U/\sqrt{\Delta\rho g H}$', 'kH': '$k H$', 'kLB': r'$k L_{\textup{B}}$'}
lims = {'Froude': (5.8e-3, 450), 'kLB': (0.009, 7.5), 'kH': (2.2e-2, 10.8)}
couples = [('Froude', 'kH'), ('kLB', 'kH'), ('Froude', 'kLB')]
mask = ~np.isnan(modulus)
plot_idx = np.random.permutation(np.arange(modulus[mask].size))  # to plot the points of the scatter plot in random order
#
fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.04, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.07, top=0.94, hspace=0.05)
gs_plots = gs[1].subgridspec(2, 2, hspace=0.05, wspace=0.05)
#
for i, (var1, var2) in enumerate(couples):
    ax = plt.subplot(gs_plots[i])
    ax.set_xscale('log')
    ax.set_yscale('log')
    a = plt.scatter(numbers[var1][plot_idx], numbers[var2][plot_idx], s=5, c=modulus[plot_idx], lw=0, rasterized=True, vmin=0, vmax=20, cmap='plasma')
    # a = plt.scatter(numbers[var1][plot_idx], numbers[var2][plot_idx], s=5, color=colors[plot_idx], lw=0, rasterized=True, vmin=0, vmax=20, cmap='plasma')
    ax.set_xlim(lims[var1])
    ax.set_ylim(lims[var2])
    if i in [0, 2]:
        plt.ylabel(ax_labels[var2])
    if i in [1, 2]:
        plt.xlabel(ax_labels[var1])
    if i == 0:
        ax.set_xticklabels([])
    if i == 1:
        ax.set_yticklabels([])

# colorbar
cb = fig.colorbar(a, cax=plt.subplot(gs[0]), orientation='horizontal')
cb.set_label(r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
plt.savefig(os.path.join(path_savefig, 'regime_diagrams_hydro_coeff.pdf'))
plt.show()


# %%
# Plotting the 3 possible regime diagrams -- binned
# ------------------------

log_counts_max = np.log10(2230)

fig = plt.figure(figsize=(np.round(theme.fig_width, 3), np.round(1.2*theme.fig_width, 3)))
gs = gridspec.GridSpec(2, 1, height_ratios=[0.2, 1], figure=fig)
gs.update(left=0.09, right=0.98, bottom=0.07, top=0.94, hspace=0.15)
gs_plots = gs[1].subgridspec(2, 2, hspace=0.05, wspace=0.05)
#
for i, (var1, var2) in enumerate(couples):
    ax = plt.subplot(gs_plots[i])
    ax.set_xscale('log')
    ax.set_yscale('log')
    #
    # #### binning data
    bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
    bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
    counts, x_edge, y_edge, _ = binned_statistic_2d(numbers[var1][mask], numbers[var2][mask], modulus[mask], statistic='count', bins=[bin1, bin2])
    average, x_edge, y_edge, _ = binned_statistic_2d(numbers[var1][mask], numbers[var2][mask], modulus[mask], statistic='mean', bins=[bin1, bin2])
    x_center = x_edge[:-1] + (x_edge[1] - x_edge[0])/2
    y_center = y_edge[:-1] + (y_edge[1] - y_edge[0])/2
    # #### making plot
    X, Y = np.meshgrid(x_center, y_center)
    a = plt.pcolormesh(x_edge, y_edge, average.T, vmax=20, snap=True)
    #
    # #### updating transparency
    log_counts = np.log10(counts)
    log_counts[np.abs(log_counts) == np.inf] = 0
    alpha_array = (log_counts/log_counts_max)
    fig.canvas.draw()
    colors = a.get_facecolor()
    colors[:, 3] = alpha_array.T.flatten()
    a.set_facecolor(rgba_to_rgb(colors))
    fig.canvas.draw()
    #
    ax.set_xlim(lims[var1])
    ax.set_ylim(lims[var2])
    if i in [0, 2]:
        plt.ylabel(ax_labels[var2])
    if i in [1, 2]:
        plt.xlabel(ax_labels[var1])
    if i == 0:
        ax.set_xticklabels([])
    if i == 1:
        ax.set_yticklabels([])

# #### colorbars color
gs_colorbars = gs[0].subgridspec(4, 1, hspace=0.3)
# colorbar color
norm = mpcolors.Normalize(vmin=0, vmax=20)
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
cb = fig.colorbar(sm, cax=plt.subplot(gs_colorbars[0]), orientation='horizontal')
cb.set_label(r'$\sqrt{\mathcal{A}_{0}^{2} + \mathcal{B}_{0}^{2}}$')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
# colorbar transparency
ncolors = 100
for i, perc in enumerate([0, 0.5, 0.99]):
    color_array = np.zeros((ncolors, 4))
    color_array[:, -1] = np.linspace(0, 1, ncolors)
    color_array[:, :-1] = plt.get_cmap('viridis')(perc)[:-1]
    color_array = rgba_to_rgb(color_array)
    #
    map_object = mpcolors.LinearSegmentedColormap.from_list(name='cmap_alpha', colors=color_array)
    norm = mpcolors.Normalize(vmin=0, vmax=log_counts_max)
    sm = plt.cm.ScalarMappable(cmap=map_object, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, cax=plt.subplot(gs_colorbars[i + 1]), orientation='horizontal', ticks=[0, 1, 2, 3])
    cb.solids.set_edgecolor("face")
    if i < 2:
        cb.set_ticklabels([])
    else:
        cb.ax.xaxis.set_major_formatter(mticker.FuncFormatter(log_tick_formatter))
        cb.ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        cb.set_label(r'$\textup{N}_{\textup{points}}$', labelpad=0)

plt.savefig(os.path.join(path_savefig, 'regime_diagrams_binned_hydro_coeff.pdf'))
plt.show()


# %%
# Plotting the 3D scatter plot
# ------------------------

fig = plt.figure(figsize=(theme.fig_width, theme.fig_width))
ax = fig.add_subplot(projection='3d')
ax.scatter(np.log10(numbers['Froude'][plot_idx]), np.log10(numbers['kH'][plot_idx]), np.log10(numbers['kLB'][plot_idx]), s=5, c=modulus[plot_idx], lw=0, rasterized=True, vmin=0, vmax=20, cmap='plasma')
ax.set_xlabel(ax_labels['Froude'][15:])
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
plt.savefig(os.path.join(path_savefig, 'regime_diagram_3d_hydro_coeff.pdf'))
plt.show()
