"""
============================
Figure 11 -- Online Resource
============================

"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import matplotlib.transforms as mtransforms
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.general import smallestSignedAngleBetween, find_mode_distribution
from python_codes.plot_functions import plot_regime_diagram

# Loading figure theme
theme.load_style()

# paths
path_savefig = '../../Paper/Figures'
path_outputdata = '../../static/data/processed_data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

# #### Computing quantities

Orientation_era = np.concatenate([Data[station]['Orientation_era'] for station in Stations])
Orientation_insitu = np.concatenate([Data[station]['Orientation_insitu'] for station in Stations])
U_era = np.concatenate([Data[station]['U_star_era'] for station in Stations])
U_insitu = np.concatenate([Data[station]['U_star_insitu'] for station in Stations])
numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}
#
Delta = smallestSignedAngleBetween(Orientation_era, Orientation_insitu)
mode_delta = np.array([find_mode_distribution(Delta, i) for i in np.arange(150, 350)]).mean()
delta_angle = np.abs(Delta)
delta_u = (U_era - U_insitu)/U_era

# #### Figure parameters

lims = {'Froude': (5.8e-3, 450), 'kLB': (0.009, 7.5), 'kH': (2.2e-2, 10.8)}
cmaps = [theme.cmap_delta_theta, theme.cmap_delta_u]
norms = [mpcolors.Normalize(vmin=0, vmax=99),
         mpcolors.TwoSlopeNorm(vmin=-3, vcenter=0, vmax=1)]
cbar_labels = [r'$\delta_{\theta}~[^\circ]$', r'$\delta_{u}$']
quantities = [delta_angle, delta_u]
labels = [r'\textbf{a}', r'\textbf{b}', r'\textbf{c}', r'\textbf{d}']
cbticks = [[0, 25, 50, 75], [-3, -1.5, 0, 0.5, 1]]

mask = ~np.isnan(numbers['Froude'])
log_counts_max = np.log10(2230)

vars = [('kLB', 'kH'), ('kLB', 'Froude')]
ax_labels = {'kH': r'$kH$', 'Froude': r'$\mathcal{F} =  U/\sqrt{(\Delta\rho/\rho_{0}) g H}$',
             'kLB': r'$\mathcal{F}_{\textup{I}} =  kU/N$'}
xlabels = [r'$\mathcal{F}_{\textup{I}} =  kU/N$']
ylabels = [r'$kH$', r'$\mathcal{F} =  U/\sqrt{(\Delta\rho/\rho) g H}$']
lim_regime = {'kH': 0.32, 'Froude': 0.4, 'kLB': 0.35}


# #### Figure
fig, axarr = plt.subplots(2, 2, figsize=(theme.fig_width, 0.6*theme.fig_height_max),
                          constrained_layout=True, gridspec_kw={'height_ratios': [1, 1]})

# #### colorbars
for i, (cmap, norm, cbtick) in enumerate(zip(cmaps, norms, cbticks)):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = plt.colorbar(sm, ax=axarr[0, i], location='top', ticks=cbtick)
    cb.set_label(cbar_labels[i])

for i, (var1, var2) in enumerate(vars):
    for j, (ax, quantity, cmap, norm) in enumerate(zip(axarr[i, :].flatten(), quantities, cmaps, norms)):
        vars = [numbers[var1][mask], numbers[var2][mask]]
        lims_list = [lims[var1], lims[var2]]
        #
        bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
        bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
        bins = [bin1, bin2]
        xlabel = None if i < 1 else ax_labels[var1]
        ylabel = None if j > 0 else ax_labels[var2]
        #
        a = plot_regime_diagram(ax, quantity[mask], vars, lims_list, xlabel, ylabel, bins=bins, norm=norm, cmap=cmap, type='binned')
        #
        # regime lines
        ax.axvline(lim_regime[var1], color=theme.regime_line_color, linestyle='--', lw=2)
        ax.axhline(lim_regime[var2], color=theme.regime_line_color, linestyle='--', lw=2)

trans = mtransforms.ScaledTranslation(5/72, -5/72, fig.dpi_scale_trans)
for i, (ax, label) in enumerate(zip(axarr.flatten(), labels)):
    ax.text(0.0, 1.0, label, transform=ax.transAxes + trans, va='top')

fig.align_labels()
plt.savefig(os.path.join(path_savefig, 'Figure11_supp.pdf'), dpi=400)
plt.show()
