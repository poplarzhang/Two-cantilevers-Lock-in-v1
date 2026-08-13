"""
Resonance fitting tools.
"""

import numpy as np
from scipy.optimize import curve_fit



# =====================================================
# Lorentzian model
# =====================================================

def lorentzian(
    frequency,
    f0,
    gamma,
    amplitude,
    offset
):

    """
    Lorentzian resonance function.

    f0:
        resonance frequency

    gamma:
        half width at half maximum

    amplitude:
        peak amplitude

    offset:
        background
    """



    return (
        offset 
        +
        amplitude
        *
        (
            gamma**2
            /
            (
                (frequency-f0)**2
                +
                gamma**2
            )
        )
    )



# =====================================================
# Resonance fit
# =====================================================

def fit_resonance(
    frequency,
    amplitude
):

    """
    Robust resonance fit.

    Returns:
        f0
        linewidth
        Q
    """


    # Convert to numpy arrays

    frequency = np.asarray(
        frequency
    )

    amplitude = np.asarray(
        amplitude
    )



    # Remove possible invalid points

    mask = np.isfinite(
        amplitude
    )


    frequency = frequency[mask]

    amplitude = amplitude[mask]



    # Initial resonance frequency

    index = np.argmax(
        amplitude
    )


    f0_guess = frequency[index]



    # Background estimate

    offset_guess = np.min(
        amplitude
    )



    # Peak height

    amplitude_guess = (
        np.max(amplitude) -
        offset_guess
    )

    # Estimate linewidth from data range

    linewidth_guess = (frequency[-1] - frequency[0]) / 10 # frequency[-1] means the last element in a arrary//10/AUG YZ

    initial = [

        f0_guess,

        linewidth_guess,

        amplitude_guess,

        offset_guess

    ]

    # Add parameter limits
    #
    # This prevents impossible solutions

    lower = [

        frequency[0],

        0,

        0,

        -np.inf

    ]

    upper = [

        frequency[-1],

        frequency[-1] - frequency[0],

        np.inf,

        np.inf

    ]

    parameters, covariance = curve_fit(

        lorentzian,

        frequency,

        amplitude,

        p0=initial,

        bounds=(
            lower,
            upper
        ),

        maxfev=10000

    )

    f0 = parameters[0]
    gamma = parameters[1]

    Q = (f0 / (2*gamma) )


    return {
        "f0": f0,

        "gamma": gamma,

        "Q": Q,

        "parameters": parameters,

        "covariance": covariance
    }