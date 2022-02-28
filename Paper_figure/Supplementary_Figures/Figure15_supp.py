"""
============================
Figure 15 -- Online Resource
============================

"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('../../')
import python_codes.theme as theme
from python_codes.plot_functions import make_nice_histogram


# Loading figure theme
theme.load_style()

# paths
path_savefig = '../../Paper/Figures'
path_outputdata = '../../static/data/processed_data/'

# ##### Loading meteo data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
# Stations = ['South_Namib_Station', 'Deep_Sea_Station']
Stations = ['Deep_Sea_Station']

# #### Computing quantities
Orientation_era = np.concatenate([Data[station]['Orientation_era'] for station in Stations])
U_era = np.concatenate([Data[station]['U_star_era'] for station in Stations])
U_insitu = np.concatenate([Data[station]['U_star_insitu'] for station in Stations])
time = np.concatenate([Data[station]['time'] for station in Stations])
month = np.array([i.month for i in time])
hour = np.array([i.hour for i in time])
#
delta_u = (U_era - U_insitu)/U_era
limits = [0, -0.5]

# #### Figure
fig, axarr = plt.subplots(2, 2, figsize=(theme.fig_width, 0.9*theme.fig_width),
                          constrained_layout=True)
gs = axarr[0, 0].get_gridspec()
# remove the underlying axes
for ax in axarr[0, :]:
    ax.remove()
axbig = fig.add_subplot(gs[0, :])

for limit in limits:
    mask = delta_u < limit
    make_nice_histogram(Orientation_era[mask], 150, axbig, vmin=0, vmax=360, alpha=0.5, density=True)
    make_nice_histogram(month[mask], 13, axarr[1, 0], vmin=0.5, vmax=12.5, alpha=0.5, density=True)
    make_nice_histogram(hour[mask], 13, axarr[1, 1], vmin=-0.5, vmax=23.5, alpha=0.5, density=True)

axarr[1, 0].set_xlim(0.5, 12.5)
axarr[1, 1].set_xlim(-0.5, 23.5)
axbig.set_xlim(0, 360)
axarr[1, 0].set_xlabel('Months of the year')
axarr[1, 1].set_xlabel('Hours of the day')
axbig.set_xlabel(r'Wind orientation, $\theta_{\textup{ERA}}$')
axarr[1, 1].set_ylabel('PDF')
axarr[1, 0].set_ylabel('PDF')
axbig.set_ylabel('PDF')
axarr[1, 0].set_xticks([1, 3, 5, 7, 9, 11])
axarr[1, 1].set_xticks([0, 6, 12, 18])
axbig.set_xticks([0, 45, 90, 135, 180, 225, 270, 315, 360])

axarr[1, 0].text(0.04, 0.96, r'\textbf{b}', ha='left', va='top',
                 transform=axarr[1, 0].transAxes)
axarr[1, 1].text(0.04, 0.96, r'\textbf{c}', ha='left', va='top',
                 transform=axarr[1, 1].transAxes)
axbig.text(0.02, 0.96, r'\textbf{a}', ha='left', va='top',
           transform=axbig.transAxes)


plt.savefig(os.path.join(path_savefig, 'Figure15_supp.pdf'))
plt.show()