"""
==============================
Preprocessing of the wind data
==============================

For each station, we follow these preprocessing steps:

    - put the wind direction in the trigonometric referential (counter clockwise, 0 in the WE-direction).
    - averaging of the in situ data in 1-hr bins centered on the time stamps of the Era5Land dataset.
    - filtering unusued data (NaNs, 0 velocity)


"""


import numpy as np
import os
from scipy.stats import binned_statistic
from datetime import datetime, timedelta
import sys
sys.path.append('../')
from python_codes.general import cosd, sind
import python_codes.theme as theme
#
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

theme.load_style()

# paths
path_savefig = '../static/output_data/figures/'
path_ouputdata = '../static/output_data/data/'
path_inputdata = '../static/input_data'

Stations = ['Adamax_Station', 'Deep_Sea_Station', 'Huab_Station', 'South_Namib_Station']

Data = {}

for station in Stations:
    Data[station] = {}
    ############################################################################
    # Loading data
    ############################################################################
    #
    # ###### Era5Land wind data
    path_Era5_land = os.path.join(path_inputdata, station, 'Era5Land_wind_data_' + station + '.npy')
    Data_era = np.load(path_Era5_land, allow_pickle=True).item()
    #
    t_era = Data_era['time']
    U_era = np.sqrt(Data_era['Uwind']**2 + Data_era['Vwind']**2).squeeze()
    Orientation_era = (np.arctan2(Data_era['Vwind'], Data_era['Uwind'])*180/np.pi).squeeze() % 360
    # ###### in situ wind data
    path_insitu = os.path.join(path_inputdata, station, 'in_situ_wind_data_' + station + '.npy')
    Data_insitu = np.load(path_insitu, allow_pickle=True).item()
    #
    t_station = Data_insitu['time']
    U_station = Data_insitu['velocity']
    # putting angles in trigo. ref.
    Orientation_station = (270 - Data_insitu['direction']) % 360
    #
    ############################################################################
    # Averaging in situ data over 1hr
    ############################################################################
    dt = timedelta(minutes=60)  # bin size for averaging
    tmin, tmax = t_era[0].replace(minute=0), t_era[-1].replace(minute=50)
    t_station_hourly = np.arange(tmin - dt/2, tmax + dt/2, dt).astype(datetime)  # centered on Era5Land time steps
    # #### Using number of seconds from tmin for averaging function
    diff_time_seconds = [i.total_seconds() for i in (t_station - tmin)]
    bins_seconds = [i.total_seconds() for i in (t_station_hourly - tmin)]
    #
    # #### Averaging into bins
    U_av, bin_edges, _ = binned_statistic(diff_time_seconds, [U_station*cosd(Orientation_station), U_station*sind(Orientation_station)],
                                          bins=bins_seconds, statistic=np.nanmean)
    #
    Orientation_av = (np.arctan2(U_av[1, :], U_av[0, :])*180/np.pi) % 360  # orientation time series
    U_av = np.linalg.norm(U_av, axis=0)  # velocity time series
    bin_centered = bin_edges[1:] - (bin_edges[1] - bin_edges[0])/2
    t_station_avg = tmin + np.array([timedelta(seconds=i) for i in bin_centered])
    # Note: at this point, the in situ data are mapped on the ERA5 time steps, with a lot of NaNs where there was no in situ data.
    #
    ############################################################################
    # Filtering unusued data (NaNs, 0 velocity)
    ############################################################################
    mask = (~ (np.isnan(U_av) | np.isnan(Orientation_av))) & (U_av > 0)
    #
    # #### Storing data into dictionnary
    Data[station]['U_station'] = U_av[mask]
    Data[station]['Orientation_station'] = Orientation_av[mask]
    Data[station]['time'] = t_station_avg[mask]
    #
    Data[station]['U_era'] = U_era[mask]
    Data[station]['Orientation_era'] = Orientation_era[mask]
    # check that time periods agrees
    ############################################################################
    # If available, do the same for the meteorological data from Era5
    ############################################################################
    if station in ['South_Namib_Station', 'Deep_Sea_Station']:
        # BLH
        path_Era5_land = os.path.join(path_inputdata, station, 'Era5_BLH_' + station + '.npy')
        Data_BLH = np.load(path_Era5_land, allow_pickle=True).item()
        Data[station]['Boundary layer height'] = Data_BLH['Boundary layer height'][mask]
        # Pressure level data
        path_Era5_land = os.path.join(path_inputdata, station, 'Era5_level_' + station + '.npy')
        Data_level = np.load(path_Era5_land, allow_pickle=True).item()
        Data[station]['Pressure levels'] = Data_level['Pressure levels']
        inds_mask = np.arange(t_era.size)[mask]
        for key in Data_level.keys():
            if key not in ['time', 'Pressure levels']:
                Data[station][key] = Data_level[key][..., inds_mask]

path_save = os.path.join(path_ouputdata, 'Data_preprocessed.npy')
np.save(path_save, Data)