"""
============
Figure 5 -- SI
============

"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.plot_functions import plot_scatter_surrounded


theme.load_style()

# paths
path_savefig = '../../Paper/Figures'
path_outputdata = '../../static/processed_data/'

Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
labels = [r'\textbf{a}', r'\textbf{b}']

# preparing data
Stations_ref = ['Adamax_Station', 'Huab_Station']
#
Theta_ERA = np.concatenate([Data[station]['Orientation_era'] for station in Stations_ref])
Theta_Station = np.concatenate([Data[station]['Orientation_insitu'] for station in Stations_ref])
#
U_ERA = np.concatenate([Data[station]['U_star_era'] for station in Stations_ref])
U_Station = np.concatenate([Data[station]['U_star_insitu'] for station in Stations_ref])


# #### Figure

fig, axrr = plt.subplots(1, 2, figsize=(theme.fig_width, 0.5*theme.fig_width),
                         constrained_layout=True)

for ax, label, quantity in zip(axrr, labels, [[Theta_ERA, Theta_Station], [U_ERA, U_Station]]):
    plt.sca(ax)
    plot_scatter_surrounded(quantity[0], quantity[1], color='tab:blue', alpha=0.1)
    ax.plot([0, 360], [0, 360], 'k--')
    ax.text(0.05, 0.95, label, ha='center', va='center', transform=ax.transAxes)

axrr[0].set_xlim(0, 360)
axrr[0].set_ylim(0, 360)
axrr[0].set_xticks([0, 90, 180, 270, 360])
axrr[0].set_yticks([0, 90, 180, 270, 360])
axrr[0].set_xlabel(r'$\theta_{\textup{ERA}}$')
axrr[0].set_ylabel(r'$\theta_{\textup{in situ}}$')
axrr[0].set_aspect('equal')
#
axrr[1].set_xlim(0, 0.5)
axrr[1].set_ylim(0, 0.5)
axrr[1].set_xlabel(r'$u_{*, \textup{ERA}}$')
axrr[1].set_ylabel(r'$u_{*, \textup{in situ}}$')
axrr[1].set_aspect('equal')
#

plt.savefig(os.path.join(path_savefig, 'Figure5_supp.pdf'), dpi=400)
plt.show()
