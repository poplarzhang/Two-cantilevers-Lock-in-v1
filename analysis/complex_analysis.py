# Complex analysis tools for two-channel HF2LI measurements.
# Apply two cantilevers 

import numpy as np


# ---------------------------------------------------------
# Convert x/y into complex signals
# ---------------------------------------------------------

def get_complex_signals(measurement):
    """
    Build complex signals from one measurement.

    Parameters
    ----------
    measurement : dict

    Returns
    -------
    z0, z1 : ndarray
        Complex signals from demodulator 0 and 1.
    """

    x0 = np.asarray(measurement["x_0"], dtype=float)
    y0 = np.asarray(measurement["y_0"], dtype=float)

    x1 = np.asarray(measurement["x_1"], dtype=float)
    y1 = np.asarray(measurement["y_1"], dtype=float)

    z0 = x0 + 1j * y0
    z1 = x1 + 1j * y1

    return z0, z1


# ---------------------------------------------------------
# Sample-by-sample complex ratio
# ---------------------------------------------------------

def calculate_complex_ratio(measurement):
    """
    Calculate the complex ratio for every sample.

    Returns
    -------
    ndarray
        Complex array Z0/Z1.
    """

    z0, z1 = get_complex_signals(measurement)

    return z0 / z1


# ---------------------------------------------------------
# One representative ratio per measurement
# ---------------------------------------------------------

def calculate_mean_complex_ratio(measurement):
    """
    Calculate one representative complex ratio.

    The mean complex signal is calculated first,
    then the ratio is formed.

    Returns
    -------
    complex
    """

    z0, z1 = get_complex_signals(measurement)

    mean_z0 = np.mean(z0)
    mean_z1 = np.mean(z1)

    return mean_z0 / mean_z1


# ---------------------------------------------------------
# One point for every measurement in a folder
# ---------------------------------------------------------

def calculate_mean_ratios(measurements):
    """
    Calculate one complex ratio for each measurement.

    Parameters
    ----------
    measurements : list

    Returns
    -------
    ndarray
        Complex array with one value per measurement.
    """

    ratios = []

    for measurement in measurements:

        ratios.append(
            calculate_mean_complex_ratio(
                measurement
            )
        )

    return np.asarray(ratios)


# ---------------------------------------------------------
# Convert complex ratios into plotting arrays
# ---------------------------------------------------------

def split_complex(
    ratios,
    experiment_angles=None,
    labels=None
):
    """
    Prepare complex ratios for plotting.

    Parameters
    ----------
    ratios : array
        Complex ratios.

    experiment_angles : array
        Experimental angle for each measurement.

    labels : list
        Measurement labels.
    """

    ratios = np.asarray(ratios)


    result = {

        "real": np.real(ratios),

        "imag": np.imag(ratios),

        "magnitude": np.abs(ratios),

        "argument": np.angle(
            ratios,
            deg=True
        )

    }


    if experiment_angles is not None:

        result["experiment_angle"] = np.asarray(
            experiment_angles
        )


    if labels is not None:

        result["labels"] = labels


    return result