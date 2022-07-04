"""
============================
Figure 4
============================

"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../')
import python_codes.theme as theme
from python_codes.plot_functions import make_nice_histogram

# Loading figure theme
theme.load_style()

# paths
path_savefig = '../Paper/Figures'
path_outputdata = '../static/data/processed_data/'

# Loading wind data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'),
               allow_pickle=True).item()
Stations = ['Huab_Station', 'Adamax_Station']

# Figure properties
velocity_bins = [[0.05, 0.2], [0.3, 10]]
color_ax = 'purple'


# ################ Figure
fig, axarr = plt.subplots(3, 2, figsize=(theme.fig_width, 0.925*theme.fig_width),
                          constrained_layout=True, sharex=True)

for j, station in enumerate(Stations):
    label_station = 'Huab' if station == 'Huab_Station' else 'Etosha West'
    for i in range(3):  # Loop over velocites
        if i < 2:
            mask_U = (Data[station]['U_star_era'] >= velocity_bins[i][0]) & (Data[station]['U_star_era'] <= velocity_bins[i][1])
            label_u = r'$u_{*, \textup{ERA}} < ' + str(velocity_bins[i][1]) + '$ m~s$^{-1}$' if i == 0 else r'$u_{*, \textup{ERA}} > ' + str(velocity_bins[i][0]) + '$ m~s$^{-1}$'
        else:
            mask_U = (Data[station]['U_star_era'] < 10)  # take all velocities
            label_u = 'all velocities'
        axarr[i, -1].set_ylabel(label_u)
        axarr[i, -1].yaxis.set_label_position("right")
        #
        make_nice_histogram(Data[station]['Orientation_insitu'][mask_U], 80, axarr[i, j],
                            alpha=0.5, color=theme.color_insitu)
        make_nice_histogram(Data[station]['Orientation_era'][mask_U], 80, axarr[i, j],
                            alpha=0.5, color=theme.color_Era5Land)
        #
        #
        perc = (mask_U).sum()/mask_U.size
        hours = np.array([t.hour for t in Data[station]['time'][(mask_U)]])
        mask_day = (hours > 10) & (hours <= 10 + 12)
        perc_day = mask_day.sum()/(mask_U).sum()
        axarr[i, j].text(0.93, 0.95, '{:.1f} \n {:.1f}'.format(perc, perc_day),
                         ha='center', va='top', transform=axarr[i, j].transAxes)
        if i == 0:
            axarr[i, j].set_xlabel(label_station)
            axarr[i, j].xaxis.set_label_position("top")

plt.xlim(0, 360)
plt.xticks([45, 125, 215, 305])
for ax in axarr.flatten():
    ax.set_yticks([])
fig.supxlabel(r'Wind direction, $\theta~[^\circ]$')
fig.supylabel('Counts')

plt.savefig(os.path.join(path_savefig, 'Figure4.pdf'))
plt.show()
