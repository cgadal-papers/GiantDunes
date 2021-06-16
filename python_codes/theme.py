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

#  Better to define these in the style.mplstyle file

# %%
# Callable parameters
# -------------------------------------

# #### font properties
fontsize_small = 9
fontsize_usual = matplotlib.rcParams['font.size']

# #### figure sizes
text_width = 426.79  # en pt
fig_width = text_width*0.35136*0.1  # en cm
fig_width = fig_width*0.39  # inches
fig_width_small = 0.75*fig_width


# #### line widths
linewidth_small = 0.8
linewidth_contourplot = 0.5
linewidth_barscale = 2
linewidth_errorbar = 0.8

# #### marker sizes
markersize = 5
markersize_small = 2

# #### colormaps
diverging_cmap = cmocean.cm.tarn
