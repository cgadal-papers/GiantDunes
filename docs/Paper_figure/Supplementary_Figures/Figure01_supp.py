"""
============
Figure 1 -- SI
============

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import os
sys.path.append('../../')
import python_codes.theme as theme
from datetime import timedelta
#
theme.load_style()


def make_range_broken_barh(time, dt):
    diff = np.diff(time)
    t_diff = np.concatenate((time[1:][diff > dt_threshold], time[:-1][diff > dt_threshold]))
    t_diff = np.insert(t_diff, [0, t_diff.size], [time[0], time[-1]])
    t_diff = np.array(sorted(t_diff))
    return [(tstart, tspan) for tstart, tspan in zip(t_diff[::2], np.diff(t_diff)[::2])]


# Paths
path_savefig = '../../Paper/Figures'
path_inputdata = '../../static/input_data/'


Stations = ['Adamax_Station', 'Huab_Station', 'Deep_Sea_Station', 'South_Namib_Station']
dat_types = ['Era5Land_wind_data_', 'in_situ_wind_data_']
colors = ['tab:blue', 'tab:orange', 'tab:red']

dt_threshold = timedelta(minutes=60)
height_rect = 0.75
height_delta = 1
height_plot = 0
centers = []

fig_width = theme.fig_width
fig_height = 0.45*fig_width
fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
for station in Stations:
    for i, data_type in enumerate(dat_types):
        name = os.path.join(path_inputdata, station, data_type + station + '.npy')
        if os.path.exists(name):
            data = np.load(name, allow_pickle=True).item()
            time = data['time']
            if data_type == 'in_situ_wind_data_':
                orientation, velocities = data['direction'], data['velocity']
                mask = (~(np.isnan(velocities) | np.isnan(orientation))) & (velocities > 0)
            else:
                mask = np.ones(time.size).astype(bool)
            xranges = make_range_broken_barh(time[mask], dt_threshold)
            plt.broken_barh(xranges, (height_plot, height_rect), facecolor=colors[i])
            height_plot += height_rect
    centers.append(height_plot - height_rect)
    height_plot += height_delta

plt.xlabel('time [years]')
plt.gca().set_yticks(centers)
plt.gca().set_yticklabels([station[:-8].replace('_', ' ') for station in Stations])
ptch_Era5Land = mpatches.Patch(color=colors[0], label='Era5Land/Era5')
ptch_InSitu = mpatches.Patch(color=colors[1], label='In situ')
plt.legend(handles=[ptch_Era5Land, ptch_InSitu], loc='lower left')


plt.savefig(os.path.join(path_savefig, 'Figure1_supp.pdf'))
plt.show()