"""
Linear theory of a turbulent flow over a sinusoidal bottom.
"""

import numpy as np
from scipy.integrate import solve_ivp
from python_codes.general import cosd, sind
from python_codes.meteo_analysis import mu

# %%
# Geometrical model
# -----------------
# Geometrical model for the scaling of the coefficient as the function of the orientation of the bottom perturbation


def Ax(alpha, A0):
    r"""Calculate the hydrodynamic coefficient :math:`\mathcal{A}_{x}` using the geometrical model:

    .. math::

        \mathcal{A}_{x} = \mathcal{A}_{0}\cos^{2}\alpha.

    Parameters
    ----------
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    A0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.

    Returns
    -------
    array, scalar
         the hydrodynamic coefficient.
    """
    return A0*cosd(alpha)**2


def Ay(alpha, A0):
    r"""Calculate the hydrodynamic coefficient :math:`\mathcal{A}_{y}` using the geometrical model:

    .. math::

        \mathcal{A}_{y} = 0.5\mathcal{A}_{0}\cos\alpha\sin\alpha.

    Parameters
    ----------
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    A0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.

    Returns
    -------
    array, scalar
         the hydrodynamic coefficient.
    """
    return A0*cosd(alpha)*sind(alpha)/2


def Bx(alpha, B0):
    r"""Calculate the hydrodynamic coefficient :math:`\mathcal{B}_{x}` using the geometrical model:

    .. math::

        \mathcal{B}_{x} = \mathcal{B}_{0}\cos^{2}\alpha.

    Parameters
    ----------
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    B0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.

    Returns
    -------
    array, scalar
         the hydrodynamic coefficient.
    """
    return B0*cosd(alpha)**2


def By(alpha, B0):
    r"""Calculate the hydrodynamic coefficient :math:`\mathcal{B}_{y}` using the geometrical model:

    .. math::

        \mathcal{B}_{y} = 0.5*\mathcal{B}_{0}\cos\alpha\sin\alpha

    Parameters
    ----------
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    B0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.

    Returns
    -------
    array, scalar
         the hydrodynamic coefficient.
    """
    return B0*cosd(alpha)*sind(alpha)/2


def Cisaillement_basal(x, y, alpha, A0, B0, AR):
    # for a cosine topography and a wind blowing along x-axis
    # adim: lenght by 1/K, shear by Tau_0
    # x = K*x
    # y = K*y
    # alpha: dune orientation
    # A0, B0: hydrydynamic coeff.
    # AR = K*xi0 avec xi0 amplitude en dim. of the cosine
    Taux = np.real(+ (1 + (Ax(alpha, A0) + 1j*Bx(alpha, B0))*AR*np.exp(1j*(cosd(alpha)*x + sind(alpha)*y))))
    Tauy = np.real(+ (Ay(alpha, A0) + 1j*By(alpha, B0))*AR*np.exp(1j*(cosd(alpha)*x + sind(alpha)*y)))
    return Taux, Tauy


# %%
# Convective boundary layer -- stratified free atmosphere model
# -----------------


def _mu_prime(eta, eta_0, Kappa=0.4):
    r""" derivative of the ratio :math:`U(z)/u_{*}` following the law of the wall:

    ..:math::

        \frac{1}{u_{*}}\frac{\textup{d}U(z)}{\textup{d}z} = \frac{1}{\kappa}\frac{1}{(z + z_{0}}.


    Parameters
    ----------
    eta : scalar, np.array
        height
    eta_0 : scalar, np.array
        hydrodyamic roughness
    Kappa : float, optional
        Von Karmàn constant (the default is 0.4).

    Returns
    -------
    scalar, np.array
        Array of the ratio defined above.


    """

    return (1/Kappa)*(1/(eta + eta_0))


def _P(eta, eta_H, eta_0, Kappa):
    """:math:`P` matrix.

    Parameters
    ----------
    eta : scalar, np.array
        Non dimensional height :math:`k z`.
    eta_H : scalar, np.array
        Non dimensional boundary layer height :math:`k H`.
    eta_0 : scalar, np.array
        Non dimensional hydrodyamic roughness :math:`k z_{0}`.
    Kappa : float
        Von Karmàn constant.

    Returns
    -------
    np.array
        The :math:`P` matrix built from the input parameters.

    """

    tp = (1 - eta/eta_H)
    #
    P1 = [0, -1j, _mu_prime(eta, eta_0, Kappa)/(2*tp), 0]
    P2 = [-1j, 0, 0, 0]
    P3 = [1j*mu(eta, eta_0, Kappa) + 4*tp/_mu_prime(eta, eta_0, Kappa), _mu_prime(eta, eta_0, Kappa), 0, 1j]
    P4 = [0, -1j*mu(eta, eta_0, Kappa), 1j, 0]
    #
    P = np.array([P1, P2, P3, P4])
    return P


def _S(eta, eta_H, eta_0, Kappa):
    """:math:`S` vector.

    Parameters
    ----------
    eta : scalar, np.array
        Non dimensional height :math:`k z`.
    eta_H : scalar, np.array
        Non dimensional boundary layer height :math:`k H`.
    eta_0 : scalar, np.array
        Non dimensional hydrodyamic roughness :math:`k z_{0}`.
    Kappa : float
        Von Karmàn constant.

    Returns
    -------
    np.array
        The :math:`S` vector built from the input parameters.

    """
    return np.array([Kappa*_mu_prime(eta, eta_0, Kappa)**2 - _mu_prime(eta, eta_0, Kappa)/(2*eta_H), 0, 0, 0])


def _S_delta(eta, eta_H, eta_0, Kappa):
    r""":math:`S_{\delta}` vector.

    Parameters
    ----------
    eta : scalar, np.array
        Non dimensional height :math:`k z`.
    eta_H : scalar, np.array
        Non dimensional boundary layer height :math:`k H`.
    eta_0 : scalar, np.array
        Non dimensional hydrodyamic roughness :math:`k z_{0}`.
    Kappa : float
        Von Karmàn constant.

    Returns
    -------
    np.array
        The :math:`S_{\delta}` vector built from the input parameters.

    """
    tp = (1 - eta/eta_H)
    return np.array([-eta*_mu_prime(eta, eta_0, Kappa)/(2*eta_H**2*tp), 0, 0, 0])


def _q1(eta_B):
    return np.piecewise(eta_B + 0j, [eta_B > 1, eta_B <= 1],
                        [lambda x: -np.sqrt(1 - 1/x**2), lambda x: 1j*np.sqrt(1/eta_B**2 - 1)])


def _func(eta, X, eta_H, eta_0, Kappa):
    # print(X.shape)
    if len(X.shape) == 1:
        return np.squeeze(_P(eta, eta_H, eta_0, Kappa).dot(X))
    else:
        return _P(eta, eta_H, eta_0, Kappa).dot(X)


def _func1(eta, X, eta_H, eta_0, Kappa):
    # print(X.shape)
    if len(X.shape) == 1:
        return np.squeeze(_P(eta, eta_H, eta_0, Kappa).dot(X)) + _S(eta, eta_H, eta_0, Kappa)
    else:
        return _P(eta, eta_H, eta_0, Kappa).dot(X) + np.transpose(np.tile(_S(eta, eta_H, eta_0, Kappa), (X.shape[1], 1)))


def _func_delta(eta, X, eta_H, eta_0, Kappa):
    # print(X.shape)
    if len(X.shape) == 1:
        return np.squeeze(_P(eta, eta_H, eta_0, Kappa).dot(X)) + _S_delta(eta, eta_H, eta_0, Kappa)
    else:
        return _P(eta, eta_H, eta_0, Kappa).dot(X) + np.transpose(np.tile(_S_delta(eta, eta_H, eta_0, Kappa), (X.shape[1], 1)))


def _solve_system(eta_0, eta_H, Kappa=0.4, eta_span=None, method='DOP853', dense_output=True, **kwargs):
    eta_span_tp = [0, eta_H] if eta_span is None else eta_span
    # eta_val = np.linspace(0, eta_H, 100)
    X0_vec = [np.array([-_mu_prime(0, eta_0, Kappa), 0*1j, 0, 0], dtype='complex_'),
              np.array([0, 0*1j, 1, 0], dtype='complex_'),
              np.array([0, 0*1j, 0, 1], dtype='complex_'),
              np.array([0, 0, 0, 0], dtype='complex_')]
    Results = []
    for i, X0 in enumerate(X0_vec):
        # print(i)
        if i == 0:
            test = solve_ivp(_func1, eta_span_tp, X0, args=(eta_H, eta_0, Kappa), method=method, dense_output=dense_output, **kwargs)
        elif i == 4:
            test = solve_ivp(_func_delta, eta_span_tp, X0, args=(eta_H, eta_0, Kappa), method=method, dense_output=dense_output, **kwargs)
        else:
            test = solve_ivp(_func, eta_span_tp, X0, args=(eta_H, eta_0, Kappa), method=method, dense_output=dense_output, **kwargs)
        Results.append(test)
    return Results


def calculate_solution(eta, eta_H, eta_0, eta_B, Fr, max_z, Kappa=0.4):
    r"""Solve the system and apply the boundary conditions.

    Parameters
    ----------
    eta : scalar, numpy.array
        vector of vertical non dimensional positions :math:`k z` where to calculate the solutions.
    eta_H : scalar, np.array
        Non dimensional boundary layer height :math:`k H`.
    eta_0 : scalar, np.array
        Non dimensional hydrodyamic roughness :math:`k z_{0}`.
    eta_B :  scalar, np.array
        Non dimensional stratification length :math:`k L_{B}`.
    Fr : scalar, np.array
        Froude number
    max_z : scalar, np.array
        Maximum vertical position where the system is solved, and also where the boundary conditons are applied. Usually set to something slightly smaller than `eta_H` to avoid the very slow resolution close to the top of the boundary layer. Usefull when investigating the solution close to the bottom.
    Kappa : float, optional
        Von Karmàn constant (the default is 0.4).

    Returns
    -------
    np.array
        The solution in every vertical step specified by `eta`.

    """
    Results = _solve_system(eta_0, eta_H, Kappa=0.4, eta_span=[0, max_z], atol=1e-10, rtol=1e-10)
    # Defining boundary conditions
    To_apply = np.array([X.sol(max_z)[1:] for X in Results]).T
    #
    b = np.array([1j*mu(max_z, eta_0, Kappa),  # W(eta_H) = i*mu(eta_H)*delta
                  1/max_z,                     # St(eta_H) = delta/eta_H
                  mu(max_z, eta_0, Kappa)**2*(complex(_q1(eta_B)) + 1/(eta_H*Fr**2))])  # Sn(eta_H) = mu(eta_H)**2*(q1 - 1/(eta_H*Fr**2))*delta
    # Applying boundary condition
    pars = np.dot(np.linalg.inv(To_apply[:, :-1]), b - To_apply[:, -1])
    coeffs = np.array([1, pars[1]/pars[0], pars[2]/pars[0], 1/pars[0]])
    # returning solutions in eta
    return np.sum(np.array([X.sol(eta) for X in Results])*coeffs[:, None], axis=0)
