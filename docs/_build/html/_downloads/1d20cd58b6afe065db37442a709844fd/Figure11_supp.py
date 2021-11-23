"""
============
Figure 11 -- SI
============

"""

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import sys
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.plot_functions import make_nice_histogram

theme.load_style()

# paths
path_savefig = '../../Paper/Figures'
path_outputdata = '../../static/output_data/data/'
path_inputdata = '../../static/input_data'

# Loading data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}
mask = ~np.isnan(numbers['Froude'])
ad_hoc_quantity = np.concatenate([Data[station]['U_star_era'] for station in Stations])

# Figure properties
couples = [('Froude', 'kH'), ('kLB', 'kH')]
lims = {'Froude': (5.8e-3, 450), 'kLB': (0.009, 7.5), 'kH': (2.2e-2, 10.8)}
ax_labels = {'Froude': r'$Fr_{\textup{surface}}$', 'kH': '$k H$', 'kLB': r'$Fr_{\textup{internal}}$'}
norm = LogNorm(vmin=1, vmax=1.5e3)

# #### Figure
fig, axarr = plt.subplots(2, 3, figsize=(theme.fig_width, 0.8*theme.fig_width), sharey='row',
                          constrained_layout=True, gridspec_kw={'height_ratios': [1, 2], 'width_ratios': [2, 2, 1]})

axarr[0, -1].remove()
for j, (ax, (var1, var2)) in enumerate(zip(axarr[1, :2], couples)):
    ax.set_xscale('log')
    ax.set_yscale('log')
    #
    x_var, y_var = numbers[var1][mask], numbers[var2][mask]
    xlabel = ax_labels[var1]
    ylabel = ax_labels[var2] if j == 0 else None
    #
    bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
    bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
    # #### binning data
    counts, x_edge, y_edge = np.histogram2d(x_var, y_var, bins=[bin1, bin2])
    # plotting histogramm
    a = ax.pcolormesh(x_edge, y_edge, counts.T, snap=True, norm=norm)
    #
    ax.set_xlim(lims[var1])
    ax.set_ylim(lims[var2])
    ax.set_xlabel(ax_labels[var1])
    if j == 0:
        ax.set_ylabel(ax_labels[var2])
    # else:
    #     ax.set_yticklabels([])

for i, (ax, var) in enumerate(zip([axarr[0, 0], axarr[0, 1], axarr[1, -1]], ['Froude', 'kLB', 'kH'])):
    orientation = 'vertical' if i < 2 else 'horizontal'
    make_nice_histogram(Data['South_Namib_Station'][var], 150, ax, alpha=0.4, density=False, scale_bins='log', orientation=orientation)
    make_nice_histogram(Data['Deep_Sea_Station'][var], 150, ax, alpha=0.4, density=False, scale_bins='log', orientation=orientation)
    if i < 2:
        ax.set_xticklabels([])
        ax.set_xlim(lims[var])
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        if i == 0:
            ax.set_ylabel('Counts')
    else:
        ax.set_xlabel('Counts')
        ax.set_ylim(lims[var])
        # ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))


fig.colorbar(a, ax=axarr[0, :2], location='top', label='Counts', aspect=30)
#
plt.savefig(os.path.join(path_savefig, 'Figure11_supp.pdf'))
plt.show()
