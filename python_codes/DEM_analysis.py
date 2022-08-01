"""
Functions used in the analysis of elevation data.

"""

import numpy as np
from scipy.signal import find_peaks, correlate
from scipy.ndimage import map_coordinates
from python_codes.general import cosd, sind


def array_transect(A, p0, p1, type='cubic', num=100):
    """Compute the profile between to points inside a matrix.

    Parameters
    ----------
    A : array_like, shape(M, N)
        Input array.
    p0 : array_like, shape(2,)
        Pixel coordinates of the starting point.
    p1 : array_like, shape(2,)
        Pixel coordinates of the ending point.
    type : str, optional
        Type of the interpolation: 'nearest' or 'cubic' (the default is 'nearest').
    num : int, optional
        Size of the output interpolated transect (the default is 100).

    Returns
    -------
    array_like, shape(num,)
        Interpolated transect between `p0` and `p1`.

    """
    x0, y0 = p0[1], p0[0]  # These are in pixel coordinates!!
    x1, y1 = p1[1], p1[0]
    #
    if type == 'cubic':
        x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
        #
        # Extract the values along the line, using cubic interpolation
        return map_coordinates(A, np.vstack((x, y)))
    elif type == 'nearest':
        length = int(np.hypot(x1-x0, y1-y0))
        x, y = np.linspace(x0, x1, length), np.linspace(y0, y1, length)
        x_ok, y_ok = x[(x > 0) & (x < A.shape[0]) & (y > 0) & (y < A.shape[1])], y[(x > 0) & (x < A.shape[0]) & (y > 0) & (y < A.shape[1])]
        #
        # Extract the values along the line
        return A[x_ok.astype(np.int), y_ok.astype(np.int)]
    else:
        print('wrong type')


def polyfit2d(X, Y, Z, kx, ky, order_max=None):
    """Fitting polynomials in 2d dimensions.
        Resultant fit can be plotted with: `np.polynomial.polynomial.polygrid2d(x, y, p.reshape((kx+1, ky+1)).T)`

    Parameters
    ----------
    X : array_like, shape (M,N)
        1st coordinate array as output of `np.meshgrid`.
    Y : array_like, shape (M,N)
        2nd coordinate array as output of `np.meshgrid`.
    Z : array_like, shape (M,N)
        Surface points to be fitted
    kx : int
        Degree in the first coordinate.
    ky : int
        Degree in the second coordinate.
    order_max : int or None, optional
        If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
        If int, coefficients up to a maximum of kx+ky <= order_max are considered (the default is None).

    Returns
    -------
    p: ndarray
        Least-squares solution from
    residuals: ndarray
        Sums of squared residuals.
    rank: int
        Rank of matrix a.
    s: ndarray
        Singular values of a.

    """
    X_flat, Y_flat = X.flatten(), Y.flatten()
    power_x, power_y = np.meshgrid(np.arange(kx + 1), np.arange(ky + 1))
    coeffs = np.ones(power_x.shape)
    if order_max is not None:
        mask_order = (power_x + power_y) > order_max
        coeffs[mask_order] = 0
    A = coeffs.flatten()[None, :]*X_flat[:, None]**power_x.flatten()[None, :]*Y_flat[:, None]**power_y.flatten()[None, :]
    return np.linalg.lstsq(A, Z.flatten(), rcond=None)


def find_first_max(a, type='first', min_pos=0, max_pos=-1):
    """Find the first maximum of an autocorrelation profile.

    Parameters
    ----------
    a : array_like, shape (N, )
        Input array.
    type : str
        If 'first', the returned peak is the first peak detected by `scipy.signal.find_peaks`. If 'max', the returned peak is the one with the largest height (the default is 'first').
    min_pos : int
        Minimum index above which the peak is searched (the default is 0).
    max_pos : int
        Minimum index below which the peak is searched (the default is -1).

    Returns
    -------
    int
        Return the position of the first peak.

    """
    peaks = find_peaks(a)[0]
    if max_pos == -1:
        max_pos = a.size
    if len(peaks) > 0:
        mask = (peaks >= min_pos) & (peaks <= max_pos) & (a[peaks] > 0)
        peaks = peaks[mask]
        if len(peaks) > 0:
            a_norm = a/np.max(a)
            if type == 'first':
                ind = 0
            elif type == 'max':
                ind = np.argmax(a_norm[peaks])
            else:
                print('wrong argument type in function call')
            lamb = peaks[ind]
        else:
            lamb = np.nan
    else:
        lamb = np.nan
    return lamb


def periodicity_2d(A, rad, type='first'):
    r"""Calculate the properties (orientation, wavelength, amplitude) of a 2-dimensional pattern.

    - The orientation is calculated by computed the integration over `rad` of the autocorrelation matrix around its maximum in each direction. The pattern orientation is then taken as where the maximum is.
    - The wavelength is taken at the position of the first maximum of the autocorrelation profile in the direction perpendicular to the orientation.
    - The amplitude is linked to the maximum of the autocorrelation matrix as :math:`A = \sqrt{2 C(0, 0)}`.

    Parameters
    ----------
    A : array_like
        Input array.
    rad : int
        Distance over wich the integration for the cauclation of the orientation is computed.
    type : str
        Type of the detection of the peak of the autocorrelation for finding the wavelength. It can be 'first' or 'max'. See `python_codes.DEM_analysis.find_first_max for details.`

    Returns
    -------
    orientation: float
        Orientation of the pattern in degrees.
    wavelength: float
        Wavelength of the pattern in pixels.
    amplitude: float
        Amplitude of the pattern in the input array unit.
    p0: array_like, shape (2,)
        Coordinates of the maximum of the autocorrelation matrix.
    p1: array_like, shape (2,)
        Coordinates of the end of the profile used for the calculation of the wavelength.
    transect: array_like
        Profile used for the calculation of the wavelength.
    C: array_like
        Autocorrelation matrix.

    """
    C = correlate(A, A)/A.size
    alpha = list(np.linspace(0, 179, 181))
    grad = np.zeros((len(alpha),))
    Imax = np.unravel_index(np.argmax(C), C.shape)
    #
    for a in alpha:
        for r in range(rad):
            I_col = int(round(Imax[1] + cosd(a)*r))  # x
            I_row = int(round(Imax[0] + sind(a)*r))  # y
            if I_row < 0:
                I_row = 0
            if I_col < 0:
                I_col = 0
            grad[alpha.index(a)] = grad[alpha.index(a)] + C[I_row, I_col]
    orientation = alpha[np.argmax(grad)]
    if (orientation > 88 and orientation < 92):
        transect = C[A.shape[0], A.shape[1]:]
    elif (orientation < 2 or orientation > 178):
        transect = C[A.shape[0]:, A.shape[1]]
    else:
        p0 = np.array(Imax[::-1])
        p1 = p0 + np.array([cosd(orientation + 90), sind(orientation + 90)])*min(A.shape)
        transect = array_transect(C, p0, p1, type='cubic', num=int(round(np.linalg.norm(p1-p0))))

    wavelength = find_first_max(transect)
    amplitude = np.sqrt(2*transect[0])
    return orientation, wavelength, amplitude, p0, p1, transect, C
