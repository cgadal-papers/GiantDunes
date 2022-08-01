"""
Theme used by matplotlib for the paper figures
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mpcolors
import numpy as np
import cmocean
import cmasher as cmr
import os


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """Truncate a given colormap.

    Parameters
    ----------
    cmap : matplotlib colormap.
        Input colormap to be truncated.
    minval : float
        Where to start the wanted colormap, assuming that 0 is the start of the input colormap, and 1 its end (the default is 0.0).
    maxval : type
        Where to start the wanted colormap, assuming that 0 is the start of the input colormap, and 1 its end (the default is 0.0).
    n : type
        Description of parameter `n` (the default is 100).

    Returns
    -------
    type
        Description of returned object.

    """
    # from here: https://stackoverflow.com/a/18926541/9530017
    new_cmap = mpcolors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def load_style():
    """Function that load the matplolib style sheet.

    Examples
    --------
    >>> theme.load_style()

    """
    plt.style.use(os.path.join(os.path.dirname(__file__), '_static/style.mplstyle'))


# %%
# Default parameters (matplotlib.rcParams)
# -------------------------------------
load_style()


# %%
# Callable parameters
# -------------------------------------

# #### font properties
fontsize_small = 9
fontsize_usual = matplotlib.rcParams['font.size']

# #### figure sizes
mm_to_inch = 0.0393701
fig_width, fig_height = matplotlib.rcParams['figure.figsize']
fig_height_max = 195*mm_to_inch


# #### line widths
linewidth_barscale = 2

# #### marker sizes
markersize = 5
markersize_small = 2

# #### colormaps
cmap_delta_u = truncate_colormap(cmr.emergency_s_r, minval=0.05, maxval=1.0, n=256)
cmap_delta_theta = 'plasma'
cmap_topo = truncate_colormap(cmocean.cm.turbid_r, minval=0, maxval=0.8, n=256)
cmap_wind = truncate_colormap(plt.cm.viridis, 0.15, 1, 256)

# #### colors
color_dune_orientation = 'grey'
flux_color = matplotlib.colors.ListedColormap('navajowhite')
color_day = '#C3B632'
color_night = '#3D134F'
color_Era5Land = 'tab:orange'
color_Era5Land_sub = '#cc0000'
color_insitu = 'tab:blue'
color_insitu_sub = '#17becf'
color_station_position = 'black'
regime_line_color = 'tab:green'

# #### special Icons
Icon_day = r'\faSun'
Icon_night = r'\faMoon'
