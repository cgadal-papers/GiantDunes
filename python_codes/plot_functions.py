import numpy as np
import matplotlib.path as path
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from windrose import WindroseAxes
from scipy.stats import binned_statistic_2d


def plot_wind_rose(theta, U, bins, ax, fig, label=None,
                   props=dict(boxstyle='round', facecolor=(1, 1, 1, 0.9), edgecolor=(1, 1, 1, 1), pad=0),
                   **kwargs):
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
    label : str or None
        if not None, label plotted below the wind rose (default is None).
    **kwargs :
        Optional parameters passed to :func:`windrose.WindroseAxes.bar <windrose.WindroseAxes>`.

    Returns
    -------
    WindroseAxes
        return the axe on which the wind rose is plotted. Can be used for further modifications.

    """
    # changing ax to have to have the windrose projection
    subplotspec = ax.get_subplotspec()
    ax.remove()
    ax_rose = fig.add_subplot(subplotspec, projection='windrose')
    Angle = (90 - theta) % 360
    ax_rose.bar(Angle, U, bins=bins, normed=True, zorder=20, opening=1, edgecolor=None,
                linewidth=0.5, nsector=60, **kwargs)
    ax_rose.grid(True, linewidth=0.4, color='k', linestyle='--')
    ax_rose.patch.set_alpha(0.6)
    ax_rose.set_axisbelow(True)
    ax_rose.set_yticks([])
    ax_rose.set_xticklabels([])
    ax_rose.set_yticklabels([])
    if label is not None:
        fig.text(0.5, 0.05, label, ha='center', va='center', transform=ax.transAxes, bbox=props)
    return ax_rose


def plot_flux_rose(angles, distribution, ax, fig, nbins=20, withaxe=0, label=None,
                   props=dict(boxstyle='round', facecolor=(1, 1, 1, 0.9), edgecolor=(1, 1, 1, 1), pad=0),
                   **kwargs):
    """Short summary.

    Parameters
    ----------
    angles : array_like
        bin center in orientation of the flux distribution.
    distributions : array_like
        angular flux distribution.
    ax : matplotlib.axes
        ax of the figure on which the wind rose is plotted.
    fig : matplotlib.figure
        figure on which the wind rose is plotted.
    nbins : int
        number of angular bins for the plot (the default is 20).
    withaxe : 0 or 1
        Define if the polar axes are plotted or not (the default is 0).
    label : str
        If not None, sets a label at the bottom of the flux rose (the default is None).
    **kwargs :
        Optional parameters passed to :func:`windrose.WindroseAxes.bar <windrose.WindroseAxes>`.

    Returns
    -------
    WindroseAxes
        return the axe on which the wind rose is plotted. Can be used for further modifications.

    """

    PdfQ = distribution/np.nansum(distribution)  # normalization
    # creating the new pdf with the number of bins
    Lbin = 360/nbins
    Bins = np.arange(0, 360, Lbin)
    Qdat = []
    Qangle = []
    precision_flux = 0.001

    for n in range(len(Bins)):
        ind = np.argwhere((angles >= Bins[n] - Lbin/2) & (angles < Bins[n] + Lbin/2))
        integral = int(np.nansum(PdfQ[ind])/precision_flux)
        for i in range(integral):
            Qangle.append(Bins[n])
            Qdat.append(1)
    Qangle = np.array(Qangle)
    # #### making the plot
    ax_rose = WindroseAxes.from_ax(fig=fig)
    ax_rose.set_position(ax.get_position(), which='both')
    # bars = ax.bar(Angle, Intensity, normed=True, opening=1, edgecolor='k', nsector = Nsector, bins = Nbin, cmap = cmap)
    Qangle = (90 - Qangle) % 360
    if Qangle.size != 0:
        _ = ax_rose.bar(Qangle, Qdat, nsector=nbins, **kwargs)
        ax_rose.set_rmin(0)
        ax_rose.plot(0, 0, '.', color='w', zorder=100, markersize=3)
        # ax_rose.set_yticklabels(['{:.1f}'.format(float(i.get_text())*precision_flux) for i in ax.get_yticklabels()])
        if withaxe != 1:
            ax_rose.set_yticks([])
    if label is not None:
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
    color : str or array_like
        color passed to `c` argument of `plt.scatter`.
    alpha : float
        alpha passed to `plt.scatter`.

    Returns
    -------
    None
        Nothing, it just updates the plot.

    """
    plt.scatter(x % 360, y % 360, s=5, c='0.0', lw=0.5, rasterized=True)
    plt.scatter(x % 360, y % 360, s=5, c='1.0', lw=0, rasterized=True)
    plt.scatter(x % 360, y % 360, s=3, c=color, lw=0, alpha=alpha, rasterized=True)


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


def plot_regime_diagram(ax, quantity, vars, lims, xlabel, ylabel, type='scatter', bins=None, **kwargs):
    x_var, y_var = vars[0], vars[1]
    ax.set_xscale('log')
    ax.set_yscale('log')
    #
    if type == 'binned':
        x_bin, y_bin = bins[0], bins[1]
        # #### binning data
        average, x_edge, y_edge, _ = binned_statistic_2d(x_var, y_var, quantity, statistic='mean', bins=[x_bin, y_bin])
        #
        # #### making plot
        a = ax.pcolormesh(x_edge, y_edge, average.T, snap=True, **kwargs)
    elif type == 'scatter':
        a = ax.scatter(x_var, y_var, s=5, c=quantity, lw=0, rasterized=True, **kwargs)
    #
    ax.set_xlim(lims[0])
    ax.set_ylim(lims[1])
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xticklabels([])
    #
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    else:
        ax.set_yticklabels([])
    return a


def make_nice_histogram(data, nbins, ax, vmin=None, vmax=None, scale_bins='lin', density=True, orientation='vertical', **kwargs):
    min = np.nanmin(data) if vmin is None else vmin
    max = np.nanmax(data) if vmax is None else vmax
    if scale_bins == 'log':
        bins = np.logspace(np.log10(min), np.log10(max), nbins)
        if orientation == 'vertical':
            ax.set_xscale('log')
        else:
            ax.set_yscale('log')
    else:
        bins = np.linspace(min, max, nbins)
    a = ax.hist(data, bins=bins, histtype='stepfilled',
                density=density, orientation=orientation, **kwargs)
    ax.hist(data, bins=bins, histtype='step',
            color=a[-1][0].get_fc(), density=density, orientation=orientation)


def plot_arrow(ax, start, end, arrowprops):
    """Plot an arrow using matplotlib :func:`FancyArrowPatch <matplotlib.patch.FancyArrowPatch>`. Note that it can plot dashed arrows without having an ugly head depending on `type` argument, following https://stackoverflow.com/questions/47180328/pyplot-dotted-line-with-fancyarrowpatch.

    Parameters
    ----------
    ax : matplotlib axe
        Axe on which to plot the arrow
    start : tuple, list, numpy array
        starting coordinates of the arrow
    end : tuple, list, numpy array
        starting coordinates of the arrow
    arrowprops : dict
        `arrowprops` dictionnary passed to matplotlib :func:`FancyArrowPatch <matplotlib.patch.FancyArrowPatch>`.

    Returns
    -------

        Return nothing, only plot the arrow

    """
    arrow = ptch.FancyArrowPatch(end, start, **arrowprops)
    ax.add_patch(arrow)
    if arrow.get_linestyle() != '-':
        # Tail
        v1 = arrow.get_path().vertices[0:3, :]
        c1 = arrow.get_path().codes[0:3]
        p1 = path.Path(v1, c1)
        pp1 = ptch.PathPatch(p1, color=arrow.get_facecolor(), lw=arrow.get_linewidth(), linestyle=arrow.get_linestyle(), fill=False)
        ax.add_patch(pp1)
        # Heads ====> partie qui ne marche pas
        v2 = arrow.get_path().vertices[3:, :]
        c2 = arrow.get_path().codes[3:]
        c2[0] = 1
        p2 = path.Path(v2, c2)
        pp2 = ptch.PathPatch(p2, color=arrow.get_facecolor(), lw=arrow.get_linewidth(), linestyle='-')
        ax.add_patch(pp2)
        arrow.remove()


def north_arrow(ax, center, length, length_small=None, width=None, radius=None,
                theta=0, textcolor='k', transform=None, **kwargs):
    """Plot a arrow indicating the North on a figure.

    Parameters
    ----------
    ax : matplotlib axe
        Axe on which to plot the arrow
    center : list, tuple, np.array
        Position of the arrow
    length : float
        arrow max length
    length_small : float
        length of the center par tof the arrow (the default is 0.8*length).
    width : float
        arrow width (the default is (3/7)*length).
    radius : float
        distance between the text and the arrow (the default is (45/70)*length).
    theta : float
        rotation of the arrow indicating the north (the default is 0 for an arrow pointing upward).
    textcolor : str
        color of the text (the default is 'k').
    transform : matplotlib transform
        transform for the coordinate systen of the input length and positions (the default is ax.transData).
    **kwargs :
        Optional parameters passed to :func:`Polygon <matplotlib.patch.Polygon>`, used to customize the arrow.

    Returns
    -------
    None
        return nothing

    """
    if transform is None:
        transform = ax.transData
    if length_small is None:
        length_small = 0.8*length
    if width is None:
        width = (3/7)*length
    if radius is None:
        radius = (45/70)*length
    y_start = radius + length - length_small
    arrow = np.array([[0, y_start], [width/2, radius],
                      [0, radius + length], [-width/2, radius], [0, y_start]])
    # barycentre = np.sum(arrow, axis=0)/arrow.shape[0]
    # arrow = np.dot(Rotation_matrix(theta), (arrow-barycentre).T).T + barycentre
    r = np.array(((np.cos(theta), -np.sin(theta)),
                  (np.sin(theta),  np.cos(theta))))
    arrow = np.dot(r, arrow.T).T
    arrow = arrow + np.array(center)
    #
    ax.add_patch(ptch.Polygon(arrow, transform=transform, **kwargs))
    ax.text(center[0], center[1], r'\textbf{N}', transform=transform,
            ha='center', va='center')
