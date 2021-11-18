import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import sys
import os
sys.path.append('../')
import python_codes.theme as theme
from python_codes.general import smallestSignedAngleBetween, find_mode_distribution
from python_codes.plot_functions import plot_regime_diagram

# Loading figure theme
theme.load_style()

# path
path_imgs = '../static/images/'
path_savefig = '../Paper/Figures'
path_outputdata = '../static/output_data/data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = ['South_Namib_Station', 'Deep_Sea_Station']

# #### Computing quantities

Orientation_era = np.concatenate([Data[station]['Orientation_era'] for station in Stations])
Orientation_station = np.concatenate([Data[station]['Orientation_station'] for station in Stations])
U_era = np.concatenate([Data[station]['U_star_era'] for station in Stations])
U_station = np.concatenate([Data[station]['U_star_station'] for station in Stations])
numbers = {key: np.concatenate([Data[station][key] for station in Stations]) for key in ('Froude', 'kH', 'kLB')}
#
Delta = smallestSignedAngleBetween(Orientation_era, Orientation_station)
mode_delta = np.array([find_mode_distribution(Delta, i) for i in np.arange(150, 350)]).mean()
delta_angle = np.abs(Delta)
delta_u = (U_era - U_station)/U_era

# #### Figure properties

quantities = [delta_angle, delta_u]
couples = [('Froude', 'kH'), ('kLB', 'kH')]
labels = [(r'\textbf{a}', r'\textbf{b}'), (r'\textbf{c}', r'\textbf{d}')]
#
ax_labels = {'Froude': r'$Fr_{\textup{surface}} =  U/\sqrt{(\Delta\rho/\rho) g H}$', 'kH': '$k H$', 'kLB': r'$Fr_{\textup{internal}} = k U/N$'}
lims = {'Froude': (5.8e-3, 450), 'kLB': (0.009, 7.5), 'kH': (2.2e-2, 10.8)}
#
regime_line_color = 'tab:blue'
cmaps = [theme.cmap_delta_theta, theme.cmap_delta_u]
norms = [mpcolors.Normalize(vmin=0, vmax=95),
         mpcolors.TwoSlopeNorm(vmin=-3.5, vcenter=0, vmax=1.2)]
cbar_labels = [r'$\delta_{\theta}$ [deg.]', r'$\delta_{u}$']
#

mask = ~np.isnan(numbers['Froude'])
log_counts_max = np.log10(2230)

# #### Figure

fig, axarr = plt.subplots(2, 2, figsize=(theme.fig_width, 0.525*theme.fig_height_max),
                          constrained_layout=True)
#
for i, (quantity, cmap, norm) in enumerate(zip(quantities, cmaps, norms)):
    for j, (var1, var2) in enumerate(couples):
        ax = axarr[i, j]
        vars = [numbers[var1][mask], numbers[var2][mask]]
        lims_list = [lims[var1], lims[var2]]
        xlabel = ax_labels[var1] if i > 0 else None
        ylabel = ax_labels[var2] if j == 0 else None
        #
        bin1 = np.logspace(np.floor(np.log10(numbers[var1][mask].min())), np.ceil(np.log10(numbers[var1][mask].max())), 50)
        bin2 = np.logspace(np.floor(np.log10(numbers[var2][mask].min())), np.ceil(np.log10(numbers[var2][mask].max())), 50)
        bins = [bin1, bin2]
        a = plot_regime_diagram(ax, quantity[mask], vars, lims_list, xlabel, ylabel, bins=bins, norm=norm, cmap=cmap, type='binned')
        #
        ax.text(0.04, 0.94, labels[i][j], transform=ax.transAxes, ha='left', va='center')

        # regime lines
        ax.axvline(0.4, color=regime_line_color, linestyle='--', lw=2)
        ax.axhline(0.32, color=regime_line_color, linestyle='--', lw=2)

    # colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, ax=axarr[i, :], orientation='vertical')
    cb.set_label(cbar_labels[i])
    if i == 0:
        cb.ax.xaxis.set_ticks_position('top')
        cb.ax.xaxis.set_label_position('top')

plt.savefig(os.path.join(path_savefig, 'Figure5.pdf'))
plt.show()
