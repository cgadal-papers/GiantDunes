r"""
Dune growth mechanism theory developped by Courrech du Pont et al. 2014.

References
----------
[1] Courrech du Pont, S., Narteau, C., & Gao, X. (2014). Two modes for dune orientation. Geology, 42(9), 743-746.
"""

# Note that it is here derived is the fixed referential math:`(x,y)`
# used by Gadal et al. 2019. The dune orientation math:`\alpha` is then calculated with respect to the `y`-axis.
# [2] Gadal, C., Narteau, C., Du Pont, S. C., Rozier, O., & Claudin, P. (2019). Incipient bedforms in a bidirectional wind regime. Journal of Fluid Mechanics, 862, 490-516.

import numpy as np
from python_codes.general import Vector_average, cosd, sind


############################################################################
########################### Fluxes at the crest ############################
############################################################################


def Flux_at_crest(alpha, theta, Q0, gamma=1.6):
    r"""Calculation of the sand flux at the dune crest:

    .. math::

        Q_{\rm crest} = Q_{0}\left[1 + \gamma\sin\vert\theta-\alpha\vert\right]

    Parameters
    ----------
    alpha : scalar, numpy array
        Dune orientation :math:`\alpha`.
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).

    Returns
    -------
    scalar, numpy array
        Flux at the dune crest :math:`Q_{\rm crest}`

    Examples
    --------
    >>> import numpy as np
    >>> alpha = 10
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Qcrest = Flux_at_crest(alpha, theta, Q0)

    """
    return theta, Q0*(1 + gamma*np.abs(sind(theta - alpha)))


def Resultant_flux_at_crest(alpha, theta, Q0, gamma=1.6, **kwargs):
    r"""Resultant flux (i.e vectorial average) of the sand flux at the crest.

    Parameters
    ----------
    alpha : scalar, numpy array
        Dune orientation :math:`\alpha`.
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).
    **kwargs :
        `kwargs` are passed to :func:`Vector_average <PyDune.General.Vector_average>`.

    Returns
    -------
    list of scalars, numpy arrays
        A list containing the orientation and the magnitude of the resultant sand flux at the crest.

    Examples
    --------
    >>> import numpy as np
    >>> alpha = 10
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Qcrest = Resultant_flux_at_crest(alpha, theta, Q0)

    """
    th_crest, N_crest = Flux_at_crest(alpha, theta, Q0, gamma=gamma)
    return Vector_average(th_crest, N_crest, **kwargs)

# def Resultant_flux_aligned_crest(alpha, gamma, theta, Q0):
#     RDD, RDP = Flux_at_crest(alpha, gamma, theta, Q0)
#     alpha = np.expand_dims(alpha, tuple(np.arange(1, len(theta.shape))))
#     return RDP*(cosd(alpha)*cosd(RDD) + sind(alpha)*sind(RDD))


def Resultant_flux_perp_crest_at_crest(alpha, theta, Q0, gamma=1.6, axis=-1):
    r"""Component of the resultant flux (i.e vectorial average) at the crest perpendicular to the dune crest.

    Parameters
    ----------
    alpha : scalar, numpy array
        Dune orientation :math:`\alpha`.
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).
    axis : int
        axis over wich the average is done (the default is -1).

    Returns
    -------
    list of scalars, numpy arrays
        A list containing the orientation and the magnitude of the resultant sand flux at the crest.

    Examples
    --------
    >>> import numpy as np
    >>> alpha = 10
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Qcrest_perp = Resultant_flux_perp_crest_at_crest(alpha, theta, Q0)

    """
    RDD, RDP = Resultant_flux_at_crest(alpha, theta, Q0, gamma=gamma, axis=axis)
    alpha_squeezed = np.squeeze(alpha, axis=axis)
    return RDP*(cosd(alpha_squeezed + 90)*cosd(RDD) + sind(alpha_squeezed + 90)*sind(RDD))


def Elongation_direction(theta, Q0, gamma=1.6, alpha_bins=np.linspace(0, 360, 361), axis=-1, **kwargs):
    r"""Calculate the elongation direction as the dune orientation for wich the components of the resultant sand flux at the dune crest
    perpendicular to the dune crest cancel each other out.

    Parameters
    ----------
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).
    alpha_bins : numpy array
        Bins in dune orientation used to calculate the resultant flux at the crest (the default is np.linspace(0, 360, 361)).
    **kwargs :
        `kwargs` are optional parameters passed to :func:`CourrechDuPont2014.Resultant_flux_perp_crest_at_crest <PyDune.Physics.Dune.CourrechDuPont2014.Resultant_flux_perp_crest_at_crest>`.

    Returns
    -------
    scalar, numpy array
        The elongation direction predicted from the model of Courrech du Pont et al. corresponding to the input sand flux distributions.

    Examples
    --------
    >>> import numpy as np
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Alpha_F = Elongation_direction(theta, Q0)

    References
    ----------
    [1] Courrech du Pont, S., Narteau, C., & Gao, X. (2014). Two modes for dune orientation. Geology, 42(9), 743-746.
    """

    # Matching dimensions
    alpha_expanded = np.expand_dims(alpha_bins, tuple(np.arange(1, len(theta.shape) + 1)))
    th_expanded, N_expanded, gamma_expended = np.expand_dims(theta, 0), np.expand_dims(Q0, 0), np.expand_dims(gamma, 0)
    #
    Alpha_F = alpha_bins[np.argmin(np.abs(Resultant_flux_perp_crest_at_crest(alpha_expanded, th_expanded, N_expanded, gamma=gamma_expended, axis=axis, **kwargs)), axis=0)]
    del alpha_expanded, th_expanded, N_expanded
    RDD, _ = Vector_average(theta, Q0)  # wind resultant angle
    #
    prod = cosd(Alpha_F)*cosd(RDD) + sind(Alpha_F)*sind(RDD)  # check that the orientation goes in the right drirection
    del RDD
    return np.mod(np.where(prod > 0, Alpha_F, Alpha_F + 180), 360)


def Growth_rate(alpha, theta, Q0, gamma=1.6, axis=-1, capture_rate=1):
    r"""Calculate the dune growth rate using the dimensional analysis from Courrech du Pont et al. 2014.

    Parameters
    ----------
    alpha : scalar, numpy array
        Dune orientation :math:`\alpha`.
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).
    axis : int
        axis over wich the average is done (the default is -1).
    capture_rate : function, scalar, numpy array
        Capture rate of the avalanche slope. Can either be a scalar, a numpy array with dimensions corresponding to `alpha`, `theta` and `Q0`,
         or function taking as argument `alpha`, `theta` and `Q0`, in this order (the default is 1).

    Returns
    -------
    scalar, numpy array
        Dune growth rate corresponding to input sand flux distributions.

    Examples
    --------
    >>> import numpy as np
    >>> alpha = 10
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Qcrest_perp = Growth_rate_courrech(alpha, theta, Q0)

    References
    ----------
    [1] Courrech du Pont, S., Narteau, C., & Gao, X. (2014). Two modes for dune orientation. Geology, 42(9), 743-746.
    """
    if callable(capture_rate):
        CR = capture_rate(alpha, theta, Q0)
    else:
        CR = capture_rate

    return np.squeeze(np.sum(CR*Q0*(np.abs(sind(theta - alpha)) + gamma*sind(theta-alpha)**2), axis=axis))


def Bed_Instability_Orientation(theta, Q0, gamma=1.6, alpha_bins=np.linspace(0, 360, 361), **kwargs):
    r"""Calculate the dune orientation growing from the flat bed instability as the maximum of the dimensional growth rate calculated in Courrech du Pont at al. 2014.

    Parameters
    ----------
    theta : scalar, numpy array
        Flux orientation :math:`\theta` in degrees.
    Q0 : scalar, numpy array
        Flux at the bottom of the dune :math:`Q_{0}`.
    gamma : scalar, numpy array
        Flux-up ratio :math:`\gamma` (the default is 1.6).
    alpha_bins : numpy array
        Bins in dune orientation used to calculate the resultant flux at the crest (the default is np.linspace(0, 360, 361)).
    **kwargs :
        `kwargs` are optional parameters passed to :func:`CourrechDuPont2014.Growth_rate <PyDune.Physics.Dune.CourrechDuPont2014.Growth_rate>`.

    Returns
    -------
    scalar, numpy array
        The dune orientation predicted from the model of Courrech du Pont et al. corresponding to the input sand flux distributions.

    Examples
    --------
    >>> import numpy as np
    >>> theta = np.random.random((1000,))*360
    >>> Q0 = np.random.random((1000,))*50
    >>> Alpha_F = Bed_Instability_Orientation(theta, Q0)

    References
    ----------
    [1] Courrech du Pont, S., Narteau, C., & Gao, X. (2014). Two modes for dune orientation. Geology, 42(9), 743-746.
    """

    # Matching dimensions
    alpha_expanded = np.expand_dims(alpha_bins, tuple(np.arange(1, len(theta.shape) + 1)))
    th_expanded, N_expanded, gamma_expended = np.expand_dims(theta, 0), np.expand_dims(Q0, 0), np.expand_dims(gamma, 0)
    #
    G_rate = Growth_rate(alpha_expanded, th_expanded, N_expanded, gamma=gamma_expended, **kwargs)
    return np.mod(alpha_bins[G_rate.argmax(0)], 180)
