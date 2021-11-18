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


r"""
Sediment transport laws. Here, sediment fluxes are made non dimensional
by the characteristic flux :math:`Q = \sqrt{\displaystyle\frac{(\rho_{\rm p} - \rho_{\rm f}) g d}{\rho_{\rm f}}}d`.

"""


def quadratic_transport_law(theta, theta_d, omega):
    r"""Quadratic transport law :math:`q_{\rm sat}/Q = \Omega \sqrt{\theta_{\rm th}}(\theta - \theta_{\rm th})`, from Duràn et al. 2011.

    Parameters
    ----------
    theta : scalar, numpy array
        Shield number.
    theta_d : scalar, numpy array
        Threshold Shield number.
    omega : scalar, numpy array
        Prefactor of the transport law.

    Returns
    -------
    scalar, numpy array
        Sediment fluxes calculated elementwise using the quadratic transport law.

    Examples
    --------
    >>> import numpy as np
    >>> theta = np.random.random((2000, ))
    >>> theta_d, omega = 0.0053, 7.8
    >>> qsat = quadratic_transport_law(theta, theta_d, omega)

    References
    --------
    [1] Durán, O., Claudin, P., & Andreotti, B. (2011). On aeolian transport: Grain-scale interactions,
    dynamical mechanisms and scaling laws. Aeolian Research, 3(3), 243-270.

    """
    return np.piecewise(theta, [theta > theta_d, theta <= theta_d],
                        [lambda theta: omega*np.sqrt(theta_d)*(theta - theta_d), lambda theta: 0])


def quartic_transport_law(theta, theta_d, Kappa=0.4, mu=0.63, cm=1.7):
    r"""Quartic transport law :math:`q_{\rm sat}/Q = \frac{2\sqrt{\theta_{\rm th}}}{\kappa\mu}(\theta - \theta_{\rm th})\left[1 + \frac{C_{\rm M}}{\mu}(\theta - \theta_{\rm th})\right]` from Pähtz et al. 2020.

    Parameters
    ----------
    theta : scalar, numpy array
        Shield number.
    theta_d : scalar, numpy array
        Threshold Shield number.
    Kappa : scalar, numpy array
        von Kármán constant (the default is 0.4).
    mu : scalar, numpy array
        Friction coefficient (the default is 0.63).
    cm : scalar, numpy array
        Transport law coefficient (the default is 1.7).

    Returns
    -------
    scalar, numpy array
        Sediment fluxes calculated elementwise using the quartic transport law.

    Examples
    --------
    >>> import numpy as np
    >>> theta = np.random.random((2000, ))
    >>> theta_d = 0.0035
    >>> qsat = quartic_transport_law(theta, theta_d)

    References
    --------
    [1] Pähtz, T., & Durán, O. (2020). Unification of aeolian and fluvial sediment transport rate from granular physics. Physical review letters, 124(16), 168001.

    """
    return np.piecewise(theta, [theta > theta_d, theta <= theta_d],
                        [lambda theta: (2/(Kappa*mu))*np.sqrt(theta_d)*(theta - theta_d)*(1 + (cm/mu)*(theta - theta_d)), lambda theta: 0])
