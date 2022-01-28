"""
============
Figure 1
============

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import sys
import os
from PIL import Image
sys.path.append('../')
import python_codes.theme as theme
from python_codes.plot_functions import plot_wind_rose

# Loading figure theme
theme.load_style()

# paths
path_imgs = '../static/images/'
path_savefig = '../Paper/Figures'
path_outputdata = '../static/processed_data'

# Loading wind data
Data = np.load(os.path.join(path_outputdata, 'Data_final.npy'), allow_pickle=True).item()
Stations = sorted(Data.keys())

# fig properties
bins = [0.03, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
labels = ['Adamax', 'Huab', 'Deep Sea', 'South Namib']
coords_stations = np.array([(-19.034111,  15.737194), (-20.874722,  13.642), (-24.125533,  15.049100), (-26.044083,  15.396972)])
scales = [1300, 1100, 1650, 2600]
bbox = dict(facecolor=(1, 1, 1, 0.5), edgecolor=(1, 1, 1, 0))
bbox2 = dict(facecolor=(1, 1, 1, 0.5), edgecolor=(1, 1, 1, 0), pad=0.25)
numbering = [r'\textbf{a}', r'\textbf{b}', r'\textbf{c}', r'\textbf{d}', r'\textbf{e}']
coords_station_pix = [(1141, 544), (881, 554), (755, 430), (772, 550)]

# #### Figure
fig = plt.figure(figsize=(theme.fig_width, 0.6*theme.fig_height_max))
gs = gridspec.GridSpec(2, 2, height_ratios=[2.5, 1], width_ratios=[0.78, 1], figure=fig)
gs.update(left=0, right=0.99, bottom=0.001, top=0.999, wspace=0.27, hspace=0)

# map
ax0 = fig.add_subplot(gs[0, 0])
Map = np.array(Image.open(os.path.join(path_imgs, 'Map.png')))
ax0.imshow(Map[:-104, 642:-791], extent=[12.55, 17.38, -27.27, -18.2])
ax0.set_xlabel(r'Longitude~[$^\circ$]')
ax0.set_ylabel(r'Latitude~[$^\circ$]')
ax0.yaxis.set_label_position('right')
ax0.yaxis.tick_right()
ax0.text(0.005, 0.998, numbering[0], transform=ax0.transAxes, ha='left', va='top', color='k', bbox=bbox2)
#
plt.scatter(coords_stations[:, 1], coords_stations[:, 0], s=25, color=theme.color_station_position)
for point, txt in zip(coords_stations, labels):
    if txt != 'Huab':
        pad_x, pad_y = 0.05, -0.5
        plt.gca().annotate(r'\textbf{' + txt + '}', (point[1] + pad_x, point[0] + pad_y), ha='right', va='bottom', color='k', bbox=bbox2)
    else:
        pad_x, pad_y = 0, -0.5
        plt.gca().annotate(r'\textbf{' + txt + '}', (point[1] + pad_x, point[0] + pad_y), ha='left', va='bottom', color='k', bbox=bbox2)

# right images
gs_sub = gs[:, -1].subgridspec(4, 1, height_ratios=[1, 1, 1, 1], hspace=0)
for i, station in enumerate(['Adamax_Station', 'Huab_Station', 'Deep_Sea_Station', 'South_Namib_Station']):
    ax = fig.add_subplot(gs_sub[i])
    img = np.array(Image.open(os.path.join(path_imgs, station[:-8] + '.png')))
    ax.imshow(img[:-104, :], zorder=-10)
    ax.set_xticks([])
    ax.set_yticks([])
    # labels
    ax.text(0.015, 0.08, r'\textbf{' + labels[i] + '}', transform=ax.transAxes, ha='left', va='center', bbox=bbox, zorder=-5)
    # scale bars
    backgrnd = Rectangle((0.75, 0), width=0.25, height=0.2, transform=ax.transAxes, facecolor='w', alpha=0.6, ec=None)
    ax.add_patch(backgrnd)
    txt = r'$' + str(scales[i]) + r'~\textup{m}$'
    scalebar = AnchoredSizeBar(ax.transData, 384, txt, 'lower right', color='k',
                               frameon=False, size_vertical=10, label_top=True, sep=1, pad=0.15)
    ax.add_artist(scalebar)

    # wind roses
    axins1 = ax.inset_axes([0, 0.45, 0.3, 0.5])
    plot_wind_rose(Data[station]['Orientation_era'], Data[station]['U_star_era'], bins,
                   axins1, fig, label=None, cmap=theme.cmap_wind)
    #
    axins1 = ax.inset_axes([0.7, 0.45, 0.3, 0.5])
    plot_wind_rose(Data[station]['Orientation_insitu'], Data[station]['U_star_insitu'], bins,
                   axins1, fig, label=None, cmap=theme.cmap_wind)
    #
    # labelling
    ax.text(0.005, 0.99, numbering[i+1], transform=ax.transAxes, ha='left', va='top', color='k', bbox=bbox2)
    # stations
    ax.scatter(coords_station_pix[i][0], coords_station_pix[i][1], s=25, color=theme.color_station_position)

# colorbar
# left, bottom, width, height = [ax0.get_position().x0, 0.15, 0.43, 0.025]
left, bottom, width, height = [0.025, 0.15, 0.43, 0.025]
ax_colorbar = fig.add_axes([left, bottom, width, height])

bounds = bins + [bins[-1] + bins[-1] - bins[-2]]
bounds[0] = 0
norm = BoundaryNorm(boundaries=bounds, ncolors=256)
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
cb = fig.colorbar(sm, cax=ax_colorbar, orientation='horizontal', ticks=bounds[::2])
cb.set_label(r'Wind shear velocity, $u_{*}~[\textrm{m}~\textrm{s}^{-1}]$')
labels = [item.get_text() for item in cb.ax.get_xticklabels()]
# labels[-1] = r'$\infty$'
# labels[0] = r'$0$'
# cb.ax.set_xticklabels(labels)

plt.savefig(os.path.join(path_savefig, 'Figure1.pdf'), dpi=600)
plt.show()
