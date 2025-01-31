"""
Linear theory of a turbulent flow over a sinusoidal bottom.


References
----------

.. line-block::
    [1] Fourrière, A. (2009). Morphodynamique des rivières: Sélection de la largeur, rides et dunes (Doctoral dissertation, Université Paris-Diderot-Paris VII).
    [2] Fourriere, A., Claudin, P., & Andreotti, B. (2010). Bedforms in a turbulent stream: formation of ripples by primary linear instability and of dunes by nonlinear pattern coarsening. Journal of Fluid Mechanics, 649, 287-328.
    [3] Andreotti, B., Fourriere, A., Ould-Kaddour, F., Murray, B., & Claudin, P. (2009). Giant aeolian dune size determined by the average depth of the atmospheric boundary layer. Nature, 457(7233), 1120-1123.
    [4] Andreotti, B., Claudin, P., Devauchelle, O., Durán, O., & Fourrière, A. (2012). Bedforms in a turbulent stream: ripples, chevrons and antidunes. Journal of Fluid Mechanics, 690, 94-128.

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
    r"""Calculate the basal shear stress over a two dimensional sinusoidal topography for a wind from left to right (along the :math:`x`-direction):

        .. math::

            \Tau_{x} = \Re\left(1 + (\mathcal{A}_{x}(\alpha, \mathcal{A}_{0}) + i\mathcal{B}_{x}(\alpha, \mathcal{B}_{0}))k\xi\exp^{i\cos\alpha x + \sin\alpha y}\right)
            \Tau_{y} = \Re\left((\mathcal{A}_{y}(\alpha, \mathcal{A}_{0}) + i\mathcal{B}_{y}(\alpha, \mathcal{B}_{0}))k\xi\exp^{i\cos\alpha x + \sin\alpha y}\right)

    Parameters
    ----------
    x : array, scalar
        Streamwise coordinate, non-dimensional (:math:`kx`).
    y : array, scalar
        Spanwise coordinate, non-dimensional (:math:`ky`).
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    A0 : array, scalar
        value of the in-phase hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.
    B0 : array, scalar
        value of the in-quadrature hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.
    AR : array, scalar
        dune aspect ratio, :math:`k\xi`.

    Returns
    -------
    Taux : array, scalar
        Streamwise component of the non-dimensional shear stress.
    Tauy : array, scalar
        Spanwise component of the non-dimensional shear stress

    """

    Taux = np.real(+ (1 + (Ax(alpha, A0) + 1j*Bx(alpha, B0))*AR*np.exp(1j*(cosd(alpha)*x + sind(alpha)*y))))
    Tauy = np.real(+ (Ay(alpha, A0) + 1j*By(alpha, B0))*AR*np.exp(1j*(cosd(alpha)*x + sind(alpha)*y)))
    return Taux, Tauy


def Cisaillement_basal_rotated_wind(x, y, alpha, A0, B0, AR, theta):
    r"""Calculate the basal shear stress over a two dimensional sinusoidal topography for an arbitrary wind direction.

    Parameters
    ----------
    x : array, scalar
        Streamwise coordinate, non-dimensional (:math:`kx`).
    y : array, scalar
        Spanwise coordinate, non-dimensional (:math:`ky`).
    alpha : array, scalar
        Dune orientation with respect to the perpendicular to the flow direction (in degree).
    A0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.
    B0 : array, scalar
        value of the hydrodynamic coefficient for :math:`\alpha = 0`, i.e. for a dune orientation perpendicular to the flow direction.
    AR : array, scalar
        dune aspect ratio, :math:`k\xi`.
    theta : array, scalar
        Wind direction, in degree, in the trigonometric convention.

    Returns
    -------
    Taux : array, scalar
        Streamwise component of the non-dimensional shear stress.
    Tauy : array, scalar
        Spanwise component of the non-dimensional shear stress

    """
    # same but for an arbitrary wind direction oriented by theta
    xrot = x*cosd(theta) + y*sind(theta)
    yrot = y*cosd(theta) - x*sind(theta)
    alpha_rot = ((alpha - theta + 90) % 180) - 90
    # alpha_rot = alpha - theta
    Taux, Tauy = Cisaillement_basal(xrot, yrot, alpha_rot, A0, B0, AR)
    return cosd(theta)*Taux - sind(theta)*Tauy,  Taux*sind(theta) + Tauy*cosd(theta)


# %%
# Hydrodynamic coefficients approximation Fourriere 2011
# -----------------

def function_coeff(R, a):
    return a[0] + (a[1] + a[2]*R + a[3]*R**2 + a[4]*R**3)/(1 + a[5]*R**2 + a[6]*R**4)


def coeffA0(eta_0):
    R = np.log(2*np.pi/eta_0)
    a = [2, 1.0702, 0.093069, 0.10838, 0.024835, 0.041603, 0.0010625]
    return function_coeff(R, a)


def coeffB0(eta_0):
    R = np.log(2*np.pi/eta_0)
    b = [0, 0.036989, 0.15765, 0.11518, 0.0020249, 0.0028725, 0.00053483]
    return function_coeff(R, b)


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


def _solve_system(eta_0, eta_H, Kappa=0.4, max_z=None, method='DOP853', dense_output=True, **kwargs):
    eta_span_tp = [0, eta_H] if max_z is None else [0, max_z]
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


def calculate_solution(eta, eta_H, eta_0, eta_B, Fr, max_z, Kappa=0.4, output='simple', **kwargs):
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
    output : string, optional
        changes what returns the function (default is 'simple').

    Returns
    -------
    np.array, list
        If `output` is 'simple', return an array with the solution in every vertical step specified by `eta`. If `output` is 'full', return a list whose elements are:
        - the array with the solution in every vertical step specified by `eta`.
        - the output of `_solve_system`.
        - the coefficients of the linear decomposition of the solution.

    """
    Results = _solve_system(eta_0, eta_H, Kappa=0.4, max_z=max_z, atol=1e-10, rtol=1e-10, **kwargs)
    # Defining boundary conditions
    To_apply = np.array([X.sol(max_z)[1:] for X in Results]).T
    #
    b = np.array([1j*mu(max_z, eta_0, Kappa),  # W(eta_H) = i*mu(eta_H)*delta
                  1/max_z,                     # St(eta_H) = delta/eta_H
                  mu(max_z, eta_0, Kappa)**2*(complex(_q1(eta_B)) + 1/(eta_H*Fr**2))])  # Sn(eta_H) = mu(eta_H)**2*(q1 - 1/(eta_H*Fr**2))*delta
    # Applying boundary condition
    pars = np.dot(np.linalg.inv(To_apply[:, :-1]), b - To_apply[:, -1])
    coeffs = np.array([1, pars[1]/pars[0], pars[2]/pars[0], 1/pars[0]])
    coeffs_expanded = np.expand_dims(coeffs, (1, ) + tuple(np.arange(len(np.array(eta).shape)) + 2))
    # returning solutions in eta
    if output == 'simple':
        return np.sum(np.array([X.sol(eta) for X in Results])*coeffs_expanded, axis=0)
    elif output == 'full':
        return [np.sum(np.array([X.sol(eta) for X in Results])*coeffs_expanded, axis=0),
                Results,
                coeffs]
