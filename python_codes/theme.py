import matplotlib
import matplotlib.pyplot as plt
import cmocean
import os


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

#  Better to define these in the style.mplstyle file

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
cmap_delta_u = cmocean.cm.curl_r
cmap_delta_theta = 'plasma'
cmap_topo = cmocean.cm.turbid_r

# #### colors
color_dune_orientation = 'grey'
flux_color = matplotlib.colors.ListedColormap('navajowhite')
