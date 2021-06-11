import matplotlib.pyplot as plt
from windrose import WindroseAxes
import python_codes.theme as theme
import numpy as np


def plot_wind_rose(theta, U, bins, ax, fig, label):
    """Plot a wind rose from one dimensional time series.

    Parameters
    ----------
    theta : array_like
        Wind orientation in the trigonometric convention.
    U : array_like
        Wind velocity, same shape as `theta`.
    bins : list
        Velocity bin edges.
    ax : matplotlib.axes
        ax of the figure on which the wind rose is plotted.
    fig : matplotlib.figure
        figure on which the wind rose is plotted
    label : str
        label plotted below the wind rose.

    Returns
    -------
    WindroseAxes
        return the axe on which the wind rose is plotted. Can be used for further modifications.

    """
    props = dict(boxstyle='round', facecolor=(1, 1, 1, 0.9), edgecolor=(1, 1, 1, 1), pad=0)
    ax_rose = WindroseAxes.from_ax(fig=fig)
    ax_rose.set_position(ax.get_position(), which='both')
    Angle = (90 - theta) % 360
    ax_rose.bar(Angle, U, bins=bins, normed=True, zorder=20, opening=1, edgecolor=None,
                linewidth=0.5, nsector=60, cmap=plt.cm.viridis)
    ax_rose.grid(True, linewidth=0.4, color=theme.wind_grid_color, linestyle='--')
    ax_rose.patch.set_alpha(0.6)
    ax_rose.set_axisbelow(True)
    ax_rose.set_yticks([])
    ax_rose.set_xticklabels([])
    ax_rose.set_yticklabels([])
    fig.text(0.5, 0.05, label, ha='center', va='center', transform=ax.transAxes, bbox=props)
    ax.remove()
    return ax_rose


def plot_scatter_surrounded(x, y, color, alpha):
    """Plot a scatter plot with a black thin line surrounding point clusters.

    Parameters
    ----------
    x : array_like
        `x` vector.
    y : array_like
        `x` vector, same shape as `y`.
    color : str
        color passed to `plt.scatter`.
    alpha : float
        alpha passed to `plt.scatter`.

    Returns
    -------
    None
        Nothing, it just updates the plot.

    """
    plt.scatter(x % 360, y % 360, s=5, color='0.0', lw=0.5, rasterized=True)
    plt.scatter(x % 360, y % 360, s=5, color='1.0', lw=0, rasterized=True)
    plt.scatter(x % 360, y % 360, s=3, color=color, lw=0, alpha=alpha, rasterized=True)


def log_tick_formatter(val, pos=None):
    return f"$10^{{{int(val)}}}$"


def rgba_to_rgb(color):
    """Convert a RGBA color to RGB taking transparency into account. From https://stackoverflow.com/a/52101597/9530017.

    Parameters
    ----------
    color : np.array, shape (N, 4)
        RGBA color array.

    Returns
    -------
    np.array, shape (N, 3)
        RGB color array.

    """
    white = np.array([1, 1, 1])
    alpha = color[..., -1]
    color = color[..., :-1]
    return alpha[:, None]*color + (1 - alpha[:, None])*white[None, :]
