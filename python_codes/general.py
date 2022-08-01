"""
A few general functions used in many scripts.
"""

import numpy as np
from xhistogram.core import histogram


def tand(x):
    """Compute tangent element-wise using :func:`np.tan <numpy.tan>` with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.tan(np.radians(x))


def sind(x):
    """Trigonometric sine using :func:`np.sin <numpy.sin>`, element-wise with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.sin(np.radians(x))


def cosd(x):
    """Cosine element-wise :func:`np.cos <numpy.cos>` with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.cos(np.radians(x))


def Vector_average(angles, norm, axis=-1):
    """Calculate the average vector from series of angles and norms.

    Parameters
    ----------
    angles : array_like
        angles.
    norm : array_like
        norms.
    axis : None or int
        axis along wich the averaging is performed (the default is -1). None compute the average on the flattened array.

    Returns
    -------
    angle : array_like
        the counterclockwise angle of the resultant vector in the range [-180, 180].
    norm : array_like
        norm of the resultant vector.

    """
    average = np.nanmean(norm*np.exp(1j*np.radians(angles)), axis=axis)
    return np.degrees(np.angle(average)), np.absolute(average)


def smallestSignedAngleBetween(x, y):
    """Calculate the smallest angle between two angle arrays.

    Parameters
    ----------
    x : array_like
        First angle.
    y : array_like
        Second angle.

    Returns
    -------
    array_like
        return the smallest angle between `y` and `x`, elementwise.

    """
    a = (x - y) % 360
    b = (y - x) % 360
    return np.where(a < b, -a, b)


def find_mode_distribution(data, bin_number):
    """Find de mode of a distribution from a serie of realisations of the random variable.

    Parameters
    ----------
    data : array_like
        serie of realisation of the random variable
    bin_number : int
        number of bins used is the calculation of the histogram.

    Returns
    -------
    float
        return the mode of the distribution.

    """
    counts, bins_edges = np.histogram(data, bins=bin_number)
    bin_centers = bins_edges[:-1] + (bins_edges[1] - bins_edges[0])
    return bin_centers[counts.argmax()]


def Make_angular_PDF(angles, weight, bin_edges=np.linspace(0, 360, 361), axis=-1):
    """Calculate the angular PDF (normalized) from input arrays.

    Parameters
    ----------
    angles : np.array
        array of angles.
    weight : np.array
        array of weights. Its dimensions must match those of angles.
    bin_edges : np.array
        array containing the bins used to calculate the distribution (the default is np.linspace(0, 360, 361)).
    axis : int
        axis of the input aray along which the distribution is calculated (the default is -1).

    Returns
    -------
    hist: np.array
        array containing the distribution.
    bin_centers: np.array
        array containing the bin centers of the distribution.

    """
    hist, _ = histogram(angles, bins=bin_edges, density=1, weights=weight, axis=axis)
    bin_centers = bin_edges[1:] - (bin_edges[1] - bin_edges[0])/2
    return hist, bin_centers
