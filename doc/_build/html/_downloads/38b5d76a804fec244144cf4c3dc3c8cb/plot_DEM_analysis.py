"""
===========
DEM analysis
===========

Analyzing DEMs to extract average orientation, wavelength and amplitude of the dune pattern.
"""


import numpy as np
from geopy import distance
import sys
sys.path.append('../')
from python_codes.general import cosd, sind
from python_codes.DEM_analysis import polyfit2d, periodicity_2d


def DEM_analysis(file):
    data = np.load(file, allow_pickle=True).item()
    # Removing large scale topo
    kx, ky = 2, 2
    LON, LAT = np.meshgrid(data['lon'], data['lat'])
    soln, residuals, rank, s = polyfit2d(LON, LAT, data['DEM'], kx=kx, ky=ky, order_max=2)
    fitted_surf = np.polynomial.polynomial.polyval2d(LON, LAT, soln.reshape((kx + 1, ky + 1)).T)
    # Calculating average conversion deg -> km
    x_km = np.array([distance.distance((data['lat'][0], i), (data['lat'][0], data['lon'][0]), ellipsoid='WGS-84').km for i in data['lon']])
    y_km = np.array([distance.distance((i, data['lon'][0]), (data['lat'][0], data['lon'][0]), ellipsoid='WGS-84').km for i in data['lat']])
    km_step = np.mean([np.diff(x_km).mean(), np.diff(y_km).mean()])
    return *periodicity_2d(data['DEM'] - fitted_surf, 40), data['DEM'] - fitted_surf, data['lon'], data['lat'], km_step


if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt
    import python_codes.theme as theme
    #
    theme.load_style()
    Stations = ['Deep_Sea_Station', 'South_Namib_Station']
    #
    path_data = 'input_data/'
    path_save = 'output_data/DEM_analysis/'
    if not os.path.isdir(path_save):
        os.mkdir(path_save)
    #
    for i, station in enumerate(Stations):
        file = os.path.join(path_data, station, 'DEM_' + station + '.npy')
        orientation, wavelength, amplitude, p0, p1, transect, C, topo, lon, lat, km_step = DEM_analysis(file)
        fig_width = theme.fig_width
        fig_height = 0.6*fig_width
        fig = plt.figure(figsize=(fig_width, fig_height), tight_layout=True)
        #
        plt.subplot(2, 2, 1)
        plt.contourf(lon, lat, topo, levels=50)
        plt.colorbar(label='$h$~[m]')
        plt.xlabel(r'longitude [$^{\circ}$]')
        plt.ylabel(r'latitude [$^{\circ}$]')
        plt.gca().set_aspect('equal')
        #
        plt.subplot(2, 2, 2)
        x = list(-(lon - lon[0])[::-1]) + list((lon - lon[0])[1:])
        y = list(-(lat - lat[0])[::-1]) + list((lat - lat[0])[1:])
        plt.contourf(x, y, C, levels=50)
        #
        plt.plot([x[p0[0]], x[int(round(p1[0]))]], [y[p0[1]], y[int(round(p1[1]))]], color='tab:red', label='profile for wavelength calculation')
        p11 = p0 + np.array([cosd(orientation), sind(orientation)])*min(topo.shape)
        p12 = p0 - np.array([cosd(orientation), sind(orientation)])*min(topo.shape)
        plt.plot([x[int(round(p11[0]))], x[int(round(p12[0]))]], [y[int(round(p11[1]))], y[int(round(p12[1]))]], color='k', label='orientation')
        plt.xlabel(r'longitude -- shift [$^{\circ}$]')
        plt.ylabel(r'latitude -- shift [$^{\circ}$]')
        # plt.legend()
        plt.gca().set_aspect('equal')
        #
        plt.subplot(2, 1, 2)
        x_transect = np.arange(transect.size)*km_step
        plt.plot(x_transect, transect, color='tab:red')
        plt.plot(x_transect[wavelength], transect[wavelength], color='tab:blue', marker='.')
        plt.xlabel('Distance along profile [km]')
        plt.ylabel('Autocorrelation~[m$^{2}$]')
        plt.xlim(0, x_transect.max())
        plt.savefig(path_save + 'Analysis_DEM_' + station + '.pdf')
        np.save(path_save + 'Analysis_DEM_' + station + '.npy', {'orientation': orientation, 'wavelength': x_transect[wavelength], 'amplitude': amplitude})
        print(station, r'orientation: ' + '{:.1f}'.format(orientation) + r' deg., wavelength: ' + r'{:.1f}'.format(x_transect[wavelength]) + r' km, amplitude: ' + r'{:.1f}'.format(amplitude) + r' m')
        if i == 1:
            plt.show()
        else:
            plt.close()
