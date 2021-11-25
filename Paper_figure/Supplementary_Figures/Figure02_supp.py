"""
============
Figure 2 -- SI
============

"""

import numpy as np
import os
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
sys.path.append('../../')
import python_codes.theme as theme

theme.load_style()

# paths
path_savefig = '../../Paper/Figures'
path_outputdata = '../../static/output_data/data/'
path_inputdata = '../../static/input_data'

# figure parameters
station = 'South_Namib_Station'
tmin, tmax = datetime(2017, 6, 3), datetime(2017, 6, 10)
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()

# Loading and recomputing some raw data
path_insitu = os.path.join(path_inputdata, station, 'in_situ_wind_data_' + station + '.npy')
Data_insitu = np.load(path_insitu, allow_pickle=True).item()
#
t_station = Data_insitu['time']
U_station = Data_insitu['velocity']
# putting angles in trigo. ref.
Orientation_station = (270 - Data_insitu['direction']) % 360


# ### Figure
fig, axarr = plt.subplots(2, 1, figsize=(theme.fig_width, 0.85*theme.fig_width),
                          constrained_layout=True, sharex=True)

axarr[0].plot(t_station, Orientation_station, label='Raw data')
axarr[0].plot(Data[station]['time'], Data[station]['Orientation_station'], label='Binned data')
#
axarr[1].plot(t_station, U_station, label='Raw data')
axarr[1].plot(Data[station]['time'], Data[station]['U_station'], label='1hr-averaged data')
#
axarr[0].set_ylabel(r'Wind orientation, $\theta~[^{\circ}]$')
axarr[0].set_ylim(0, 360)
axarr[0].set_yticks([0, 90, 180, 270, 360])
axarr[1].set_ylabel(r'Wind velocity at 2.6 m, $[\textup{m}~\textup{s}^{-1}]$')
axarr[1].set_ylim(bottom=0)
axarr[1].set_xlim(tmin, tmax)
axarr[1].set_xlabel(r'Days in June 2017')
myFmt = mdates.DateFormatter('%d')
axarr[1].xaxis.set_major_formatter(myFmt)
plt.legend(loc='upper center')

# subplots labels
axarr[0].text(0.015, 0.93, r'\textbf{a}', ha='left', va='center', transform=axarr[0].transAxes)
axarr[1].text(0.015, 0.93, r'\textbf{b}', ha='left', va='center', transform=axarr[1].transAxes)

plt.savefig(os.path.join(path_savefig, 'Figure2_supp.pdf'))
plt.show()