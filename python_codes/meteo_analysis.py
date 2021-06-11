import numpy as np
from scipy.stats import binned_statistic_2d
from python_codes.general import cosd, sind


def compute_circadian_annual_cycle(theta, U, time):
    """Average the wind data into bins of 'time of day' and 'day of year'.

    Parameters
    ----------
    theta : array_like
        wind orientation in degrees.
    U : array_like
        wind velocity, same shape as `theta`.
    time : array_like
        numpy array of `datetime.datetime` objects, same shape as `theta`.

    Returns
    -------
    np.array, shape (366, 24)
        the wind orientation averaged into bins of 'time of day' and 'day of year'.
    np.array, shape (366, 24)
        the wind velocity averaged into bins of 'time of day' and 'day of year'.
    np.array, shape (366,)
        the days corresponding to the first dimension of the averaged two dimensional arrays.
    np.array, shape (24,)
        the hours corresponding to the first dimension of the averaged two dimensional arrays.

    """
    days = np.array([i.timetuple().tm_yday for i in time])
    hours = np.array([i.hour for i in time])
    possible_days = np.array(sorted(set(days)))[::3]
    possible_hours = np.array(sorted(set(hours)))
    #
    days_bins = np.append(possible_days, 2*possible_days[-1] - possible_days[-2])
    hours_bin = np.append(possible_hours, 2*possible_hours[-1] - possible_hours[-2])
    #
    Ux_av, _, _, _ = binned_statistic_2d(days, hours, U*cosd(theta), bins=[days_bins, hours_bin], statistic=np.nanmean)
    Uy_av, _, _, _ = binned_statistic_2d(days, hours, U*sind(theta), bins=[days_bins, hours_bin], statistic=np.nanmean)
    #
    U_binned = np.sqrt(Ux_av**2 + Uy_av**2)
    Orientation_binned = (np.arctan2(Uy_av, Ux_av)*180/np.pi) % 360
    return Orientation_binned, U_binned, possible_days, possible_hours


def mu(z, z0, Kappa=0.4):
    r""" Calculate the ratio :math:`U(z)/u_{*}` following the law of the wall:

    ..:math::

        \frac{U(z)}{u_{*}} = \frac{1}{\kappa}\log\left(1 +\frac{z}{z_{0}}\right).

    Parameters
    ----------
    z : array_like
        height
    z0 : array_like
        hydrodyamic roughness
    Kappa : float, optional
        Von Karman constant (the default is 0.4).

    Returns
    -------
    array_like
        return the ratio :math:`U(z)/u_{*}` following the law of the wall.

    """

    return (1/Kappa)*np.log(1 + z/z0)
